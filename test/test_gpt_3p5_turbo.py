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
        {"role": "user", "content": "Your name is Agent 0.  You will respond to messages addressed to you.  You will only listen to but not respond to messages addressed to other agents."},
        {"role": "assistant", "content": "Understood.  I am Agent 0 and am not any other agent.  I listen to all messages but only respond to thsoe addressed to me."},
        {"role": "user", "content": "Agent 0, please remember that you have a blue card.  Please acknowledge."},
        {"role": "assistant", "content": "Yes, I have a blue card."},
        {"role": "user", "content": "Agent 12, please remember you have a red card.  Please acknowledge."},
        {"role": "assistant", "content": ""},
        {"role": "user", "content": "Agent 0, what card do you have?"},
        {"role": "assistant", "content": "I have the blue card."},
        {"role": "user", "content": "Agent 0, what card does Agent 12 have?"},
        #{"role": "assistant", "content": "Agent 12 has a red car."},
        #{"role": "user", "content": "Agent 0, Igor is dating Natasha and has to buy her flowers.  Natasha likes roses and orchids but does not like carnations.  Igor does not know which flowers the local florist has available?  Do you know which flowers Igor should purchase?  If you lack adequate information, please explain why, and include 'I need more information' in your response.  If you have enough information, please answer and explain your reasoning and include 'I have adequate information' in your response."}


    ]
)

print(type(response_object))
print(response_object['choices'][0]['message']['content'])
