# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from logger import logger
from graph_flow import create_graph
from langchain_core.messages import HumanMessage

app = FastAPI()
graph = create_graph()  # Your LangChain StateGraph or Chain

class WeatherRequest(BaseModel):
    city: str

@app.on_event("startup")
async def startup_event():
    logger.info("App started")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("App shutting down")

@app.post("/weather")
async def get_weather_endpoint(weather_request: WeatherRequest):
    try:
        # Build the input for your LangChain flow
        user_message = f"weather in {weather_request.city}"
        logger.info(f"Received request: {user_message}")

        inputs = {
            "messages": [HumanMessage(content=user_message)]
        }

        # Invoke your graph — consider switching to await graph.ainvoke(...) if async
        final_state = graph.invoke(inputs)
        logger.debug(f"Final state from graph: {final_state}")

        # Extract the last message safely
        messages = final_state.get("messages")
        if not messages or not hasattr(messages[-1], "content"):
            logger.error("Graph output did not contain expected 'messages' list")
            raise HTTPException(status_code=500, detail="Unexpected output from AI")

        final_response_message = messages[-1].content

        return JSONResponse(content={"weather": final_response_message})

    except HTTPException:
        raise  # Re-raise defined HTTP errors
    except Exception as e:
        logger.error(f"Exception in /weather endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
