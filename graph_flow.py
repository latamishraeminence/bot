# graph_flow.py
# Defines the overall LangGraph structure, including nodes and edges.

from langgraph.graph import StateGraph, END
from state import WeatherBotState
from nodes.extract_city import extract_city
from nodes.fetch_weather import fetch_weather
from nodes.format_weather import format_weather
from logger import logger

def create_graph():
    """
    Creates and compiles the LangGraph for the weather bot.
    """
    logger.info("Creating LangGraph.")
    
    # Create a StateGraph instance.
    builder = StateGraph(WeatherBotState)

    # Add nodes to the graph.
    builder.add_node("extract_city", extract_city)
    builder.add_node("fetch_weather", fetch_weather)
    builder.add_node("format_weather", format_weather)

    # Define the edges (flow control).
    builder.set_entry_point("extract_city")
    builder.add_edge("extract_city", "fetch_weather")
    builder.add_edge("fetch_weather", "format_weather")
    builder.add_edge("format_weather", END)

    # Compile the graph into a runnable object.
    graph = builder.compile()
    logger.info("LangGraph compiled successfully.")
    
    return graph

if __name__ == "__main__":
    # Example of running the graph directly from this file.
    graph = create_graph()
    
    print("--- Running graph for London ---")
    final_state = graph.invoke({"location": "London"})
    print(f"\nFinal Response: {final_state['response_message']}")
