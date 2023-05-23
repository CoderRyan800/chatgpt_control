def test_environment():
    environment = Environment(5, 10)

    assert os.path.isfile("agent_0_memory.txt")
    assert os.path.isfile("agent_1_memory.txt")
    assert os.path.isfile("agent_2_memory.txt")
    assert os.path.isfile("agent_3_memory.txt")
    assert os.path.isfile("agent_4_memory.txt")

    environment.send_message("Hello, All Agents", "All Agents")
    environment.send_message("Hello, Agent 1", "Agent 1")

test_environment()
