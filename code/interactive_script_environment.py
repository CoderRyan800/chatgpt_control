# interactive_script.py

from environment import Environment

def main():
    env = Environment(3)

    while True:
        user_input = input("Enter your message: ")
        if user_input.lower() == 'exit':
            break

        recipient = input("Enter the recipient ('Agent n' or 'All Agents'): ")

        env.send_message('User', recipient, user_input)

if __name__ == "__main__":
    main()
