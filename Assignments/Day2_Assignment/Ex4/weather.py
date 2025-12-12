from info import weather_info

city_name=input("Enter a city name to get weather data : ")
weather_data=weather_info(city_name)

if weather_data:
    print("City Name : ",weather_data['name'])
    print("Temperature : ",weather_data['main']['temp'],"°C")
    print("Pressure : ",weather_data['main']['pressure'],"hPa")
    print("Humidity :",weather_data['main']['humidity'],"%")


