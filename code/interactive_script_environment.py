# interactive_script.py

from environment import Environment

def main():
    num_agents = 3
    recursive_limit = 10
    env = Environment(num_agents, recursive_limit)

    while True:
        user_input = input("Enter your message (type 'exit' to end): ")
        if user_input.lower() == 'exit':
            break

        recipient = input("Enter the recipient ('Agent n' or 'All Agents'): ")
        env.send_message(user_input, recipient)

if __name__ == "__main__":
    main()
