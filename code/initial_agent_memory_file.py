import json
from agent_instructions import *

def generate_agent_initial_memory(agent_id):

    memory_filename = f'agent_{agent_id}_memory.txt'

    instruction_json = generate_agent_instructions(agent_id=agent_id)

    with open(memory_filename,'w') as fp:
        fp.write(json.dumps(instruction_json,indent=4))

def main():

    num_agents = 5

    for agent_id in range(num_agents):
        generate_agent_initial_memory(agent_id=agent_id)

if __name__ == "__main__":
    main()
