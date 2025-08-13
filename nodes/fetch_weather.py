# nodes/fetch_weather.py
# The node that fetches weather data by calling the weather service.

from state import WeatherBotState
from services.weather_service import get_weather_live
from logger import logger
import os
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from a .env file
load_dotenv() 

# Load the API key from the environment
api_key = os.getenv("OPENWEATHER_API_KEY")
if not api_key:
    logger.error("OPENWEATHER_API_KEY not found in environment variables.")

def fetch_weather(state: WeatherBotState) -> WeatherBotState:
    """
    Fetches live weather data for the specified location using the weather service.
    """
    # New code (correct)
    location = state.location
    logger.info(f"Entering fetch_weather node. Fetching data for {location}.")

    # Only proceed if the API key is available
    if not api_key:
        logger.error("API key is missing, cannot fetch live weather.")
        return {**state, "weather_data": None}

    weather_data = get_weather_live(location, api_key)

    if weather_data:
        logger.info(f"Data found for {location}.")
        # Correct way to update the Pydantic model
        state.weather_data = weather_data
        return state
    else:
        logger.warning(f"No data for {location}.")
        # Correct way to update the Pydantic model
        state.weather_data = None
        return state