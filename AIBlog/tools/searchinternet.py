from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools import DuckDuckGoSearchRun

searchinternettool = DuckDuckGoSearchResults(output_format="json")
askinternettool = DuckDuckGoSearchRun()