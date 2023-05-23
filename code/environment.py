import os
import json
from agent import Agent
import re

class Environment:
    def __init__(self, num_agents, recursive_depth_limit=10):
        self.agents = []
        self.recursive_depth_limit = recursive_depth_limit
        for agent_id in range(num_agents):
            agent_memory_file = f'agent_{agent_id}_memory.txt'
            if os.path.isfile(agent_memory_file):
                self.agents.append(Agent(agent_id, num_agents, agent_memory_file))
            else:
                self.agents.append(Agent(agent_id, num_agents))

    def _save_agent_memory(self, agent_id):
        agent = self.agents[agent_id]
        with open(f'agent_{agent_id}_memory.txt', 'w') as file:
            json.dump(agent.get_memory(), file)

    def send_message(self, message, recipient, recursive_depth=0):
        if recursive_depth >= self.recursive_depth_limit:
            print("Recursive depth limit reached, message not sent.")
            return

        if recipient == "All Agents":
            for agent in self.agents:
                agent.add_message("user", message)
                response = agent.respond(message)
                self._save_agent_memory(agent.id)
                print(f'Agent {agent.id} responded: {response}')
                recipient_response = re.findall(r"^(All Agents|Agent \d+)", response)
                if recipient_response:
                    self.send_message(response, recipient_response[0], recursive_depth + 1)
        else:
            agent_id = int(recipient.split(' ')[1])  # Get agent ID from recipient string 'Agent {id}'
            agent = self.agents[agent_id]
            agent.add_message("user", message)
            response = agent.respond(message)
            self._save_agent_memory(agent.id)
            print(f'Agent {agent_id} responded: {response}')
            recipient_response = re.findall(r"^(All Agents|Agent \d+)", response)
            if recipient_response:
                self.send_message(response, recipient_response[0], recursive_depth + 1)
