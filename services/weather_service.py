# services/weather_service.py
# This service file is responsible for all interactions with the
# OpenWeather API.

import requests
import os
from typing import Optional

def get_weather_live(location: str, api_key: str) -> Optional[dict]:
    """
    Fetches live weather data from the OpenWeatherMap API.

    Args:
        location (str): The city name to search for.
        api_key (str): The OpenWeatherMap API key.

    Returns:
        Optional[dict]: The weather data dictionary, or None if an error occurs.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"  # Get temperature in Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"City not found: {location}")
        else:
            print(f"HTTP Error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    
    return None