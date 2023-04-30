import openai
from config.config import *
openai.api_key = config_json['openai_api_key']

class Agent:
    def __init__(self, agent_id, num_agents):
        self.id = agent_id
        self.num_agents = num_agents
        self.messages = []
        self.addressed_to = None
        
        if self.num_agents > 1:
            self.addressing_instructions = f"Please address your messages to 'all' or to a specific agent number between 0 and {self.num_agents - 1}, or to 'Human' (e.g. 'ask agent1 ...', 'send agent2 ...', 'ask_Human ...', or 'send_Human ...')"
        else:
            self.addressing_instructions = "You are the only agent in this environment. Please address your messages to 'all' or to 'Human'."
        
        self.add_message("assistant", self.addressing_instructions)
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        
    def send_message(self, addressed_to, content):
        addressed_to.add_message(self.id, content)
    
    def generate_response(self, prompt, addressed_to=None):
        messages = self.messages.copy()
        messages.append({"role": "user", "content": str(prompt)})
        if addressed_to is not None:
            addressed_to_str = addressed_to.id if addressed_to.id == "Human" else f"agent{addressed_to.id}"
            self.add_message("assistant", f"Sending message to {addressed_to_str}")
        else:
            self.add_message("assistant", "Broadcasting message to all agents")
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=messages,
            temperature=0.7,
            max_tokens=1024,
            n=1,
            stop=None,
            timeout=10,
        )
        text = response.choices[0].text.strip()
        self.add_message("assistant", text)
        return text
    
class MultiAgentEnvironment:
    def __init__(self, num_agents):
        self.agents = [Agent(i, num_agents) for i in range(num_agents)]
        self.agents.append(Agent("Human", num_agents))
    
    def get_agent(self, agent_id):
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None
    
    def parse_message(self, sender_id, message):
        tokens = message.split(" ")
        if tokens[0] == "ask":
            addressed_to_str = tokens[1]
            if addressed_to_str == "all":
                for agent in self.agents:
                    if agent.id != sender_id:
                        agent.send_message(self.get_agent(sender_id), " ".join(tokens[2:]))
            elif addressed_to_str == "Human":
                addressed_to = self.get_agent("Human")
                addressed_to.send_message(self.get_agent(sender_id), " ".join(tokens[2:]))
            elif addressed_to_str.startswith("agent") and addressed_to_str[5:].isdigit():
                addressed_to_id = int(addressed_to_str[5:])
                addressed_to = self.get_agent(addressed_to_id)
                if addressed_to is None:
                    self.get_agent("Human").add_message("assistant", f"No agent with id {addressed_to_id}")
                    return
                addressed_to.send_message(self.get_agent(sender_id), " ".join(tokens[2:]))
            else:
                self.get_agent("Human").add_message("assistant", f"Invalid agent id: {addressed_to_str}")
                return
        elif tokens[0] == "send":
            addressed_to_str = tokens[1]
            if addressed_to_str == "all":
                for agent in self.agents:
                    if agent.id != sender_id:
                        agent.send_message(self.get_agent(sender_id), " ".join(tokens[2:]))
                addressed_to = self.get_agent("Human")
                addressed_to.send_message(self.get_agent(sender_id), " ".join(tokens[2:]))
            elif addressed_to_str == "Human":
                addressed_to = self.get_agent("Human")
                addressed_to.send_message(self.get_agent(sender_id), " ".join(tokens[2:]))
            elif addressed_to_str.startswith("agent") and addressed_to_str[5:].isdigit():
                addressed_to_id = int(addressed_to_str[5:])
                addressed_to = self.get_agent(addressed_to_id)
                if addressed_to is None:
                    self.get_agent("Human").add_message("assistant", f"No agent with id {addressed_to_id}")
                    return
                addressed_to.send_message(self.get_agent(sender_id), " ".join(tokens[2:]))
            else:
                self.get_agent("Human").add_message("assistant", f"Invalid agent id: {addressed_to_str}")
                return
        elif tokens[0] == "ask_Human":
            addressed_to = self.get_agent("Human")
            addressed_to.send_message(self.get_agent(sender_id), " ".join(tokens[1:]))
        elif tokens[0] == "send_Human":
            addressed_to = self.get_agent("Human")
            addressed_to.send_message(self.get_agent(sender_id), " ".join(tokens[1:]))


env = MultiAgentEnvironment(num_agents=2)

# Initialize agents with necessary knowledge
env.parse_message(0, "send Human Agent 0 knows that Igor is dating Natasha.")
env.parse_message(0, "send Human Natasha likes roses and orchids but hates carnations.")
env.parse_message(1, "send Human Agent 1 knows that the florist has orchids and carnations but not roses.")

# Agent 0 asks Agent 1 what flowers are available and what Natasha likes
env.parse_message(0, "ask Agent1 What flowers does the florist have?")
env.parse_message(1, "send Agent0 The florist has orchids and carnations.")
env.parse_message(0, "ask Agent1 Which flowers does Natasha like?")
env.parse_message(1, "send Agent0 Natasha likes roses and orchids but hates carnations.")

# Agent 0 determines which flowers Igor should purchase
env.parse_message(0, "ask Agent1 Does the florist have roses?")
env.parse_message(1, "send Agent0 No, the florist does not have roses.")
env.parse_message(0, "send Agent1 Okay, got it. Tell Igor to get orchids.")

# Agent 1 broadcasts the final message to Igor
env.parse_message(1, "send Human Igor, please purchase orchids from the florist.")
