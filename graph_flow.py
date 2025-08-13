# graph_flow.py
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from logger import logger
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from services.weather_service import get_weather_live_tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os

from typing import List, TypedDict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]

# Set up the LLM with the correct model and bind the tool
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", api_key=os.getenv("GEMINI_API_KEY"))
tools = [get_weather_live_tool]
llm_with_tools = llm.bind_tools(tools)

# Define the nodes and their logic
def call_llm(state: AgentState):
    """
    Invokes the LLM with the current message history.
    """
    messages = state["messages"]

    if not messages:
        raise ValueError("Cannot call LLM with an empty message list.")

    safe_messages = []
    for m in messages:
        content = getattr(m, "content", None)

        if isinstance(m, ToolMessage):
            # Tool output - stringify it
            safe_messages.append(
                HumanMessage(content=f"Tool output: {m.content or str(m)}")
            )
        elif not content:
            # AI tool calls or blank messages - give placeholder text
            safe_messages.append(
                AIMessage(content="(No prior message content, continuing conversation.)")
            )
        else:
            safe_messages.append(m)

    response = llm_with_tools.invoke(safe_messages)

    return {"messages": messages + [response]}

# The ToolNode handles tool execution
tool_node = ToolNode(tools)

# Define the conditional logic
def should_continue(state: AgentState):
    """
    Checks for a tool call and routes the graph.
    """
    last_message = state['messages'][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return END

def create_graph():
    logger.info("Creating LangGraph for agent with tools.")
    
    builder = StateGraph(AgentState)

    builder.add_node("llm", call_llm)
    builder.add_node("tools", tool_node)
    
    builder.set_entry_point("llm")
    
    builder.add_conditional_edges(
        "llm",
        should_continue,
        {"tools": "tools", END: END}
    )
    
    # CORRECT: Loop back to the LLM after the tool call
    builder.add_edge("tools", "llm")
    
    graph = builder.compile()
    logger.info("LangGraph agent compiled successfully.")
    
    return graph