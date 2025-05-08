# Streamlit App Final Project 
### Project Overview: 
The goal of this project is to demonstrate my **proficiency in Streamlit, data parsing, and data visualization** by developing an **advanced app** that enables detailed analysis of rowing workout data exported from NK CoxBox or SpeedCoach devices. Uaing Pandas for data manipulation and MatPlotLib for visualization, the app produces insightful, real-time charts that track stroke rate trends, splits, and efficiency comparisons like meters-per-stroke. Designed specifically for coaches, coxswains, and rowers, the app **streamlines performance review by transforming raw workout data into clear, actionable insights**. This project also reflects my ability to **handle complex data preprocessing**, **implement error handling**, and **create a user-friendly interface** for a specialized audience.

Link to Python file: https://github.com/margaretabbott/Abbott-Python-Portfolio/blob/main/StreamlitAppFinal/RowingDataAnalyzer.py  
### Instructions & Dependencies:  
Dependencies: **Streamlit**, **Pandas**, **StringIO**, and **MatPlotLib**  

Link to requirements: https://github.com/margaretabbott/Abbott-Python-Portfolio/blob/main/StreamlitAppFinal/requirements.txt  
### App Features:
The app **automatically detects and extracts multiple data sections** from NK CoxBox and SpeedCoach CSV files, handling **varying headers and formats**. Users can interactively select key performance metrics and view real-time visualizations, including stroke rate trends, split times, and efficiency comparisons. The app also provides a **clean performance summary** and intuitive filtering to streamline the analysis process for coaches, coxswains, and rowers.
### Link To My Streamlit App: 
https://rowingdataanalyzer.streamlit.app/  
### Dataset Description: 
Since the average person does not have NK SpeedCoach or CoxBox workout data to download and upload, a sample dataset is inlcuded. This dataset (as will all others from NK) includes four sections: session information, session summary, summary for session intervals, and session detail data. Session deatil data is were analytical work can be done as this breaks down the data of each stroke, each 100m, or each 500m, showing metrics such as split, meters per stroke, stroke rate, heart rate (if set up for this), time, etc. depending on the set up of the workout. The three other sections are purely informational on their own. 

Link to sample data: https://github.com/margaretabbott/Abbott-Python-Portfolio/blob/main/StreamlitAppFinal/SpeedCoach%20GPS.csv
