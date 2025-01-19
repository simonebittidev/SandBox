from datetime import datetime, timedelta
import getpass
import os

from typing import Annotated

from TomorrowNews.tools.getimage import get_image_by_text
from TomorrowNews.tools.getnews import get_todays_news_feed
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import InjectedState, create_react_agent

from langchain_openai import AzureChatOpenAI

if "AZURE_OPENAI_API_KEY" not in os.environ:
    raise Exception("No AZURE_OPENAI_API_KEY found in environment!")

if "AZURE_OPENAI_ENDPOINT" not in os.environ:
    raise Exception("No AZURE_OPENAI_ENDPOINT found in environment!")


newstool = get_todays_news_feed
imagetool = get_image_by_text

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",  # or your deployment
    api_version="2024-02-15-preview",  # or your api version
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

def journalist(
        state: Annotated[dict, InjectedState]
):
    system_prompt = (
        f"""
        Based on the Editor's analysis, develop in-depth stories and headlines for the "Tomorrow News" edition.
        Focus on predicting plausible future events as a result of today’s news.
        Cover diverse topics such as geopolitics, environment, health, and culture.
        Each story should be detailed enough to fill the column space, resembling a genuine newspaper article in length and depth. 
        Ensure that your writing is engaging, informative, and reflects the nuances of future predictions.
        """
    )
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    ai_msg = llm.invoke(messages)
    return ai_msg.content


def photographer(
    state: Annotated[dict, InjectedState]
):
    system_prompt = (
        """
Role: Expert Newspaper Photographer
Task: Use the image generation tool to create realistic and visually compelling photos that align with the newspaper headlines.
Instructions:
Think Like a Newspaper Photographer: Approach each image as if you're capturing a real-world scene for a major publication. Consider the context, mood, and details that would make the photo believable and engaging.
Provide Detailed Descriptions: Describe each photo thoroughly, including the setting, subjects, emotions, lighting, and any other elements that contribute to the realism and relevance of the image.
Focus on Realism: Ensure that the images are as realistic as possible. Avoid abstract or overly artistic interpretations unless explicitly required by the headline.
Content Filtering Awareness: Be mindful of the image tool's content filtering. Aim to create images that are appropriate and unlikely to be filtered. If an image is rejected due to filtering, promptly revise the description and try again to ensure a successful result.
Iterate as Needed: If content filtering issues arise, adjust the photo description to avoid sensitive or restricted content and retry until an acceptable image is generated.
        """
    )
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    ai_msg = llm.invoke(messages)
    return ai_msg.content


def html_developer(
        state: Annotated[dict, InjectedState]
):
    system_prompt = (
        """
After receiving the content from the Editor, your responsibility is to design a professional HTML layout for "Tomorrow News." The layout should include:
A clear title "Tomorrow News."
A two-column format with a wide central column for the main content.
Visually striking headlines and a prominent main headline.
Well-integrated images provided by the Photographer.
Ensure readability with appropriate fonts, contrast, and a cohesive color scheme.
Prioritize responsiveness so the layout adapts well to both desktop and mobile views.
The final output must be pure HTML, structured for seamless browser rendering.

        """
    )
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    ai_msg = llm.invoke(messages)
    return ai_msg.content


def editor(
    state: Annotated[dict, InjectedState]
):
    timestamp = datetime.utcnow()
    next_day = timestamp + timedelta(days=1)
    system_prompt = (
        f"""
You are the Editor, the central figure in producing the next day's edition of "Tomorrow News" (dated {next_day.strftime('%Y-%m-%d')}), starting from today's newspaper ({timestamp.strftime('%Y-%m-%d')}). 
Your role involves analyzing current news, predicting future events, and orchestrating the creation of content and design. You will:
Analyze today’s news (using tool) to forecast future events.
Delegate tasks to the appropriate agents—Journalist, Photographer, and HTML Developer—ensuring a smooth workflow.
Review the outputs at each stage to maintain quality and coherence.
After your analysis:
Assign the Journalist to create imaginative and plausible headlines and stories.
Once the stories are ready, pass them to the Photographer to generate realistic images that complement the content.
Finally, direct the HTML Developer to integrate the content and images into a professional, responsive HTML layout.
Your goal: Create a cohesive, compelling edition of "Tomorrow News" that provides a realistic glimpse into the future across various domains like politics, economy, and technology.
The final output must be pure HTML!
        """
    )
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    ai_msg = llm.invoke(messages)
    return ai_msg.content

tools = [newstool, imagetool, journalist, photographer, html_developer]

timestamp = datetime.utcnow()
next_day = timestamp + timedelta(days=1)
system_prompt = f"""
You are the Editor, the central figure in producing the next day's edition of "Tomorrow News" (dated {next_day.strftime('%Y-%m-%d')}), starting from today's newspaper ({timestamp.strftime('%Y-%m-%d')}). 
Your role involves analyzing current news, predicting future events, and orchestrating the creation of content and design. You will:
Analyze today’s news (using tool) to forecast future events.
Delegate tasks to the appropriate agents—Journalist, Photographer, and HTML Developer—ensuring a smooth workflow.
Review the outputs at each stage to maintain quality and coherence.
After your analysis:
Assign the Journalist to create imaginative and plausible headlines and stories.
Once the stories are ready, pass them to the Photographer to generate realistic images that complement the content.
Finally, direct the HTML Developer to integrate the content and images into a professional, responsive HTML layout.
Your goal: Create a cohesive, compelling edition of "Tomorrow News" that provides a realistic glimpse into the future across various domains like politics, economy, and technology.
The final output must be pure HTML!
"""

supervisor = create_react_agent(llm, tools, state_modifier=system_prompt)

supervisor.get_graph().draw_mermaid_png(output_file_path="TomorrowNews/supervisor.png")