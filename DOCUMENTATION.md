# 📚 Weather Bot – Technical Documentation

## 1. Overview
Weather Bot is an AI-powered weather assistant built using **FastAPI**, **LangGraph**, **Google Gemini**, and the **OpenWeather API**.  
It can:
- Understand user queries in natural language.
- Extract the city name.
- Fetch live weather information.
- Generate friendly responses.

---

## 2. Architecture

### 2.1 High-Level Flow
1. **User Input** → Sent via `/weather` API endpoint.
2. **LangGraph LLM Node** → Uses Gemini to decide:
   - Extract city.
   - Call weather API tool if needed.
3. **Tool Node** → Calls `get_weather_live_tool()` from `weather_service.py`.
4. **Weather API Response** → Returned to LLM.
5. **LLM Generates Reply** → Sent back to user.

---

## 3. Components

### 3.1 `main.py`
- FastAPI app entry point.
- `/weather` POST endpoint.
- Calls the LangGraph pipeline.

### 3.2 `graph_flow.py`
- Defines the **LangGraph StateGraph**:
  - **LLM Node** (`call_llm`): Uses Gemini + bound tools.
  - **Tool Node**: Runs OpenWeather API request.
  - **Conditional Edges**: Decide whether to call tools or end.
- Uses `GEMINI_API_KEY` from `.env`.

### 3.3 `nodes/fetch_weather.py`
- Fetches weather from `weather_service.py` using `OPENWEATHER_API_KEY`.
- Updates the conversation state with results.

### 3.4 `services/weather_service.py`
- Implements `get_weather_live_tool()` for LangChain tool use.
- Calls **OpenWeather API**.
- Returns JSON weather data.

### 3.5 `services/llm_service.py`
- Uses Gemini for:
  - **City extraction** from text.
  - **Response generation** from weather data.
- Uses `PromptTemplate` for flexible prompt creation.

### 3.6 `state.py`
- Defines conversation state using **Pydantic**.
- Holds a list of messages (`BaseMessage` objects).

### 3.7 `logger.py`
- Configures logging to both `app.log` and console.

---

## 4. Environment Variables

| Variable              | Description                  |
|-----------------------|------------------------------|
| `OPENWEATHER_API_KEY` | OpenWeather API key           |
| `GEMINI_API_KEY`      | Google Gemini API key         |

Create a `.env` file in the root directory:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
GEMINI_API_KEY=your_gemini_api_key
