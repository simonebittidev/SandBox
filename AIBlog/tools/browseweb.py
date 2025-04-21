import typing
import asyncio
from playwright.async_api import async_playwright, Browser
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
# from langchain_community.tools.playwright.utils import (
#     create_async_playwright_browser,  
#     create_sync_playwright_browser
# )
import subprocess

subprocess.run(["playwright", "install"])

async def create_async_playwright_browser(
        headless: bool = True, args: typing.Optional[typing.List[str]] = None
) -> Browser:
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless, args=args)
    return browser

async def get_browsewebtools():
    async_browser = await create_async_playwright_browser()

    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    browsewebtools = toolkit.get_tools()
    return browsewebtools

# sync_browser = create_sync_playwright_browser()

# synctoolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
# syncbrowsewebtools = synctoolkit.get_tools()

