# services/weather_service.py
import requests
import os
from typing import Optional
from langchain_core.tools import tool

from dotenv import load_dotenv
load_dotenv()

@tool
def get_weather_live_tool(location: str) -> str:
    """
    Fetches live weather data from the OpenWeatherMap API for a given location.
    
    Args:
        location (str): The city name to search for.
    
    Returns:
        str: The weather data as a JSON string, or a message indicating an error.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY is not set."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return f"HTTP Error: {err}. City not found."
    except Exception as err:
        return f"An unexpected error occurred: {err}"