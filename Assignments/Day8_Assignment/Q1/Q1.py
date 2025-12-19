# • Create tools: calculator, file reader, current weather, and knowledge lookup
# using @tool decorator.
# • Build an agent with all three tools and test with prompts requiring tool usage.
# • Inspect message history to understand tool-calling flow.

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import os
import requests
import json

@tool
def calculator(expression : str):
    """
    This calculator function solves any arithmetic expression containing all constant values.
    It supports basic arithmetic operators +, -, *, /, and parenthesis. 
    
    :param expression: str input arithmetic expression
    :returns expression result as str
    """
    try:
        result=eval(expression)
        return str(result)
    except:
        return "Error : Cannot solve the given expression"

@tool
def file_read(file_path):
    """
    Reads and returns the full text content of a file from the given file path.

    This tool opens a file in read mode, reads all its contents, and returns
    the data as a single string. It is intended for text-based files such as
    .txt, .md, or source code files.
    return a good summarization of the  content present inside the file path 

    :param filepath: Absolute or relative path to the file to be read
    :type filepath: str
    :return: Complete content of the file as a string
    :rtype: str
    :raises FileNotFoundError: If the specified file does not exist
    :raises IOError: If the file cannot be opened or read
    """
    with open(file_path , 'r') as file :
        text=file.read()
        return text

@tool
def current_weather(city):
    """
    This get_weather() function gets the current weather of given city.
    If weather cannot be found, it returns 'Error'.
    This function doesn't return historic or general weather of the city.

    :param city: str input - city name
    :returns current weather in json format or 'Error'    
    """

    API_KEY=os.getenv("WEATHER_API")
    base_url="https://api.openweathermap.org/data/2.5/weather"

    url=f"{base_url}?appid={API_KEY}&q={city}&units=metric"

    try:
        response=requests.get(url)
        weather=response.json()
        return weather
    except:
        return "Error : cannot find weather of the given city"




load_dotenv()

#create an llm 
llm=init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    api_key="dummy_api",
    base_url="http://10.186.172.6:1234/v1"
)

#create a agent
agent=create_agent(
    model=llm,
    tools=[
        calculator,
        file_read,
        current_weather
    ],
    system_prompt="""
    You are a helpful, intelligent AI assistant.

    • Answer general knowledge and conceptual questions directly using your own knowledge.
    • Use tools ONLY when a question explicitly requires calculation, file reading, or live weather data.
    • Do NOT force tool usage for normal questions.
    • If no tool is relevant, respond with a clear, direct answer.
    • Keep answers crisp, accurate, and easy to understand.
    """
)

st.title("Smart ChatBot")

user_input = st.chat_input("Ask anything (you can provide a file path like: Read D:/test.txt)")

if user_input:
    result = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })
    llm_output = result["messages"][-1]
    if hasattr(llm_output, "tool_calls") and llm_output.tool_calls:
        st.json(llm_output.tool_calls)
    else:
        st.write(llm_output.content)