#!/usr/bin/env python3

# rate limits: https://ai.google.dev/gemini-api/docs/rate-limits#free-tier
import os
import re

from dotenv import load_dotenv
from google import genai
from openai import OpenAI

def hello_world(client):
    # response = client.models.generate_content(
    #     model="gemini-2.5-flash",
    #     contents="Hello World!"
    # )
    #
    # # Print out the generated text response
    # print("Response from Gemini model:")
    # print(response.text)
    # # Hello to you too, world! Or should I say, `print("Hello World!")`? 😉

    chat_completion = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role": "user", "content": "Hello world"}]
    )
    response = chat_completion.choices[0].message.content
    print("Response from Gemini model:")
    print(response.text)
    # How can I help you today? Are you learning to program, or just saying hello?

def calculate(what):
    return eval(what)

def average_dog_weight(name):
    if name in "Scottish Terrier":
        return "Scottish Terriers average 20 lbs"
    elif name in "Border Collie":
        return "a Border Collies average weight is 37 lbs"
    elif name in "Toy Poodle":
        return "a toy poodles average weight is 7 lbs"
    else:
        return "An average dog weights 50 lbs"

def get_known_actions():
    return {
        "calculate": calculate,
        "average_dog_weight": average_dog_weight
    }

class Agent:
    def __init__(self, client, model="gemini-2.5-flash", system=""):
        self.client = client
        self.model = model
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        assistant_instruction = self.execute()
        self.messages.append({"role": "assistant", "content": assistant_instruction})
        return assistant_instruction

    def execute(self):
        completion = self.client.chat.completions.create(
                        model=self.model,
                        temperature=0,
                        messages=self.messages)
        return completion.choices[0].message.content

def get_initial_prompt():
    return """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:

Answer: A bulldog weights 51 lbs
""".strip()

def manual_assistance(client):
    abot = Agent(client, system=get_initial_prompt())  # init
    assistant_instructions = abot("How much does a toy poodle weigh?")  # call
    print("assistant_instructions:\n", assistant_instructions)

    # the instructions:  average_dog_weight: Toy Poodle
    # we are supposed to call this function and provide the answer
    the_answer = average_dog_weight("Toy Poodle")
    final_response = abot(f"Observation: {the_answer}")
    print(final_response)


def main():
    # Load environment variables, including your API key
    load_dotenv()
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_GENAI_API_KEY not found in environment")
        return
    # Gemini models are accessible using the OpenAI libraries (Python and TypeScript / Javascript)
    # along with the REST API, by updating three lines of code and using your Gemini API key.
    # https://ai.google.dev/gemini-api/docs/openai
    client = OpenAI(
        api_key  = api_key,
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # manual_assistance(client)

    known_actions = get_known_actions()
    action_re = re.compile('^Action: (\w+): (.*)$')
    bot = Agent(client, system=get_initial_prompt())

    next_prompt = """
        I have 2 dogs, a border collie and a scottish terrier. 
        What is their combined weight?
    """

    for i in range(5):
        print("************************************")
        print("next prompt:\n", next_prompt)
        result = bot(next_prompt)
        print("reply:\n", result)
        actions = [
            action_re.match(a)
            for a in result.split('\n')
            if action_re.match(a)
        ]
        print("actions: ", [a.groups() for a in actions])
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(f"Unknown action: {action}: {action_input}")
            print(f" -- running {action} {action_input}")
            observation = known_actions[action](action_input)
            next_prompt = f"Observation: {observation}"
        else:
            break



if __name__ == "__main__":
    main()
