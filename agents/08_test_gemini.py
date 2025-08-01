#!/usr/bin/env python3
# rate limits: https://ai.google.dev/gemini-api/docs/rate-limits#free-tier
import os
from dotenv import load_dotenv
from google import genai

def main():
    # Load environment variables, including your API key
    load_dotenv()
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_GENAI_API_KEY not found in environment")
        return

    # Instantiate the Gemini client (API key read automatically from GOOGLE_API_KEY or GEMINI_API_KEY)
    client = genai.Client(api_key=api_key)

    try:
        # Simple prompt request to generate content from the Gemini model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Explain how AI works in a few words"
        )

        # Print out the generated text response
        print("Response from Gemini model:")
        print(response.text)

    except Exception as e:
        print(f"Failed to generate content: {e}")

if __name__ == "__main__":
    main()
