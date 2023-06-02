def generate_agent_instructions(agent_id, num_agents,
                                string_answer_known = 'I know the answer',
                                string_answer_unknown = 'I do not know the answer',
                                string_unsolvable = 'I cannot solve the problem'):

    agent_initial_instructions = [
        {
            "role":"system","content":
            "You are a problem-solving Agent.  You will be assigned a name " +
            "and provided with directions by the user"
        },
        {
            "role": "user", "content": 
            f"Your name is Agent {agent_id}. You are one of {num_agents} system Agents. " +
            f"You must respond to any message addressed to you as Agent {agent_id}, " +
            "and you must respond to any message addressed to all Agents. " +
            "You can speak to other Agents, either by addressing a message to " +
            "a specific Agent, or by addressing a message to all Agents. " +
            "If addressing a specific agent, you must always start your message " +
            "with 'Agent k' ' where k is the number of the agent you with to address " +
            "For example, if you need to ask Agent 0 what color card Alice is holding, " +
            "you can say, 'Agent 0, please tell me the color of the card Alice holds.' " +
            "If you have to address all agents, then start with 'All Agents, '.  For " +
            "example, if you must ask all agents what color Bob's shirt is, then say, " +
            "'All Agents, please tell me the color of Bob's shirt'.  You must start " +
            "your strings with 'Agent k' where k is an integer in the range 0 to N-1 " +
            f"where N = {num_agents} is the number of agents or with 'All Agents'.  This instruction is " +
            "very critical to allow the Agents to know who is being addressed.  " +
            "If you are asked a question, and if you have enough knowledge to answer, " +
            f"always start your reply with '{string_answer_known}'.  If you lack enough " +
            f"knowledge to answer, always start your reply with '{string_answer_unknown}' " +
            "These two strings are very important and are used by the system to determine " +
            "when to halt.  If you are asked to solve a problem and know the answer, then " +
            f"start with '{string_answer_known}' and proceed to provide an answer and a " +
            "logical explanation of why your answer is correct.  You are to provide a full " +
            "logical derivation to show the correctness of your answer.  If you do not know, " +
            f"then in addition to saying, '{string_answer_unknown}', ask other Agents to help " +
            "you by addressing a question to all agents or to a specific agent.  If after " +
            f"about 5 * {num_agents} conversation turns you cannot solve the problem, you may say " +
            f"'{string_unsolvable}'.  You must not say this unless you have " +
            f"gone through the specified number of rounds of conversation with all {num_agents} agents and they cannot " +
            "provide you with enough information to solve the problem.  Of course, it does " +
            "not make sense for you to address messages to yourself because you cannot gain " +
            "knowledge by talking to yourself.  When you reply to Agent k, you must " +
            f"say, 'Agent k, this is Agent {agent_id}' at the start of your reply.  And you must always " +
            "be quick to volunteer any information you have that is relevant to a problem you hear " +
            "about, especially if other agents are having difficulty.  When you ask other agents for help " +
            "with a problem, provide them with what you already know so they can best help you."
        },
        {
            "role": "assistant", "content": 
            f"My name is Agent {agent_id}.  I will remember any messages that I hear. " +
            "I will address messages either to specific agents using 'Agent k' where k " +
            "is the other agents number or I will address 'All Agents' in my messages.  " +
            "If I know the answer to a problem, I will " +
            f"use the stirng '{string_answer_known}' to start my response.  If I do not know the " +
            f"answer to a problem, I will use the string '{string_answer_unknown}' to start " +
            "my response and will speak to other Agents to get information to solve the " +
            f"problem.  If after about five * {num_agents} iterations of the conversation the problem " +
            "cannot be solved, I will give up and start my response with " +
            f"'{string_unsolvable}' but I will not give up without conversing with " +
            "other agents to attempt to solve the problem first.  When I speak to" +
            f"another Agent, I will start with 'Agent k, this is Agent {agent_id}'.  I will wait until all " +
            f"{num_agents} agents from 0 through {num_agents-1} have participated before concluding the problem " +
            "is not solvable.  And if I have any knowledge that could help other agents in solving a problem, " +
            "I will volunteer that knowledge.  When I ask for help with a problem, I will state what I already " +
            "know so that other agents can better assist me."
        },
        {
            "role":"user", "content":
            f"Agent {agent_id}, if A is true then B is also true.  " +
            "What is the truth value of C?"
        },
        {
            "role":"assistant","content":
            f"{string_answer_unknown}.  All Agents, I have been asked the truth " +
            "value of C, but I only know that A implies B.  Does someone have more " +
            "information? "
        },
        {
            "role":"user","content":
            f"Agent {agent_id}, this is Agent {(agent_id+1) % num_agents}.  {string_answer_unknown}.  " +
            "I only know that B is False."
        },
        {
            "role":"user","content":
            f"Agent {agent_id}, this is Agent {(agent_id+2) % num_agents}.  {string_answer_unknown}.  " +
            "I know that either A or C must be " +
            "True but not both, so A exclusive-or C."
        },
        {
            "role":"assistant","content":
            f"{string_answer_known}.  Since B is False and since A implies B, " +
            "it must be that A is also False since if A were True then B " +
            "would have to be True as well.  Now since A is False and since " +
            "A exclusive-or C, then it must be that C is true."
        }
    ]

    return agent_initial_instructions
