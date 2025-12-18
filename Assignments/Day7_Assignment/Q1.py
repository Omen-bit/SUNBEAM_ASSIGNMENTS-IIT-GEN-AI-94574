# Q1: Create a Streamlit application that allows users to upload a CSV file and view its schema.Use an LLM to convert user questions into SQL queries, execute them on the CSV data using pandasql, and explain the results in simple English.


import streamlit as st
import pandas as pd
import pandasql as ps
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm=init_chat_model(
    model="openai/gpt-oss-120b" ,
    model_provider="openai" ,
    base_url="https://api.groq.com/openai/v1" ,
    api_key=os.getenv("GROQ_API_KEY")

)

conversation=[
    {
        "role" : "system" , 
        "content" : "You are a SQLite developer with 10 years of experience"
    }
]

st.title("Explore CSV")
upload_csv=st.file_uploader("Upload a csv",type="csv")

user_input=st.chat_input("what operations you want to perform")

if upload_csv:
    df=pd.read_csv(upload_csv)
    st.write(df.dtypes)
    st.dataframe(df)

    llm_input=f"""
        Table Name = data
        Table Schema = {df.dtypes}
        Question = {user_input}
        Instructions = 
            Write a SQL query for the above question. 
            Generate SQL query only in plain text format and nothing else.
            If you cannot generate the query, then output 'Error'.
        """ 
    if user_input:
        result=llm.invoke(llm_input)

        if result.content == "Error" :
            st.error("Error!! , Please input a valid question according to the table")
        else:
            st.success(f"Query :  {result.content}")
            query=result.content
            result = ps.sqldf(query, {"data": df})
            st.dataframe(result)

            llm_input2=f"""
                Table Name = data
                Table Schema = {df.dtypes}
                Query = {query}
                Question = Explain the logic of how the sql query was generated , the result should be short , crisp and exactly to the point    
            """
            result2=llm.invoke(llm_input2)
            st.success(f"Explanation :  {result2.content}")


