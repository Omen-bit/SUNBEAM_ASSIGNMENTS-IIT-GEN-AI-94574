import streamlit as st
import pandas as pd
import pandasql as ps
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("CSV Question Answering Agent")

file = st.file_uploader("Upload CSV", type="csv")
question = st.chat_input("Ask a question about the CSV")

if file:
    df = pd.read_csv(file)
    schema = {col: str(dtype) for col, dtype in df.dtypes.items()}

    if st.button("Show Schema"):
        st.json(schema)
        st.dataframe(df.head())

    @tool
    def query_csv(sql: str) -> str:
        """
        Execute a SQLite-compatible SQL SELECT query on the uploaded CSV data.

        This tool should be used to answer analytical questions about the CSV,
        including filtering rows, aggregations (COUNT, SUM, AVG), grouping,
        sorting, and column selection.

        The table name is `data` and only columns present in the schema
        should be referenced.

        Args:
            sql (str): A valid SQLite-compatible SQL SELECT query.

        Returns:
            str: Query results formatted as a string.
        """
        result = ps.sqldf(sql, {"data": df})
        return result.to_string(index=False)

    agent = create_agent(
        model=llm,
        tools=[query_csv]
    )

    if question:
        system_prompt = f"""
You are a CSV Question Answering Agent.

Table name: data
Schema: {schema}

Rules:
- Always use the query_csv tool to answer questions
- Generate only SQLite-compatible SQL
- Use only columns present in the schema
- Do not explain your reasoning, only return the final answer
"""

        try:
            response = agent.invoke({
                "input": question,
                "system": system_prompt
            })
            st.success("Answer")
            st.text(response["output"])
        except Exception:
            st.error("Agent execution failed")
