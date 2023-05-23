# environment.py

import json
from agent import Agent

class Environment:
    def __init__(self, num_agents):
        self.agents = [Agent(i, num_agents) for i in range(num_agents)]

    def send_message(self, sender, recipient, message):
        if recipient == 'All Agents':
            for agent in self.agents:
                agent.add_message('user', message)
                response = agent.respond(message)
                self._print_message(sender, f'Agent {agent.id}', response)
                self._save_agent_memory(agent)
        else:
            recipient_id = int(recipient.split(' ')[1])
            self.agents[recipient_id].add_message('user', message)
            response = self.agents[recipient_id].respond(message)
            self._print_message(sender, recipient, response)
            self._save_agent_memory(self.agents[recipient_id])

    def _print_message(self, sender, recipient, message):
        print(f'{sender} to {recipient}: {message}')

    def _save_agent_memory(self, agent):
        with open(f'agent_{agent.id}_memory.txt', 'w') as file:
            json.dump(agent.get_memory(), file)
