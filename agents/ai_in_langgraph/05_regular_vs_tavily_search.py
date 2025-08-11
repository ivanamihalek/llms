#!/usr/bin/env python3
import os
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import re


from dotenv import load_dotenv
from tavily import TavilyClient
import json
from pygments import highlight, lexers, formatters

def tavily_search(question):
    load_dotenv()
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    tavily_client = TavilyClient(api_key=tavily_api_key)
    response = tavily_client.search(question, max_results=1)
    data = response["results"][0]["content"]
    # parse JSON
    parsed_json = json.loads(data.replace("'", '"'))

    # pretty print JSON with syntax highlighting
    formatted_json = json.dumps(parsed_json, indent=4)
    colorful_json = highlight(formatted_json,
                              lexers.JsonLexer(),
                              formatters.TerminalFormatter())

    print(colorful_json)

def scrape_weather_info(url):
    """Scrape content from the given URL"""
    if not url:
        return "Weather information could not be found."

    # fetch data
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Failed to retrieve the webpage."

    # parse result
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def regular_search(question):
    ddg = DDGS()
    try:
        results = ddg.text(question, max_results=1)
        results =  [i["href"] for i in results]
    except Exception as e:
        print(f"returning previous results due to exception reaching ddg.")
        results = [ # cover case where DDG rate limits due to high deeplearning.ai volume
            "https://weather.com/weather/today/l/USCA0987:1:US",
            "https://weather.com/weather/hourbyhour/l/54f9d8baac32496f6b5497b4bf7a277c3e2e6cc5625de69680e6169e7e38e9a8",
        ]

    for url in results:
        soup = scrape_weather_info(url)
        print(f"Website: {url}\n\n")
        print(str(soup.body)[:50000]) # limit long outputs

def main():
    city = "San Francisco"
    question =  f"""
    what is the current weather in {city}?
    Should I travel there today?
    "weather.com"
    """

    regular_search(question)

    # tavily_search(question)


if __name__ == "__main__":
    main()
