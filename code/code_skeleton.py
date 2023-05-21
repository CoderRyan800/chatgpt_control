import openai
from config.config import *
import json

openai.api_key = config_json['openai_api_key']

class Agent:
    def __init__(self, name, instructions, other_agents, initial_messages):
        self.name = name
        self.instructions = instructions
        self.other_agents = other_agents
        self.messages = []
        self.flag_problem_solved = False
        self.flag_problem_failed = False
        self.n_initial_messages = initial_messages
        # Add more attributes if needed

    def receive_message(self, message):
        # add message to memory and process it if it's addressed to this agent
        pass

    def create_message(self):
        # generate message with GPT-4, make sure to follow the rules
        pass

    def save_memory(self, filename):
        # save the memory to the specified file in JSON format
        pass

class Environment:
    def __init__(self, num_agents, instructions):
        self.agents = []
        for i in range(num_agents):
            self.agents.append(Agent(f"Agent_{i}", instructions, num_agents, len(instructions)))
        self.flag_problem_solved = False
        self.flag_problem_failed_to_solve = False

    def initialize_agents(self):
        # Send initial instructions to all agents
        pass

    def facilitate_conversation(self):
        # facilitate the conversation until the problem is solved or cannot be solved
        pass

    def save_conversation(self, filename):
        # save the conversation history to the specified file in JSON format
        pass

# For the test part, we will use Python unittest module
import unittest

class TestAgent(unittest.TestCase):
    def test_memory_maintainance(self):
        # Test memory maintainance of the agent
        pass

    def test_agent_reminder(self):
        # Test agent reminder function
        pass

    # Add more test cases as needed

if __name__ == "__main__":
    unittest.main()
