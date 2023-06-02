import openai
import json
from config.config import *
from agent_instructions import *

openai.api_key = config_json['openai_api_key']

class Agent:
    def __init__(self, agent_id, num_agents, agent_memory_file=None):
        self.id = agent_id
        self.num_agents = num_agents
        self.flag_problem_solved = False
        self.flag_problem_failed = False
        self.n_initial_messages = 0
        if agent_memory_file is None:
            self.memory = generate_agent_instructions(agent_id=agent_id)
        else:
            with open(agent_memory_file,'r') as file:
                self.memory = json.load(file)

    def add_message(self, role, content):
        self.memory.append({"role": role, "content": content})

    def respond(self, content):
        self.add_message("user", content)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.memory
        )

        message = response.choices[0].message['content']

        # Add the agent's response to the memory
        self.add_message("assistant", message)

        if "I know the answer" in message:
            self.flag_problem_solved = True
            self.flag_problem_failed = False
        elif "I do not know the answer" in message:
            self.flag_problem_solved = False
            self.flag_problem_failed = False
        elif "I cannot solve the problem" in message:
            self.flag_problem_solved = False
            self.flag_problem_failed = True

        return message

    def get_flag_problem_solved(self):
        return self.flag_problem_solved

    def get_flag_problem_failed(self):
        return self.flag_problem_failed

    def get_memory(self):
        return self.memory
