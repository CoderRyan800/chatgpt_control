import openai
from config.config import *
openai.api_key = config_json['openai_api_key']

def chat_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


class ChatGPTAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.conversations = {}

    def send_message(self, recipient, message):
        if recipient not in self.conversations:
            self.conversations[recipient] = []

        self.conversations[recipient].append({"sender": self.agent_id, "message": message})
        response = chat_gpt_response(message)
        self.conversations[recipient].append({"sender": "ChatGPT", "message": response})
        return response

    def receive_message(self, sender, message):
        if sender not in self.conversations:
            self.conversations[sender] = []
        self.conversations[sender].append({"sender": sender, "message": message})

class ChatGPTEnvironment:
    def __init__(self, num_agents):
        self.agents = [ChatGPTAgent(i) for i in range(num_agents)]

    def private_conversation(self, agent_id, message):
        agent = self.agents[agent_id]
        return agent.send_message("user", message)

    def agent_to_agent_conversation(self, sender_id, recipient_id, message):
        sender_agent = self.agents[sender_id]
        recipient_agent = self.agents[recipient_id]
        response = sender_agent.send_message(f"agent_{recipient_id}", message)
        recipient_agent.receive_message(f"agent_{sender_id}", message)
        return response

    def broadcast_message(self, sender_id, message):
        sender_agent = self.agents[sender_id]
        for recipient_id, recipient_agent in enumerate(self.agents):
            if sender_id != recipient_id:
                sender_agent.send_message(f"agent_{recipient_id}", message)
                recipient_agent.receive_message(f"agent_{sender_id}", message)

num_agents = 5
env = ChatGPTEnvironment(num_agents)

# Private conversation between user and agent 0
user_message = "Hello Agent 0, how are you?"
response = env.private_conversation(0, user_message)
print(f"Agent 0: {response}")

# Conversation between agent 0 and agent 1
message = "Hello Agent 1, I'm Agent 0. Can you help me solve a problem?"
response = env.agent_to_agent_conversation(0, 1, message)
print(f"Agent 1: {response}")

# Agent 2 broadcasts a message to all other agents
broadcast_message = "Attention all agents, this is Agent 2. We have an important update!"
env.broadcast_message(2, broadcast_message)

