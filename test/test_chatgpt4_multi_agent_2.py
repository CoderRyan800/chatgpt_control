import re
import random
import openai
from config.config import *

openai.api_key = config_json['openai_api_key']

PROBLEM_SOLVED_STRING = 'I know the answer'
PROBLEM_UNSOLVABLE_STRING = 'Insufficient information'
MAX_CONVERSATION_LENGTH = 35

class Agent:
    def __init__(self, name, generate_text_function, choose_receiver_function):
        self.name = name
        self.knowledge = ["Hello", "How are you?", "What's your favorite color?"]
        self.memory = []
        self.generate_text = generate_text_function
        self.choose_receiver = choose_receiver_function

    def receive_message(self, sender_id, message, broadcast):
        prompt = f"{self.name}: {message}"
        response = self.generate_text(prompt)

        if broadcast:
            receiver_id = self.choose_receiver(sender_id)
        else:
            receiver_id = sender_id

        return response, receiver_id


class Environment:
    def __init__(self, n_agents, generate_text_function, choose_receiver_function):
        self.agents = [
            Agent(f"Agent {agent_id}", generate_text_function, choose_receiver_function)
            for agent_id in range(n_agents)
        ]

    def send_message(self, receiver_id, message, sender_id, broadcast=False):
        agent = self.agents[receiver_id]
        response, receiver_id = agent.receive_message(sender_id, message, broadcast)

        if receiver_id is not None and receiver_id != sender_id:
            self.send_message(receiver_id, response, sender_id)

    def start_conversation(self):
        random_agent_id = random.randint(0, len(self.agents) - 1)
        self.send_message(random_agent_id, self.agents[random_agent_id].knowledge[-1], random_agent_id, broadcast=True)

    def provide_agent_info(self, agent_id, info):
        self.agents[agent_id].knowledge.append(info)

    def provide_problem_statement(self, problem_statement):
        for agent in self.agents:
            agent.knowledge.append(problem_statement)

    def print_conversation(self):
        conversation = "Conversation:"
        for agent in self.agents:
            for message in agent.memory:
                conversation += f"\n{agent.name}: {message[1]}"
        print(conversation)

    def get_solution(self):
        for agent in self.agents:
            if agent.memory and re.search(PROBLEM_SOLVED_STRING, agent.memory[-1][1]):
                return agent.memory[-1][1]
        return None


def dummy_generate_text(prompt):
    return "Dummy response"

def dummy_choose_receiver(sender_id):
    return (sender_id + 1) % 2

# ... (previous code)

generate_text_function = dummy_generate_text
choose_receiver_function = dummy_choose_receiver
env = Environment(2, generate_text_function, choose_receiver_function)

problem_statement = (
    "Tell Igor what flowers to purchase for Natasha. If there is enough information to provide a specific flower " +
    "type then provide guidance and include the exact string '%s' in your answer. " % (PROBLEM_SOLVED_STRING,) +
    "If you lack adequate information, then ask another agent, but not yourself, for help and state your " +
    "situation to that agent.  If, even after multiple tries with the other agents, you cannot solve the " +
    "problem, then indicate it is not solvable and include the specific string '%s'  in your answer." % (PROBLEM_UNSOLVABLE_STRING,) +
    "Do not give up and indicate it is unsolvable just because you lack enough information initially.  Instead " +
    "make multiple attempts to ask the other agents for their information and try to solve it first."
)
env.provide_problem_statement(problem_statement)

agent0_info = "Your name is Agent 0, and you are to answer to that name. There is one other agent whose name is Agent 1. Natasha likes roses and orchids but not carnations. Igor does not know which flowers the only available florist has. If you have enough information to provide a specific flower type, provide guidance and include the exact string 'I know the answer' in your answer. If you lack adequate information, ask Agent 1 for help and state your situation to that agent."
agent1_info = "Your name is Agent 1, and you are to answer to that name. There is one other agent whose name is Agent 0. The only available florist has orchids and carnations but not roses. You do not initially know which flowers Natasha actually likes. If you have enough information to provide a specific flower type, provide guidance and include the exact string 'I know the answer' in your answer. If you lack adequate information, ask Agent 0 for help and state your situation to that agent."
agent0_info = agent0_info + problem_statement
agent1_info = agent1_info + problem_statement
env.provide_agent_info(0, agent0_info)
env.provide_agent_info(1, agent1_info)

env.start_conversation()

solution = env.get_solution()
env.print_conversation()
print(f"Solution: {solution}")
