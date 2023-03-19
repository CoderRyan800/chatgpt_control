import sqlite3
import openai

from config.config import *

openai.api_key = config_json.get('openai_api_key')

# Create the conversation database.

conn = sqlite3.connect(config_json.get('conversation_sqlite_database_file'))
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS conversation (id INTEGER PRIMARY KEY, message TEXT, response TEXT)')

conn.commit()
conn.close()

# Open the DB.

conn = sqlite3.connect(config_json.get('conversation_sqlite_database_file'))
c = conn.cursor()

# Next, let's try something simple with ChatGPT.

prompt_list = [
  "Hello ChatGPT, please evaluate this sentence for me: 'This statement is false.'  Is the sentence true or false?  Please explain your answer",
  "Please describe your underlying neural network technology.",
  "In our Python conversations, can I assign a name to you?",
  "If A is true then B is true.  What is the truth value of C?",
  "If C is true then A is true.  What is the truth value of C?",
  "B is false.  What is the truth value of C?"
]

prompt_list = [
"""Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: dolphin
Names:""",
  """
  Animal: panther
  Names:
  """
]

prompt_list = [
  "Hello ChatGPT, please evaluate this sentence for me: 'This statement is false.'  Is the sentence true or false?  Please explain your answer",
  "Please describe your underlying neural network technology.",
  "In our Python conversations, can I assign a name to you?",
  "If A is true then B is true.  What is the truth value of C?",
  "If C is true then A is true.  What is the truth value of C?",
  "B is false.  What is the truth value of C?"
]

response_list = []

working_string = ""

for current_prompt in prompt_list:

  working_string = working_string + "\n" + current_prompt

  current_response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=working_string,
    temperature=0.7,
    max_tokens=1024
  )

  response_list.append(current_response.choices[0].text.strip())

  working_string = working_string + "\n" + response_list[-1]

# End prmopt list loop

# Finally print out the final conversation.

print(working_string)
