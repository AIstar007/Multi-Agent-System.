import requests
from google.adk.agents import Agent
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_at_location(city: str) -> dict:
    """
    Fetches current weather data for a given city.
    Args:
        city (str): City name (e.g., 'Cape Canaveral')
    Returns:
        dict: Weather status or error
    """
    if not API_KEY:
        return {"status": "error", "error_message": "Missing OpenWeatherMap API Key"}

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}"
            f"&appid={API_KEY}&units=metric"
        )
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        return {
            "status": "success",
            "report": {
                "temperature_celsius": temp,
                "weather_condition": weather,
                "wind_speed_mps": wind,
            },
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

weather_agent = Agent(
    name="weather_agent",
    model="gemini-1.5-flash",
    description="Provides current weather at a given location.",
    instruction="Return temperature, condition, and wind speed for a city.",
    tools=[get_weather_at_location],
)