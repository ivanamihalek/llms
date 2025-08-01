#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from google import genai
from readable_number import ReadableNumber

def main():
    # Load environment variables from .env file
    load_dotenv()

    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_GENAI_API_KEY not found in environment")
        return

    # Instantiate the Gemini API client with the API key
    client = genai.Client(api_key=api_key)
    rn = ReadableNumber(precision=2, digit_group_size=3)
    try:
        # List available models
        response = client.models.list(config={'page_size': 5})
        while page:=response.next_page():
            for model in page:
                print(model.name,
                     rn.of(model.input_token_limit),
                      rn.of(model.output_token_limit))

    except Exception as e:
        print(f"Failed to retrieve models: {e}")


if __name__ == "__main__":
    main()
