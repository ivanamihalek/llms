#! /usr/bin/env python

import os
from os import PathLike

import google.generativeai as genai
from google.api_core import client_options as client_option_lib


from dotenv import load_dotenv, find_dotenv


# helper fn for the API
def generate_text(prompt, model, temperature=0.0):
    return model.generate_content(prompt, generation_config={"temperature": temperature})


def svg_manip(model):

    prompt_template = """
    You are an expert on Inkscape svg format, and know how to parse xml using python.
    Please write a readable and concise python code to change 
    * stroke-width to 3 in  each polyline and in each circle element style string
    * r in each circle element to 5
    in an input svg file similar to the following:
```xml
    {question}
```
    Further instructions:
    * Take the path to the input and output files as an input from the command line.
    * Include the shebang line '#! /usr/bin/env python3'
    * Make sure that the script has a main() method
    * Keep in mind that string.replace() method in python cannot do pattern matching - use replacements like
```
        style = element.get("style", "")
        # Use regex to replace stroke-width
        new_style = re.sub(pattern1, pattern2, style)

        if new_style != style:
            element.set("style", new_style)
        else:
            # If no replacement occurred, append the style
            element.set("style", style + ";stroke-width:3")
    
```
    * Use xml.dom.minidom to format the xml output.
    
    """
    path = "/home/ivana/scratch/fig4_ivana.svg"
    with open(path, 'r') as file:
        question = file.read()
    prompt = prompt_template.format(question=question)

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
    svg_manip(model_flash)

if __name__ == "__main__":
    main()
