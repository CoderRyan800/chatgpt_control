import openai
from config.config import *
openai.api_key = config_json['openai_api_key']

def chat_gpt_response(prompt):
    response_object = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[prompt],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.1,
        best_of=3,
    )
    return response_object['choices'][0]['message']['content']
class ChatGPTAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.messages = [
            {"role": "system", "content": "Your name is Agent %d, and you are distinct from any other Agent." % (agent_id,)},
            {"role": "user", "content": "Please tell me your name."},
            {"role": "assistant", "content": "My name is Agent %d" % (agent_id,)},
            {"role": "user", "content": "You are to respond to any message addressed to you using your name.  You are also to respond to any message addressed to all agents.  You are not to respond to a message addressed to a different agent."}
        ]

    def send_message(self, recipient, message_string):

        message = {
            "role": "user",
            "content": message_string
        }

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

# num_agents = 5
# env = ChatGPTEnvironment(num_agents)
#
# # Private conversation between user and agent 0
# user_message = "Hello Agent 0, how are you?"
# response = env.private_conversation(0, user_message)
# print(f"Agent 0: {response}")
#
# # Conversation between agent 0 and agent 1
# message = "Hello Agent 1, I'm Agent 0. Can you help me solve a problem?"
# response = env.agent_to_agent_conversation(0, 1, message)
# print(f"Agent 1: {response}")
#
# # Agent 2 broadcasts a message to all other agents
# broadcast_message = "Attention all agents, this is Agent 2. We have an important update!"
# env.broadcast_message(2, broadcast_message)

