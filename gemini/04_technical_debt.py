#! /usr/bin/env python

import os
from os import PathLike

import google.generativeai as genai
from google.api_core import client_options as client_option_lib

from dotenv import load_dotenv, find_dotenv


# helper fn for the API
def generate_text(prompt, model, temperature=0.0):
    return model.generate_content(prompt, generation_config={"temperature": temperature})


def explain_code(model):

    prompt_template = """
    Can you please explain how this code works?
```python
    {question}
```
    Use a lot of detail and make it as clear as possible.
    """
    path = "/home/ivana/projects/ABCA4-faf/classes/faf_analysis.py"
    with open(path, 'r') as file:
        question = file.read()
    prompt = prompt_template.format(question=question)
    print(prompt)
    completion = generate_text(prompt, model)
    print(completion.text)


def document_code(model):

    prompt_template_0 = """
Please write technical documentation for this code and \n
make it easy for a novice developer to understand:
```python
    {question}
```
Output the results in markdown,
    """
    prompt_template = """
Please document this code:
```python
    {question}
```
Use Google docstrings formatting
    """
    path = "/home/ivana/projects/ABCA4-faf/classes/faf_analysis.py"
    with open(path, 'r') as file:
        question = file.read()
    prompt = prompt_template.format(question=question)
    print(prompt)
    completion = generate_text(prompt, model)
    print(completion.text)



def main():

    load_dotenv(find_dotenv())

    google_api_key  = os.getenv('GOOGLE_API_KEY')
    print(google_api_key)

     genai.configure(
        api_key=google_api_key,
        transport="rest",
        client_options=client_option_lib.ClientOptions(api_endpoint=os.getenv("GOOGLE_API_BASE"))
    )
    model_flash = genai.GenerativeModel(model_name='gemini-1.5-flash')
    # explain_code(model_flash)
    document_code(model_flash)

if __name__ == "__main__":
    main()
