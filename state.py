# state.py
from pydantic import BaseModel
from typing import Optional

class LocationRequest(BaseModel):
    """
    A simple Pydantic model for the API request body.
    We now expect a full sentence from the user, not just a city.
    """
    user_input: str

class WeatherBotState(BaseModel):
    """
    Represents the state of our weather bot.
    
    Attributes:
        user_input (str): The raw text from the user.
        location (Optional[str]): The city extracted from the user's input.
        weather_data (Optional[dict]): The raw weather data fetched.
        response_message (Optional[str]): The final formatted message to display.
    """
    user_input: str
    location: Optional[str] = None
    weather_data: Optional[dict] = None
    response_message: Optional[str] = None