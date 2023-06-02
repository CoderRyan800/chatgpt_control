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

    def send_message(self, sender, recipient, content, recursion_depth=0):
        print(f"send_message({sender},{recipient},{content},{recursion_depth}")
        self.all_agents_solved()
        if np.sum(self.problem_solved_flags) > len(self.agents)/2 or recursion_depth >= self.max_recursion_depth:
            print("Problem solved!\n")
            for agent in self.agents:
                with open(f"agent_{agent.id}_final_memory.txt", 'w') as file:
                    json.dump(agent.get_memory(), file, indent=4)
            return

        agent_response_list = []
        for agent in self.agents:
            if f"Agent {agent.id}" != sender:
                response = agent.respond(content)
                agent_response_list.append([agent,response])
            time.sleep(5)
        for agent_response in agent_response_list:
            agent = agent_response[0]
            response = agent_response[1]
            self.send_message(f"Agent {agent.id}", self.parse_recipient(response), response, recursion_depth + 1)


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
