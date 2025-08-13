# state.py
from pydantic import BaseModel
from typing import Optional, List
from langchain_core.messages import BaseMessage

class LocationRequest(BaseModel):
    """
    A simple Pydantic model for the API request body.
    """
    user_input: str

class AgentState(BaseModel):
    """
    Represents the state of our LangGraph agent.
    
    Attributes:
        messages (List[BaseMessage]): A list of all messages in the conversation.
    """
    messages: List[BaseMessage] = []