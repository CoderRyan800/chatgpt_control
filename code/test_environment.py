# test_environment.py

import os
from environment import Environment

def test_agent_instantiation():
    env = Environment(3)
    assert len(env.agents) == 3

def test_agent_message_passing():
    env = Environment(3)
    env.send_message('User', 'Agent 1', 'Hello, Agent 1!')
    env.send_message('Agent 1', 'Agent 2', 'Hello, Agent 2!')

def test_user_message_passing():
    env = Environment(3)
    env.send_message('User', 'All Agents', 'Hello, everyone!')

def test_agent_memory_file_creation():
    env = Environment(3)
    env.send_message('User', 'Agent 1', 'Hello, Agent 1!')
    assert os.path.exists('agent_1_memory.txt')

if __name__ == "__main__":
    test_agent_instantiation()
    test_agent_message_passing()
    test_user_message_passing()
    test_agent_memory_file_creation()
