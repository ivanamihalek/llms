#! /usr/bin/env python

import os
import google.generativeai as genai
from google.api_core import client_options as client_option_lib

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

google_api_key  = os.getenv('GOOGLE_API_KEY')
print(google_api_key)


# helper fn for the API
def generate_text(prompt, model, temperature=0.0):
    return model.generate_content(prompt, generation_config={"temperature": temperature})


def main():
    genai.configure(
        api_key=google_api_key,
        transport="rest",
        client_options=client_option_lib.ClientOptions(api_endpoint=os.getenv("GOOGLE_API_BASE"))
    )
    model_flash = genai.GenerativeModel(model_name='gemini-1.5-flash')

    prompt_template = """
        {priming}
        
        {question}
        
        {decorator}
    
        Your solution:
    """
    # priming = "You are an expert at writing clear concise Python code."
    priming = "You are a professional Python developer obsessed with code robustness and type safety."
    question = "Create a doubly linked list. Prove unit test for each class and function you define, except the main."
    decorator = "Insert comments for each line of code. Make sure your code has a main function"
    prompt =  prompt_template.format(priming=priming, question=question, decorator=decorator)
    print(prompt)
    completion = generate_text(prompt, model_flash)
    print(completion.text)



if __name__ == "__main__":
    main()
