# Q2: Create a Streamlit application that takes a city name as input from the user.Fetch the current weather using a Weather API and use an LLM to explain the weather conditions in simple English.

from langchain.chat_models import init_chat_model
import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

API_KEY=os.getenv("WEATHER_API")

def get_weather(city):
    base_url="https://api.openweathermap.org/data/2.5/weather"

    url=f"{base_url}?appid={API_KEY}&q={city}&units=metric"
    response=requests.get(url)

    if response.status_code == 200 :
        weather=response.json()
        return weather
    else:
        return "Failure" 


load_dotenv()

st.title("Weather By Click")
st.subheader("Get accurate weather info of your desired location with explanation")

user_input=st.chat_input("Enter a city")

if user_input:
    result=get_weather(user_input)

    if result != "Failure" :
        st.write(user_input)

        st.write("Temperature : ",result['main']['temp']," °C")
        st.write("Humidity :",result['main']['humidity']," %")
        st.write("Wind Speed :",result['wind']['speed']," m/s")

        llm=init_chat_model(
            model="openai/gpt-oss-120b",
            model_provider="openai",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")
        )

        llm_input=f"""
        Question={result}
        Instructions=Explain the given weather data in simple English.
        Do not include metadata, tokens, JSON, IDs, or extra information.
        Use plain sentences only, no symbols or special characters.
        add bullet points where neccessary
        give info about the stats of what should be done in such conditions
        If unable to answer, output exactly: Error

        """

        if user_input:
            reply=llm.invoke(llm_input)
            st.success(f"Explanation : {reply.content}")

    else:
        st.error("Failure!! Enter a valid city name")

