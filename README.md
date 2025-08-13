# 🌤️ Weather Bot with LangGraph + Gemini

A conversational weather assistant built with **FastAPI**, **LangGraph**, **Google Gemini**, and **OpenWeather API**.  
It can extract city names from user queries, fetch live weather data, and return friendly, conversational responses.

---

## 🚀 Features
- **Conversational AI** using Google Gemini (`langchain_google_genai`)
- **City extraction** from natural language input
- **Live weather data** via OpenWeather API
- **Tool integration** using LangGraph's `ToolNode`
- **FastAPI backend** for easy API deployment
- **.env configuration** for secrets

---

## 📂 Project Structure

```plaintext
WeatherBOT/
├── app.log                     # Log file
├── graph_flow.py               # LangGraph flow with LLM + tool integration
├── graph.ipynb                  # Jupyter notebook for experiments
├── logger.py                   # Logger configuration
├── main.py                     # FastAPI entry point
├── nodes/                      # Nodes for LangGraph
│   ├── fetch_weather.py        # Node that fetches weather data
│   └── __pycache__/            # Python cache files
├── __pycache__/                # Cache files for main modules
├── README.md                   # Project overview
├── DOCUMENTATION.md            # Project documentation
├── requirements.txt            # Dependencies
├── services/                   # Service layer
│   ├── llm_service.py          # Gemini API integration for city extraction & response
│   ├── __pycache__/            # Cache files
│   └── weather_service.py      # OpenWeather API integration
└── state.py                    # State definitions (Pydantic models)
