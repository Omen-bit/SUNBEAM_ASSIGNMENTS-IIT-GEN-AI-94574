import streamlit as st
import pandas as pd
import pandasql as ps

st.title("CSV Explorer")

data_file = st.file_uploader("Upload a csv file", type=['csv'])

if data_file:
    df = pd.read_csv(data_file)
    st.dataframe(df)


    try:
        query = st.text_input("Enter SQL Query to perform on table")
        result = ps.sqldf(query, {"data": df})
        st.dataframe(result)
    except:
        st.write("Wrong SQL Query , Please insert a valid sql query")
    
