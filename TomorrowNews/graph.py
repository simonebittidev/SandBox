import getpass
import os

from typing import Annotated

from TomorrowNews.getnews import get_todays_news_feed
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_openai import AzureChatOpenAI

if "AZURE_OPENAI_API_KEY" not in os.environ:
    raise Exception("No AZURE_OPENAI_API_KEY found in environment!")

if "AZURE_OPENAI_ENDPOINT" not in os.environ:
    raise Exception("No AZURE_OPENAI_ENDPOINT found in environment!")

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

newstool = get_todays_news_feed
tools = [newstool]

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",  # or your deployment
    api_version="2024-02-15-preview",  # or your api version
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

llm_with_tools = llm.bind_tools(tools)

def agent(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("agent", agent)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "agent")
graph_builder.set_entry_point("agent")
news_graph = graph_builder.compile()