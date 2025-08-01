#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment")
        return

    # Instantiate the client with the API key
    client = OpenAI(api_key=api_key)

    try:
        # List available models using new API style
        response = client.models.list()
        models = response.data

        print("Available OpenAI Models:")
        for model in models:
            print(f"- {model.id}")

    except Exception as e:
        print(f"Failed to retrieve models: {e}")

if __name__ == "__main__":
    main()
