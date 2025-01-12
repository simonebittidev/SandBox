from langchain_core.tools import tool
# Note: DALL-E 3 requires version 1.0.0 of the openai-python library or later
import os
from openai import AzureOpenAI
import json

from TomorrowNews.azurestorage import save_photo_to_blob

client = AzureOpenAI(
    api_version="2024-02-01",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

@tool
def get_image_by_text(text: str) -> str:
    """get the url of an image created as the input text explains, the input text should describe well the expected output"""
    result = client.images.generate(
        model="dall-e-3", # the name of your DALL-E 3 deployment
        prompt=text,
        n=1
    )

    image_url = json.loads(result.model_dump_json())['data'][0]['url']
    blob_image_url = save_photo_to_blob(image_url)
    return blob_image_url
