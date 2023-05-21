from agent import Agent

def save_memory_and_exit(agent):
    # Save agent's memory to a file
    with open("agent_memory.txt", "w") as file:
        for message in agent.get_memory():
            file.write(f"{message['role']}: {message['content']}\n")
    print("Agent memory saved. Exiting...")

def main():
    num_agents = 5  # Specify the number of agents
    agent_id = 0  # Specify the ID of the current agent

    agent = Agent(agent_id, num_agents)

    print("Welcome to the Agent Chat!")
    print("Instructions:")
    print(f"1. You are Agent {agent_id}.")
    print("2. Address the agent using 'Agent k' where k is the agent number.")
    print("3. Address all agents using 'All Agents'.")
    print("4. Type 'SAVE MEMORY AND EXIT' to save the agent's memory and exit the program.")

    while True:
        message = input("> ")

        if message == "SAVE MEMORY AND EXIT":
            save_memory_and_exit(agent)
            break

        response = agent.respond(message)
        print(response)

if __name__ == "__main__":
    main()
