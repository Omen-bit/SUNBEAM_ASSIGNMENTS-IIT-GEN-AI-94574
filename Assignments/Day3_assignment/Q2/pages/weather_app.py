import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("WEATHER_API")

base_url=f"https://api.openweathermap.org/data/2.5/weather"

def weather_info(city):
    url=f"{base_url}?appid={API_KEY}&q={city}&units=metric"
    responce=requests.get(url)

    if responce.status_code == 200:
        weather=responce.json()
        return weather
    else:
        st.write("Failure!! Enter valid city")


city=st.text_input("Enter a city name to display weather forecast : ")

if st.button("submit") or city:
    weather_data=weather_info(city)
    if weather_data:
        st.write("Temperature : ",weather_data['main']['temp']," °C")
        st.write("Humidity :",weather_data['main']['humidity']," %")
        st.write("Wind Speed :",weather_data['wind']['speed']," m/s")

if st.button("Logout"):
    st.toast("Thank You")
    st.switch_page("Q2.py")






