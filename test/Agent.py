import openai
from config.config import *

openai.api_key = config_json['openai_api_key']

class Agent:
    def __init__(self, agent_id, num_agents):
        self.id = agent_id
        self.num_agents = num_agents
        self.flag_problem_solved = False
        self.flag_problem_failed = False
        self.n_initial_messages = 0
        self.memory = [
            {"role":"system","content": f"You are a problem-solving Agent named Agent {self.id}."},
            {"role": "user", "content": 
                f"Your name is Agent {self.id}. You are one of {num_agents} system Agents. " +
                "You must respond to any message addressed to you as Agent {self.id}, " +
                "and you must respond to any message addressed to all Agents. " +
                "You must not respond to a message addressed to another agent, " +
                "but you must remember it." 
            }
        ]

    def add_message(self, role, content):
        self.memory.append({"role": role, "content": content})

    def respond(self, content):
        self.add_message("user", content)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.memory
        )

        message = response.choices[0].message['content']

        if "I know the answer" in message:
            self.flag_problem_solved = True
        elif "I do not know the answer" in message or len(self.memory) > self.n_initial_messages + 5 * self.num_agents:
            self.flag_problem_failed = True
        return message

    def get_flag_problem_solved(self):
        return self.flag_problem_solved

    def get_flag_problem_failed(self):
        return self.flag_problem_failed

    def get_memory(self):
        return self.memory
