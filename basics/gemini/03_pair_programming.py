#! /usr/bin/env python

import os
import google.generativeai as genai
from google.api_core import client_options as client_option_lib

from dotenv import load_dotenv, find_dotenv

# helper fn for the API
def generate_text(prompt, model, temperature=0.0):
    return model.generate_content(prompt, generation_config={"temperature": temperature})


def improve_code(model):
    prompt_template_1 = """
I don't think this code is the best way to do it in Python, can you help me?
```python
{question}
```
Please explain, in detail, what you did to improve it.
"""

    prompt_template_2 = """
I don't think this code is the best way to do it in Python, can you help me?
```python
{question}
```
Please explore multiple ways of solving the problem, and explain each.
"""

    prompt_template = """
    I don't think this code is the best way to do it in Python, can you help me?
    ```python
    {question}
    ```
    Please explore multiple ways of solving the problem, and tell me which is the most Pythonic.
    """

    question = """
def func_x(array):
  for i in range(len(array)):
    print(array[i])
"""
    prompt = prompt_template.format(question=question)
    print(prompt)
    completion = generate_text(prompt, model)
    print(completion.text)


def simplify_code(model):
    prompt_template = """
Can you please simplify this code for a linked list in Python?
```python
    {question}
```
Explain in detail what you did to modify it, and why.
---------------
    """
    question = """
class Node:
  def __init__(self, dataval=None):
    self.dataval = dataval
    self.nextval = None

class SLinkedList:
  def __init__(self):
    self.headval = None

list1 = SLinkedList()
list1.headval = Node("Mon")
e2 = Node("Tue")
e3 = Node("Wed")
list1.headval.nextval = e2
e2.nextval = e3

"""
    prompt = prompt_template.format(question=question)
    print(prompt)
    completion = generate_text(prompt, model)
    print(completion.text)

def make_code_more_efficient(model):
    prompt_template = """
Can you please make this code more efficient?
```python
    {question}
```
Explain in detail what you changed and why.
    """
    question = """
# Returns index of x in arr if present, else -1
def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:
        mid = (high + low) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, high, x)
    else:
        return -1

# Test array
arr = [ 2, 3, 4, 10, 40 ]
x = 10

# Function call
result = binary_search(arr, 0, len(arr)-1, x)

if result != -1:
    print("Element is present at index", str(result))
else:
    print("Element is not present in array")

"""
    prompt = prompt_template.format(question=question)
    print(prompt)
    completion = generate_text(prompt, model)
    print(completion.text)

def debug_code(model):
    prompt_template = """
Can you please help me to debug this code?
```python
{question}
```
Explain in detail what you found and why it was a bug.
    """
# I deliberately introduced a bug into this code! Let's see if the LLM can find it.
# Note -- the model can't see this comment -- but the bug is in the
# print function. There's a circumstance where nodes can be null, and trying
# to print them would give a null error.
    question = """
class Node:
   def __init__(self, data):
      self.data = data
      self.next = None
      self.prev = None

class doubly_linked_list:
   def __init__(self):
      self.head = None

# Adding data elements
   def push(self, NewVal):
      NewNode = Node(NewVal)
      NewNode.next = self.head
      if self.head is not None:
         self.head.prev = NewNode
      self.head = NewNode

# Print the Doubly Linked list in order
   def listprint(self, node):
       print(node.data),
       last = node
       node = node.next

dllist = doubly_linked_list()
dllist.push(12)
dllist.push(8)
dllist.push(62)
dllist.listprint(dllist.head)

"""
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
    # improve_code(model_flash)
    # simplify_code(model_flash)
    # make_code_more_efficient(model_flash)
    debug_code(model_flash)

if __name__ == "__main__":
    main()
