import os
import json
import time
import numpy as np
from agent import Agent

class Environment:
    def __init__(self, num_agents, max_recursion_depth):
        self.agents = []
        self.max_recursion_depth = max_recursion_depth
        self.problem_solved_flags = np.zeros((num_agents,))
        for i in range(num_agents):
            memory_file = f"agent_{i}_memory.txt"
            if os.path.isfile(memory_file):
                self.agents.append(Agent(i, num_agents, memory_file))
            else:
                self.agents.append(Agent(i, num_agents))

    def all_agents_solved(self):
        for agent in self.agents:
            if agent.get_flag_problem_solved():
                self.problem_solved_flags[agent.id] = 1

    def send_message(self, content, recursion_depth=0):
        print(f"send_message({content},{recursion_depth})")
        self.all_agents_solved()
        if np.sum(self.problem_solved_flags) > len(self.agents)/2 or recursion_depth >= self.max_recursion_depth:
            print("Problem solved!\n")
            for agent in self.agents:
                with open(f"agent_{agent.id}_final_memory.txt", 'w') as file:
                    json.dump(agent.get_memory(), file, indent=4)
            return

        # Allow all agents to respond to the message
        responses = []
        for agent in self.agents:
            print(f"Agent {agent.id} is responding to {content}.")
            response = agent.respond(content)
            formatted_response = f"Agent {agent.id} says: {response}"
            responses.append(formatted_response)
            time.sleep(5)

        # If there is no more recursion depth, return
        if recursion_depth+1 >= self.max_recursion_depth:
            return

        # Create a new list of messages to send, combining individual and combined responses
        messages_to_send = []
        messages_to_send.extend(responses)

        combined_message = '\n'.join(responses)

        # Call send_message recursively for each message in the list
        self.send_message(combined_message, recursion_depth + 1)


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
