import openai
#openai.api_key = "YOUR_API_KEY_HERE"

from config.config import *
openai.api_key = config_json['openai_api_key']

models = openai.Model.list()
for model in models['data']:
    print(model['id'])
