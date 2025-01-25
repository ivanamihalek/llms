import os
import google.generativeai as genai
from google.api_core import client_options as client_option_lib

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

google_api_key  = os.getenv('GOOGLE_API_KEY')
print(google_api_key)

def blah():
    genai.configure(
        api_key=google_api_key,
        transport="rest",
        client_options=client_option_lib.ClientOptions(api_endpoint=os.getenv("GOOGLE_API_BASE"))
    )
    # there are 36 models - too many
    print(len(list(genai.list_models())))

    # can try "geberateText"
    content_models = list(filter(lambda m: "generateContent" in m.supported_generation_methods, genai.list_models()))
    for m in content_models:
        print(m.name)
        print(m.description)
        print(m.supported_generation_methods)
        print()

    print(len(content_models))
    model_bison = content_models[0]
    print(model_bison)


# helper fn for the API
def generate_text(prompt, model, temperature=0.0):
    return model.generate_content(prompt, generation_config={"temperature": temperature})


def main():
    genai.configure(
        api_key="AIzaSyD7gUzRDfVrmf2GAHapW81SDgg0Qft636c",
        transport="rest",
        client_options=client_option_lib.ClientOptions(api_endpoint=os.getenv("GOOGLE_API_BASE"))
    )
    model_flash = genai.GenerativeModel(model_name='gemini-1.5-flash')
    # prompt = "Show me how to iterate over a list in python."
    # completion = generate_text(prompt=prompt, model=model_flash)
    # print(completion.text)

    # note that "write" is less verbose
    # prompt = "Write code to iterate over a list in python."
    # completion = generate_text(prompt=prompt, model=model_flash)
    # print(completion.text)

    # note that "write" is less verbose
    prompt = """Write code to iterate over a list in Rust, Python, R, and Java. 
            What are the advantages of each language for this task?"""
    completion = generate_text(prompt=prompt, model=model_flash)
    print(completion.text)

if __name__ == "__main__":
    main()
