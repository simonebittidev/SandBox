import asyncio
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import (
    create_async_playwright_browser,  
    create_sync_playwright_browser
)
import subprocess

subprocess.run(["playwright", "install"])

async_browser = create_async_playwright_browser()

toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
browsewebtools = toolkit.get_tools()

sync_browser = create_sync_playwright_browser()

synctoolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
syncbrowsewebtools = synctoolkit.get_tools()

