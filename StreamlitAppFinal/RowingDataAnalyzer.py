## Importing all necessary libraries
## StringIO is needed since there are multiple data sections/tables in one sheet and there is irregular spacing between them
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import matplotlib.ticker as ticker

## Creating the title for the Streamlit APP
st.title("Rowing Workout Analyzer")
st.header("On the Water Performance")

## Putting in a little blurb about what this app does and why it was created
st.write("This Streamlit App is designed to allow coaches, coxswains, or rowers to " \
"analyze on the water data that has been downloaded from their NK CoxBox or SpeedCoach. " \
"Although these devices can give useful information, this app is unique as it shows " \
"relevant graphs that otherwise could not be created with ease.")

## Uploading the CSV file to be analyzed 
uploaded_file=st.file_uploader(
    "Upload your CSV file downloaded from your NK CoxBox or SpeedCoach",
    type=["csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            ## Converting bytes into strings using utf-8
            content=uploaded_file.read().decode("utf-8").splitlines()
            ## Splits the different data sections/tables
            section_headers = {
                "Session Information": None,
                "Session Summary": None,
                "Summary for Session Intervals": None,
                "Session Detail Data": None}
            
            for i, line in enumerate(content):
                for header in section_headers:
                    if line.strip().startswith(header):
                        section_headers[header]=i

            sections={}
            headers_list=list(section_headers.items())
            for idx, (name, start_line) in enumerate(headers_list):
                if start_line is None:
                    continue

                end_line=None
                for next_idx in range(idx + 1, len(headers_list)):
                    if headers_list[next_idx][1] is not None:
                        end_line=headers_list[next_idx][1]
                        break

                ## If no next header, go to end of file
                section_lines=content[start_line + 1:end_line]

                ## Skip leading empty lines in the section
                while section_lines and section_lines[0].strip()=="":
                    section_lines=section_lines[1:]

                sections[name]=section_lines

            dataframes={}
            for section_name, lines in sections.items():
                if not lines or all(line.strip()=="" for line in lines):
                    continue
                try:
                    ## If section is "Session Information", use header rows 0 
                    if section_name=="Session Information":
                        df=pd.read_csv(StringIO("\n".join(lines)), header=[0])
                    else:
                        ## For all other sections, use header rows 1 and 2
                        df=pd.read_csv(StringIO("\n".join(lines)), header=[1, 2])

                    ## Cleans up multi-index column names in the CSV file
                    df.columns=[" ".join([str(c).strip() for c in col if str(c) != "nan"])
                                  for col in df.columns.values]

                    ## Drop first row if it looks like a repeat header
                    if df.iloc[0].astype(str).str.contains(r'\(.*\)').any():
                        df = df.drop(index=0).reset_index(drop=True)

                except:
                    ## If two headers fails, fallback to single header row
                    df=pd.read_csv(StringIO("\n".join(lines)))

                if not df.empty:
                    dataframes[section_name]=df

            if not dataframes:
                ## Prints an error message so the user knows the file isnt valid
                st.error("No valid data sections found.")
            else:
                ## Prints a message so the user knows the file is valid 
                st.success(f"Found {len(dataframes)} data sections: {list(dataframes.keys())}")
                st.write("Four data sections should be found: Session Information, Session Summary, " \
                "Summary for Session Intervals, and Session Detail Data. Of these sections, analysis will " \
                "only be done on Session Deatil Data as all other sections are soley informational.")
                section_choice=st.selectbox("Select Data Section", list(dataframes.keys()))
                df=dataframes[section_choice]

                ## Shows a preview of the selected data section 
                st.write(f"### Preview of '{section_choice}' section")
                st.dataframe(df.head())

            ## Only proceed with analysis if "Session Detail Data" is selected
            if section_choice=="Session Detail Data":

                ## Writes a list of the column names for the user to see easily
                st.write("### Detected Columns:", df.columns.tolist())

                ## Creates auto selection of columns for analysis but allows user to manually select if necessary
                def auto_select_column(possible_names, columns):
                    for name in possible_names:
                        for col in columns:
                            if name.lower() in col.lower():
                                return col
                    return columns[0]  

                st.write("Select boxes will auto fill to the column that is most likely to fit for the " \
                "analytical purpose, but manual selection is avaliable in case an error occurs with auto selection.")
                time_col=st.selectbox("Select Time Column", df.columns,
                    index=df.columns.get_loc(auto_select_column(["time"], df.columns)))
                stroke_rate_col=st.selectbox("Select Stroke Rate Column", df.columns,
                    index=df.columns.get_loc(auto_select_column(["stroke rate", "spm"], df.columns)))
                distance_col=st.selectbox("Select Distance Column", df.columns,
                    index=df.columns.get_loc(auto_select_column(["distance", "meters"], df.columns)))
                split_col=st.selectbox("Select Split Column", df.columns,
                    index=df.columns.get_loc(auto_select_column(["split"], df.columns)))
                meters_per_stroke_col=st.selectbox("Select Speed Column (Meters/Stroke)", df.columns,
                    index=df.columns.get_loc(auto_select_column(["speed", "m/stroke", "mps"], df.columns)))
                strokes_col=st.selectbox("Select Stroke Count Column", df.columns,
                    index=df.columns.get_loc(auto_select_column(["strokes", "stroke count"], df.columns)))
                heart_rate_col=st.selectbox("Select Heart Rate Column", df.columns,
                    index=df.columns.get_loc(auto_select_column(["heart rate", "hr"], df.columns)))

                ## Converts data to numeric when necessary
                df[stroke_rate_col]=pd.to_numeric(df[stroke_rate_col], errors='coerce')
                df[distance_col]=pd.to_numeric(df[distance_col], errors='coerce')
                df[heart_rate_col]=pd.to_numeric(df[heart_rate_col], errors='coerce')

                ## Converts split times to total seconds using pd.to_timedelta
                df['total_seconds'] = pd.to_timedelta("00:" + df[split_col].astype(str)).dt.total_seconds()

                average_seconds=df['total_seconds'].mean()
                minutes=int(average_seconds // 60)
                seconds=average_seconds % 60
                formatted_time=f"{minutes}:{seconds:04.1f}"

                if df.empty:
                    ## Prints a message that tells the user the data is not valid
                    st.error("No valid data after cleaning.")
                else:
                    ## Creates aggregate and index functions to show basic metrics from the data
                    total_distance=df[distance_col].iloc[-1]-df[distance_col].iloc[0]
                    total_time=df[time_col].iloc[-1]
                    avg_srate=df[stroke_rate_col].mean()
                    max_srate=df[stroke_rate_col].max()
                    avg_msp=round(df[meters_per_stroke_col].mean(),2)
                    total_strokes=df[strokes_col].count()
                    avg_heartrate=df[heart_rate_col].mean()
                    max_heartrate=df[heart_rate_col].max()

                    ## Displays the functions created above in 3 columns not just in 1 row
                    st.write("### Performance Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Distance (m)", f"{total_distance:.0f}")
                        st.metric("Total Time", f"{total_time}")
                        st.metric("Average Stroke Rate (spm)", f"{avg_srate:.1f}")
                    with col2:
                        st.metric("Max Stroke Rate (spm)", f"{max_srate:.1f}")
                        st.metric("Average Split", f"{formatted_time}")
                        st.metric("Average Meters per Stroke", f"{avg_msp}")
                    with col3:
                        st.metric("Total Strokes Taken", f"{total_strokes}")
                        st.metric("Average Heart Rate", f"{avg_heartrate}")
                        st.metric("Highest Heart Rate", f"{max_heartrate}")

                    ## Visuals that show interesting insights 
                    st.write("Three visuals are displayed below for ease of analysis by coaches, coxswains " \
                    "or rowers. The line or points of each graph desired will depend on the type of workout being uploaded.")
                    st.write("### Stroke Rate Over Distance")
                    fig, ax=plt.subplots(figsize=(10, 4))
                    ax.plot(df[distance_col], df[stroke_rate_col], color='magenta')
                    ax.set_xlabel("Distance (m)")
                    ax.set_ylabel("Stroke Rate (spm)")
                    ax.set_title("Stroke Rate vs Distance")
                    ax.grid(True)
                    st.pyplot(fig)

                    st.write("### Split Over Distance")
                    fig2, ax2 = plt.subplots(figsize=(10, 4))
                    ax2.plot(df[distance_col], df['total_seconds'], color='purple')
                    ax2.set_xlabel("Distance (m)")
                    ## Format y-axis ticks as MM:SS.s like a typical split
                    def seconds_to_mmss(x, pos):
                        if pd.isna(x):
                            return ""
                        m=int(x//60)
                        s=x%60
                        return f"{m}:{s:04.1f}"
                    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(seconds_to_mmss))
                    ax2.set_ylabel("Split")
                    ax2.set_title("Split vs Distance")
                    ax2.grid(True)
                    st.pyplot(fig2)

                    st.write("### Meters per Stroke Compared to Stroke Rate")
                    fig3, ax3=plt.subplots(figsize=(10, 4))
                    ax3.scatter(df[stroke_rate_col], df[meters_per_stroke_col], color='pink')
                    ax3.set_xlabel("Stroke Rate (spm)")
                    ax3.set_ylabel("Meters per Stroke")
                    ax3.set_title("Stroke Rate vs Meters per Stroke")
                    ax3.grid(True)
                    st.pyplot(fig3)

    except Exception as e:
        st.error(f"An error occurred: {e}")
