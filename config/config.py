import json

fp = open('/home/ryanmukai/Documents/github/chatgpt_control/config/config.json','r')

config_json = json.load(fp)

fp.close()

fp = open(config_json.get('openai_api_key_path'),'r')

key_string = fp.readline()

fp.close()

config_json['openai_api_key'] = key_string.strip()


