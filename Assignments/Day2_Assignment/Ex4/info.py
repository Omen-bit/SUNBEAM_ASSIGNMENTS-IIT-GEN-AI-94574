import requests
import os

Api_key=os.getenv("WEATHER_API")

base_url=f"https://api.openweathermap.org/data/2.5/weather"

def weather_info(city_name):
    url=f"{base_url}?q={city_name}&appid={Api_key}&units=metric"
    responce=requests.get(url)

    if responce.status_code == 200:
        weather_of_city=responce.json()
        return weather_of_city

    else:
        print("Failed to retrieve data")