# nodes/extract_city.py
from state import WeatherBotState
from services.llm_service import extract_city_from_text
from logger import logger

def extract_city(state: WeatherBotState) -> WeatherBotState:
    """
    Extracts the city name from the user's input using an LLM.
    """
    logger.info(f"Entering extract_city node. User input: {state.user_input}")
    
    extracted_city = extract_city_from_text(state.user_input)
    
    if extracted_city:
        logger.info(f"Extracted city: {extracted_city}")
        state.location = extracted_city
    else:
        logger.warning("Could not extract a city from the user's input.")
        state.location = None
        state.response_message = "I'm sorry, I couldn't understand which city you were asking about."

    return state