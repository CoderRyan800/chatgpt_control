import pytest
import openai
import unittest
import unittest.mock as mock
from agent import Agent

# Mock the OpenAI API
openai.ChatCompletion.create = mock.Mock()


def test_agent_initialization():
    agent = Agent(1, 5)

    assert agent.id == 1
    assert agent.num_agents == 5
    assert agent.flag_problem_solved is False
    assert agent.flag_problem_failed is False
    assert agent.n_initial_messages == 0
    
    expected_memory = [
        {"role": "system", "content": "You are a problem-solving Agent."},
        {"role": "user", "content":
            f"Your name is Agent 1. You are one of 5 system Agents. "
            f"You must respond to any message addressed to you as Agent 1, "
            f"and you must respond to any message addressed to all Agents. "
            f"You must not respond to a message addressed to another agent, "
            f"but you must remember it."
        }
    ]
    
    unittest.TestCase().assertListEqual(agent.memory, expected_memory)


def test_add_message():
    agent = Agent(1, 5)

    agent.add_message("user", "This is a test message.")
    assert agent.memory[-1] == {"role": "user", "content": "This is a test message."}

    agent.add_message("system", "Another test message.")
    assert agent.memory[-1] == {"role": "system", "content": "Another test message."}


def test_respond():
    agent = Agent(1, 5)

    # Mock the response of the OpenAI API
    openai.ChatCompletion.create.return_value = mock.Mock(
        choices=[mock.Mock(message={"content": "Test response"})]
    )

    response = agent.respond("Test message")
    assert response == "Test response"
    assert agent.memory[-1] == {"role": "user", "content": "Test message"}


def test_problem_solved():
    agent = Agent(1, 5)

    openai.ChatCompletion.create.return_value = mock.Mock(
        choices=[mock.Mock(message={"content": "I know the answer"})]
    )
    agent.respond("Test message")
    assert agent.flag_problem_solved is True

def test_problem_failed():
    agent = Agent(1, 5)

    openai.ChatCompletion.create.return_value = mock.Mock(
        choices=[mock.Mock(message={"content": "I do not know the answer"})]
    )
    agent.respond("Test message")
    assert agent.flag_problem_failed is False

    agent.n_initial_messages = 5 * agent.num_agents + 1

    openai.ChatCompletion.create.return_value = mock.Mock(
        choices=[mock.Mock(message={"content": "Test response"})]
    )
    agent.respond("Test message")
    assert agent.flag_problem_failed is True
