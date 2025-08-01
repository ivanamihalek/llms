#! /usr/bin/env python3
import openai
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')
print(openai.api_key)
