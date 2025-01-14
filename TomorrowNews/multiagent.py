import getpass
import os
from datetime import datetime, timedelta
from typing import Annotated
from typing_extensions import Literal
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.types import Command
from TomorrowNews.tools.getimage import get_image_by_text
from TomorrowNews.tools.getnews import get_todays_news_feed
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict
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
imagetool = get_image_by_text
tools = [newstool, imagetool]

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

@tool
def transfer_to_HTML_expert():
    """Transfer to HTML expert"""
    return

@tool
def transfer_to_photographer():
    """Transfer to photographer"""
    return

@tool
def transfer_to_editor():
    """Transfer to editor"""
    return

@tool
def transfer_to_Journalist():
    """Transfer to Journalist"""
    return

def Journalist(
    state: State,
) -> Command[Literal["hotel_advisor", "__end__"]]:
    system_prompt = (
        f"""
        Using today’s ({datetime.now().strftime('%Y-%m-%d')}) actual newspaper as a foundation, \
        apply reasoning and analysis to predict future events. \
        Create the next day’s ({(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')}) edition of 'Tomorrow News,' \
        complete with imaginative yet plausible headlines and stories. \
        Avoid simply continuing or expanding on today’s news—instead, \
        focus on predicting the next events or surprising developments \
        that could arise as consequences of current happenings or emerge unexpectedly. \
        Make it feel like a genuine glimpse into the future!\
        """
    )
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    ai_msg = llm_with_tools.bind_tools([transfer_to_photographer]).invoke(messages)
    # If there are tool calls, the LLM needs to hand off to another agent
    if len(ai_msg.tool_calls) > 0:
        tool_call_id = ai_msg.tool_calls[-1]["id"]
        # NOTE: it's important to insert a tool message here because LLM providers are expecting
        # all AI messages to be followed by a corresponding tool result message
        tool_msg = {
            "role": "tool",
            "content": "Successfully transferred",
            "tool_call_id": tool_call_id,
        }
        return Command(goto="hotel_advisor", update={"messages": [ai_msg, tool_msg]})

    # If the expert has an answer, return it directly to the user
    return {"messages": [ai_msg]}


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