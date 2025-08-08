#!/usr/bin/env python3
import os
from pprint import pprint

from dotenv import load_dotenv
from tavily import TavilyClient

def main():
    load_dotenv()
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    tavily_client = TavilyClient(api_key=tavily_api_key)
    response = tavily_client.search("Who is Luka Modric?")
    # response = tavily_client.search("What is the weather like in sf?")
    pprint(response)


if __name__ == "__main__":
    main()
