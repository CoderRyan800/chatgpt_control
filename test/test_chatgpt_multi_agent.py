
import re
from chatgpt_interface.chatgpt_multi_agent import *

# num_agents = 5
# env = ChatGPTEnvironment(num_agents)
#
# # Private conversation between user and agent 0
# user_message = "Hello Agent 0, how are you?"
# response = env.private_conversation(0, user_message)
# print(f"Agent 0: {response}")
#
# # Conversation between agent 0 and agent 1
# message = "Hello Agent 1, I'm Agent 0. Can you help me solve a problem?"
# response = env.agent_to_agent_conversation(0, 1, message)
# print(f"Agent 1: {response}")
#
# # Agent 2 broadcasts a message to all other agents
# broadcast_message = "Attention all agents, this is Agent 2. We have an important update!"
# env.broadcast_message(2, broadcast_message)

num_agents = 2
env = ChatGPTEnvironment(num_agents)

# Private conversation between user and agent 0
request_to_agent_0 = 'Call Agent 0'
request_to_agent_1 = 'Call Agent 1'
no_help_needed = 'No help needed'

regex_call_agent_0 = re.compile(request_to_agent_0)
regex_call_agent_1 = re.compile(request_to_agent_1)
regex_no_help_needed = re.compile(no_help_needed)

user_message = ("Hello Agent 0, we know that Igor is dating Natasha and must bring her flowers. " +
                "Natasha likes roses and orchids but does not like carnations. " +
                "You lack information on what the florist has available at this moment. " +
                "Which flowers can Igor buy for  Natasha.  You can ask other agents for help. " +
                "Either state the flowers Igor should purchase or ask Agent 1 to help you. " +
                f"If you need me to relay a message for Agent 1, please clearly say, {request_to_agent_1}. " +
                f"If you don't need Agent 1 to help you, state your answer and clearly say, {no_help_needed}."
                )
print(f"User: {user_message}")
response_of_agent_0 = env.private_conversation(0, user_message)
print(f"Agent 0: {response_of_agent_0}")

# Private conversation between user and agent 1
user_message = ("Hello Agent 1, we know that Igor is dating Natasha and must bring her flowers. " +
                "You know that the florist has orchids and carnations available but you do not " +
                "know which flowers Natasha likes or dislikes. " +
                "You can ask other agents for help. " +
                "Either state the flowers Igor should purchase or ask Agent 0 to help you. " +
                f"If you need me to relay a message to Agent 0, please clearly say, {request_to_agent_0}. " +
                f"If you don't need Agent 0 to help you, state your answer and clearly say, {no_help_needed}."
                )
print(f"User: {user_message}")
response_of_agent_1 = env.private_conversation(1, user_message)
print(f"Agent 1: {response_of_agent_1}")

# If Agent 0 knows the answer, print it.  If Agent 0 does not know, have it
# ask Agent 1.

flag_valid_agent_0_response = False
flag_valid_agent_1_response = False
response_of_agent_0_to_agent_1 = None
response_of_agent_1_to_agent_0 = None

MAX_ITER = 5

message_to_confused_agent = (
    "If you know the answer, you indicate no need for help and answer the question. " +
    "If you do not know the answer, you must ask the other agent for help. " +
    "Your response was not valid.  Try again."
)

while not (flag_valid_agent_0_response or flag_valid_agent_1_response):

    flag_agent_0_asks_for_help = regex_call_agent_1.search(response_of_agent_0) is not None
    flag_agent_0_needs_no_help = regex_no_help_needed.search(response_of_agent_0) is not None

    flag_agent_1_asks_for_help = regex_call_agent_0.search(response_of_agent_1) is not None
    flag_agent_1_needs_no_help = regex_no_help_needed.search(response_of_agent_1) is not None

    flag_valid_agent_0_response = (
        not (
            flag_agent_0_asks_for_help and flag_agent_0_asks_for_help
        ) and (
            flag_agent_0_asks_for_help or flag_agent_0_needs_no_help
        )
    )
    flag_valid_agent_1_response = (
        not (
            flag_agent_1_asks_for_help and flag_agent_1_asks_for_help
        ) and (
            flag_agent_1_asks_for_help or flag_agent_1_needs_no_help
        )
    )

    if not flag_valid_agent_0_response:
        # Agent 0 is confused
        print(f"Agent 0 is confused: {response_of_agent_0}")
        print(f"User: {message_to_confused_agent}")
        response_of_agent_0 = env.private_conversation(0, message_to_confused_agent)
        print(f"Agent 0: {response_of_agent_0}")

    elif flag_agent_0_asks_for_help:

        print(f"Agent 0 to Agent 1: {response_of_agent_0}")
        # # Conversation between agent 0 and agent 1
        # message = "Hello Agent 1, I'm Agent 0. Can you
        # response = env.agent_to_agent_conversation(0,
        # print(f"Agent 1: {response}")
        response_of_agent_1_to_agent_0 = env.agent_to_agent_conversation(0, 1, response_of_agent_0)
        print(f"Agent 1 responses to Agent 0: {response_of_agent_1_to_agent_0}")

    elif flag_agent_0_needs_no_help:
        print(f"Agent 0 claims to know the answer: {response_of_agent_0}")
        continue # Skip remainder of loop kernel since Agent 0 thinks it has an answer.
    else:
        print("ERROR IN UNDERSTANDING AGENT 0 STATE!\n")


    if not flag_valid_agent_1_response:
        # Agent 1 is confused
        print(f"Agent 1 is confused: {response_of_agent_1}")
        print(f"User: {message_to_confused_agent}")
        response_of_agent_1 = env.private_conversation(1, message_to_confused_agent)
        print(f"Agent 1: {response_of_agent_1}")

    elif flag_agent_1_asks_for_help:

        print(f"Agent 1 to Agent 0: {response_of_agent_1}")
        # # Conversation between agent 0 and agent 1
        # message = "Hello Agent 1, I'm Agent 0. Can you
        # response = env.agent_to_agent_conversation(0,
        # print(f"Agent 1: {response}")
        response_of_agent_0_to_agent_1 = env.agent_to_agent_conversation(1, 0, response_of_agent_1)
        print(f"Agent 0 responses to Agent 1: {response_of_agent_0_to_agent_1}")

    elif flag_agent_1_needs_no_help:
        print(f"Agent 1 claims to know the answer: {response_of_agent_1}")
        continue  # Skip remainder of loop kernel since Agent 0 thinks it has an answer.
    else:
        print("ERROR IN UNDERSTANDING AGENT 1 STATE!\n")

    response_of_agent_0 = response_of_agent_0_to_agent_1
    response_of_agent_1 = response_of_agent_1_to_agent_0
