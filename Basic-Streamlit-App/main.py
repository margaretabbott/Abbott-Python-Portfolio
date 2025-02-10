import streamlit as st
import pandas as pd
st.title("Hello, Streamlit")
st.write("Streamlit lets me build interactive web apps.")
penguins=pd.read_csv("data/my_data_penguins.csv")
st.dataframe(penguins)
island=st.selectbox("Select an island",penguins["island"].unique())
filtered_penguins=penguins[penguins["island"]==island]
st.dataframe(filtered_penguins)
