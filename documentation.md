# 🌦 Weather Bot — Full Developer Documentation

## 1. Project Overview
The **Weather Bot** is a Python-based **FastAPI** service that:

- Accepts a **natural language** query about the weather
- Uses a **Large Language Model (LLM)** to extract a city name
- Retrieves **live weather data** from the **OpenWeatherMap API**
- Uses the **LLM again** to create a natural, friendly response
- Orchestrates these steps using a **LangGraph** state machine

---

## 2. Module-by-Module API Documentation

### **`state.py`**

#### **class LocationRequest**
**Purpose:** Represents the POST body for `/weather` endpoint.

| Name        | Type | Required | Description |
|-------------|------|----------|-------------|
| `user_input`| str  | ✅        | Full sentence from the user (e.g., `"What's the weather in Paris?"`) |

---

#### **class WeatherBotState**
**Purpose:** Tracks the bot’s state across graph execution.

| Name              | Type           | Description |
|-------------------|----------------|-------------|
| `user_input`      | str            | Raw text from the user |
| `location`        | Optional[str]  | Extracted city name |
| `weather_data`    | Optional[dict] | Raw weather data from API |
| `response_message`| Optional[str]  | Final response to return |

---

### **`logger.py`**

#### **function `setup_logger()`**
**Description:**  
Initializes logging for the entire app.

**Returns:**  
`logging.Logger` — Logger instance named `"weather-bot"`

---

### **`graph_flow.py`**

#### **function `create_graph()`**
**Description:**  
Builds and compiles the LangGraph workflow.

**Workflow Nodes:**
1. `"extract_city"` — Extracts city from text  
2. `"fetch_weather"` — Retrieves live weather  
3. `"format_weather"` — Generates response  

**Returns:**  
`RunnableGraph` — Executable LangGraph instance

---

### **`nodes/extract_city.py`**

#### **function `extract_city(state: WeatherBotState) -> WeatherBotState`**
**Description:**  
Uses `services.llm_service.extract_city_from_text` to detect a city name in `state.user_input`.

| Parameter | Type             | Description |
|-----------|------------------|-------------|
| `state`   | WeatherBotState  | Current bot state |

**Returns:**  
`WeatherBotState` — Updated state with:
- `location` set if city found  
- `response_message` error if city not found  

---

### **`nodes/fetch_weather.py`**

#### **function `fetch_weather(state: WeatherBotState) -> WeatherBotState`**
**Description:**  
Fetches weather data from OpenWeatherMap for `state.location`.

**Environment Variables:**
- `OPENWEATHER_API_KEY` (must be set in `.env`)

| Parameter | Type             | Description |
|-----------|------------------|-------------|
| `state`   | WeatherBotState  | Current bot state |

**Returns:**  
`WeatherBotState` — Updated state with:
- `weather_data` populated if successful  
- `weather_data = None` if API key missing or error  

---

### **`nodes/format_weather.py`**

#### **function `format_weather(state: WeatherBotState) -> WeatherBotState`**
**Description:**  
Uses `services.llm_service.generate_response_from_weather_data` to produce a conversational weather summary.

| Parameter | Type             | Description |
|-----------|------------------|-------------|
| `state`   | WeatherBotState  | Current bot state |

**Returns:**  
`WeatherBotState` — Updated state with:
- `response_message` set to a friendly weather reply  

---

### **`services/llm_service.py`**

#### **function `extract_city_from_text(text: str) -> Optional[str]`**
**Description:**  
Prompts an LLM to extract a single city name from text.  
Returns `None` if no city found.

| Parameter | Type | Description |
|-----------|------|-------------|
| `text`    | str  | User's query |

**Returns:**  
`Optional[str]` — City name or `None`

---

#### **function `generate_response_from_weather_data(weather_data: dict, user_input: str) -> str`**
**Description:**  
Uses an LLM to craft a friendly, conversational weather response.

| Parameter     | Type | Description |
|---------------|------|-------------|
| `weather_data`| dict | Raw weather data |
| `user_input`  | str  | Original query |

**Returns:**  
`str` — Natural language reply

---

### **`services/weather_service.py`**

#### **function `get_weather_live(location: str, api_key: str) -> Optional[dict]`**
**Description:**  
Queries OpenWeatherMap for current weather in the given city.

| Parameter | Type | Description |
|-----------|------|-------------|
| `location`| str  | City name |
| `api_key` | str  | OpenWeather API key |

**Returns:**  
`Optional[dict]` — Parsed weather JSON or `None`

---

### **`main.py`**

#### **POST `/weather`**
**Description:**  
Main API endpoint for fetching weather.

**Request Body:**  
`LocationRequest` — `{ "user_input": "<query>" }`

**Response:**
```json
{
  "response_message": "<final friendly weather reply>"
}
