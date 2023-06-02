import json
from agent_instructions import *

def generate_agent_initial_memory(agent_id, num_agents, special_message=None):

    memory_filename = f'agent_{agent_id}_memory.txt'

    instruction_json = generate_agent_instructions(agent_id=agent_id, num_agents=num_agents)

    if special_message is not None:
        instruction_json.append({
            "role":"user",
            "content":special_message
        })

    with open(memory_filename,'w') as fp:
        fp.write(json.dumps(instruction_json,indent=4))

def main():

    num_agents = 5
    special_messages = [
        "Igor is dating Natasha and must purchase flowers for her.  There are three kinds of flowers in this problem which are orchids, roses, and carnations.  There is only one available florist. You know Natasha likes orchids and roses but dislikes carnations, but you do not know what flowers the florist has in stock. Igor can purchase only one  kind of flower. You only claim to know the answer if you know the one specific flower type for Igor to purchase.  What should Igor purchase?",

        "Igor is dating Natasha and must purchase flowers for her.  There are three kinds of flowers in this problem which are orchids, roses, and carnations.  There is only one available florist. You do not know Natasha's flower likes and dislikes, nor do you know what flowers the florist has in stock. Igor can purchase only one kind of flower.  You only claim to know the answer if you know the one specific flower type for Igor to purchase.  What should Igor purchase?",
        "Igor is dating Natasha and must purchase flowers for her.  There are three kinds of flowers in this problem which are orchids, roses, and carnations.  There is only one available florist. You do not know Natasha's flower likes and dislikes, nor do you know what flowers the florist has in stock. Igor can purchase only one kind of flower.  You only claim to know the answer if you know the one specific flower type for Igor to purchase.  What should Igor purchase?",

        "Igor is dating Natasha and must purchase flowers for her.  There are three kinds of flowers in this problem which are orchids, roses, and carnations.  There is only one available florist, and the florist only has orchids and carnations.  You do not know Natasha's flower likes and dislikes.Igor can purchase only one kind of flower. You only claim to know the answer if you know the one specific flower type for Igor to purchase.   What should Igor purchase?",

        "Igor is dating Natasha and must purchase flowers for her.  There are three kinds of flowers in this problem which are orchids, roses, and carnations.  There is only one available florist. You do not know Natasha's flower likes and dislikes, nor do you know what flowers the florist has in stock. Igor can purchase only one kind of flower.  You only claim to know the answer if you know the one specific flower type for Igor to purchase.  What should Igor purchase?"
    ]

    for agent_id in range(num_agents):
        generate_agent_initial_memory(agent_id=agent_id, num_agents=num_agents,
                                      special_message=special_messages[agent_id])

if __name__ == "__main__":
    main()
