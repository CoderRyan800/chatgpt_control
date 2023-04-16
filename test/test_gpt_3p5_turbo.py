import openai
import json
#openai.api_key = "YOUR_API_KEY_HERE"

from config.config import *
openai.api_key = config_json['openai_api_key']

response_object = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Igor is dating Natasha and has to buy her flowers.  Natasha likes roses and orchids but does not like carnations.  Igor does not know which flowers the local florist has available?  Do you know which flowers Igor should purchase?  If you lack adequate information, please explain why, and include 'I need more information' in your response.  If you have enough information, please answer and explain your reasoning and include 'I have adequate information' in your response."}
    ]
)

print(type(response_object))
print(response_object['choices'][0]['message']['content'])
