import random
import openai
from config.config import *

openai.api_key = config_json['openai_api_key']

class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.knowledge = []
        self.memory = []
        self.problem_solved = False
        self.failed = False

    def check_solution(self, message):
        if "I know the answer: " in message:
            self.problem_solved = True
        elif "Insufficient information." in message and len(self.memory) >= 10:
            self.failed = True
        return message

    def receive_message(self, sender_id, message, broadcast=False):
        self.memory.append((sender_id, message, broadcast))
        response = self.generate_response(message)
        response = self.check_solution(response)

        if self.problem_solved or self.failed:
            return None

        if "Agent " in response:
            receiver_id = int(response.split("Agent ")[1].split(",")[0])
            return (self.agent_id, response, False, receiver_id)
        else:
            return (self.agent_id, response, True)

    def update_knowledge(self, statement):
        self.knowledge.append(statement)

    def generate_response(self, message):
        # Add a custom user instruction to guide GPT-4
        user_instruction = f"{message} If you know the answer, say 'I know the answer: '. If you need to ask another agent, say 'Agent X, please help: '. If there is not enough information to solve the problem, say 'Insufficient information.'."

        messages = [{"role": "system", "content": "You are a helpful assistant."}]

        # Add the agent's knowledge as user messages
        for knowledge_item in self.knowledge:
            messages.append({"role": "user", "content": knowledge_item})

        # Add the conversation history
        for sender_id, msg, _ in self.memory:
            role = "user" if sender_id != self.agent_id else "assistant"
            messages.append({"role": role, "content": msg})

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            user=user_instruction
        )

        return completion.choices[0].message['content']



class Environment:
    def __init__(self, n_agents):
        self.agents = [Agent(agent_id) for agent_id in range(n_agents)]

    def print_conversation(self):
        print("Conversation:")
        for agent in self.agents:
            for sender_id, msg, broadcast in agent.memory:
                sender = f"Agent {sender_id}"
                print(f"{sender}: {msg}")

    def send_message(self, sender_id, message, broadcast, receiver_id=None):
        print(f"Agent {sender_id}: {message}")

        if broadcast:
            for agent in self.agents:
                if agent.agent_id != sender_id:
                    response = agent.receive_message(sender_id, message, broadcast=True)
                    if response is not None:
                        self.send_message(*response)
                    else:
                        break
        else:
            response = self.agents[receiver_id].receive_message(sender_id, message)
            if response is not None:
                self.send_message(*response)
            else:
                return
            
    def provide_problem_statement(self, problem_statement):
        for agent in self.agents:
            agent.update_knowledge(problem_statement)

    def provide_agent_info(self, agent_id, info):
        self.agents[agent_id].update_knowledge(info)

    def start_conversation(self):
        random_agent_id = random.randint(0, len(self.agents) - 1)
        self.send_message(random_agent_id, self.agents[random_agent_id].knowledge[-1], broadcast=True)

env = Environment(2)
problem_statement = "Tell Igor what flowers to purchase for Natasha."
env.provide_problem_statement(problem_statement)

agent0_info = "Natasha likes roses and orchids but not carnations. Igor does not know which flowers only available florist has."
agent1_info = "The only available florist has orchids and carnations but not roses."
env.provide_agent_info(0, agent0_info)
env.provide_agent_info(1, agent1_info)

env.start_conversation()

solution = ""
for agent in env.agents:
    if agent.problem_solved:
        print(f"Agent {agent.agent_id} has solved the problem!")
        solution = agent.memory[-1][1]
    elif agent.failed:
        print(f"Agent {agent.agent_id} has failed to solve the problem.")

env.print_conversation()
print(f"Solution: {solution}")

