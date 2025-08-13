# main.py
from fastapi import FastAPI
from graph_flow import create_graph
from state import LocationRequest, WeatherBotState
from logger import logger

# Create a FastAPI app instance
app = FastAPI(title="Weather Bot API")

# Create the graph instance once on startup
graph = create_graph()

@app.post("/weather")
def get_weather_endpoint(request: LocationRequest):
    """
    API endpoint to get weather data for a given location.
    """
    logger.info(f"Received request: {request.user_input}")
    
    # Pass the user_input to the graph
    final_state = graph.invoke({"user_input": request.user_input})
    
    return {"response_message": final_state['response_message']}