import xmltodict
import requests
import json
from langchain_core.tools import tool
from pydantic import BaseModel

RSS_URL = "https://feeds.bbci.co.uk/news/rss.xml"

def getRSS(url: str) -> dict:
    response = requests.get(url)
    return xmltodict.parse(response.content)

def saveRSS(filepath: str, data: dict) -> None:
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

@tool
def get_todays_news_feed() -> list[dict]:
    """get todays news as a list of dicts containing title and description"""
    data = getRSS(RSS_URL)
    result = []
    for item in data['rss']['channel']['item']:
        result.append({"title": item["title"], "description": item["description"]})
    return result