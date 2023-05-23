import os
from agent import Agent

class Environment:
    def __init__(self, num_agents, max_recursion_depth):
        self.agents = []
        self.max_recursion_depth = max_recursion_depth
        for i in range(num_agents):
            memory_file = f"agent_{i}_memory.txt"
            if os.path.isfile(memory_file):
                self.agents.append(Agent(i, num_agents, memory_file))
            else:
                self.agents.append(Agent(i, num_agents))

    def all_agents_solved(self):
        for agent in self.agents:
            if agent.get_flag_problem_solved():
                return True
        return False

    def send_message(self, sender, recipient, content, recursion_depth=0):
        print(f"send_message({sender},{recipient},{content},{recursion_depth}")
        if self.all_agents_solved() or recursion_depth >= self.max_recursion_depth:
            for agent in self.agents:
                with open(f"agent_{agent.id}_memory.txt", 'w') as file:
                    json.dump(agent.get_memory(), file)
            return

        if recipient == "All Agents":
            for agent in self.agents:
                response = agent.respond(content)
                self.send_message(f"Agent {agent.id}", self.parse_recipient(response), response, recursion_depth + 1)
        else:
            recipient_id = int(recipient.split(" ")[1])
            response = self.agents[recipient_id].respond(content)
            self.send_message(f"Agent {recipient_id}", self.parse_recipient(response), response, recursion_depth + 1)

    def parse_recipient(self, message):
        if "All Agents" in message:
            return "All Agents"
        else:
            words = message.split(" ")
            for i, word in enumerate(words):
                if word == "Agent":
                    recipient = "Agent " + words[i + 1]
                    if recipient[-1] == ",":
                        recipient = recipient[:-1]
                    return recipient
        return ""
