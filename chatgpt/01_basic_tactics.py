#! /usr/bin/env python3
from openai import OpenAI


import os
from pprint import pprint
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def main():
    # print(openai.api_key)
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    # for model in client.models.list():
    #     print(model)
    # exit()
    response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What's the difference between DNA and RNA?"}
        ])

    pprint(response)
    # print(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    main()


