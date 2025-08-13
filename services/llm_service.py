# services/llm_service.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from logger import logger
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv() 


# Initialize the LLM with your Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables.")
    # Consider raising an error here to stop the application immediately
    # raise ValueError("GEMINI_API_KEY not set")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", api_key=api_key)

def extract_city_from_text(text: str) -> str:
    """
    Uses an LLM to extract a single city name from a given text.
    """
    prompt_template = PromptTemplate.from_template(
        "You are a helpful assistant that extracts a single city name from a user query.\n"
        "If no city is mentioned, return the word 'None'.\n"
        "Query: {query}\n"
        "City:"
    )
    chain = prompt_template | llm
    
    try:
        response = chain.invoke({"query": text})
        city_name = response.content.strip()
        
        if city_name.lower() == 'none':
            return None
        return city_name
    except Exception as e:
        logger.error(f"LLM city extraction failed: {e}")
        return None

def generate_response_from_weather_data(weather_data: dict, user_input: str) -> str:
    """
    Uses an LLM to create a friendly, conversational response.
    """
    prompt_template = PromptTemplate.from_template(
        "You are a weather bot. The user's query was: '{user_input}'.\n"
        "The weather data is: {weather_data}. "
        "Create a friendly and conversational response that answers the user's question. "
        "Do not mention that you used the provided weather data. "
        "Keep the response concise and natural."
    )
    chain = prompt_template | llm
    
    try:
        response = chain.invoke({"weather_data": str(weather_data), "user_input": user_input})
        return response.content
    except Exception as e:
        logger.error(f"LLM response generation failed: {e}")
        return "Sorry, I am unable to generate a response at this time."