# nodes/format_weather.py
from state import WeatherBotState
from services.llm_service import generate_response_from_weather_data
from logger import logger

def format_weather(state: WeatherBotState) -> WeatherBotState:
    """
    Formats the raw weather data into a human-readable response using an LLM.
    """
    weather_data = state.weather_data
    user_input = state.user_input
    location = state.location
    
    logger.info(f"Entering format_weather node. Formatting data for {location}.")

    if not weather_data:
        pass
    else:
        message = generate_response_from_weather_data(weather_data, user_input)
        state.response_message = message

    logger.info(f"Formatted message: {state.response_message}")
    return state