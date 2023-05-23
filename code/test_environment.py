import os
from environment import Environment

def test_environment():
    num_agents = 5
    recursive_limit = 10
    environment = Environment(num_agents, recursive_limit)

    # Send a message to all agents
    environment.send_message("User", "All Agents", "Hello, All Agents")

    # Verify that the message has been added to all agents' memory
    for i in range(num_agents):
        agent_memory = environment.agents[i].get_memory()
        assert agent_memory[-1]["content"] == "Hello, All Agents", f"Agent {i} did not receive the broadcast message"

    # Send a message to Agent 1
    environment.send_message("User", "Agent 1", "Hello, Agent 1")

    # Verify that the message has been added to Agent 1's memory
    agent_1_memory = environment.agents[1].get_memory()
    assert agent_1_memory[-1]["content"] == "Hello, Agent 1", "Agent 1 did not receive the directed message"

    # Verify that the message has not been added to other agents' memory
    for i in [0, 2, 3, 4]:
        agent_memory = environment.agents[i].get_memory()
        assert agent_memory[-1]["content"] != "Hello, Agent 1", f"Agent {i} incorrectly received the directed message to Agent 1"

if __name__ == "__main__":
    test_environment()
