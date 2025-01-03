import xmltodict
import requests
import json

RSS_URL = "https://feeds.bbci.co.uk/news/rss.xml"

def getRSS(url: str) -> dict:
    response = requests.get(url)
    return xmltodict.parse(response.content)

def saveRSS(filepath: str, data: dict) -> None:
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

data = getRSS(RSS_URL)

for item in data['rss']['channel']['item']:
    print(item['title'])
    print(item['description'])
    print(item['link'])
    print()