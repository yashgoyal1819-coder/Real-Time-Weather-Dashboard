import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

API_KEY = ""

st.set_page_config(
    page_title="Real-Time Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st_autorefresh(interval=5000, key="weather_refresh")

st.title("🌤️ Real-Time Weather Analytics Dashboard")
st.write("Live weather data using OpenWeatherMap API")

city = st.text_input("Enter City Name", "Delhi")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

if st.button("Get Weather") or city:
    data = get_weather(city)

    if data.get("cod") == 200:
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        weather = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        visibility = data["visibility"] / 1000

        st.subheader(f"📍 Weather in {data['name']}, {data['sys']['country']}")

        col1, col2, col3 = st.columns(3)

        col1.metric("🌡️ Temperature", f"{temp} °C")
        col2.metric("🥵 Feels Like", f"{feels_like} °C")
        col3.metric("💧 Humidity", f"{humidity}%")

        col4, col5, col6 = st.columns(3)

        col4.metric("🌬️ Wind Speed", f"{wind_speed} m/s")
        col5.metric("🔽 Pressure", f"{pressure} hPa")
        col6.metric("👁️ Visibility", f"{visibility} km")

        st.info(f"Current Weather: **{weather}** - {description.title()}")

        if temp >= 40:
            st.error("🔥 Heat Alert: Temperature is very high!")
        elif temp <= 10:
            st.warning("❄️ Cold Alert: Temperature is very low!")
        else:
            st.success("✅ Weather condition looks normal.")

        st.caption(f"Last updated: {datetime.now().strftime('%d %B %Y, %I:%M:%S %p')}")
        st.caption("Dashboard auto-refreshes every 5 seconds.")

    else:
        st.error("City not found or API error. Please check city name/API key.")