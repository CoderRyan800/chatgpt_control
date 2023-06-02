# chatgpt_control

## Goals

1. Create ChatGPT-based agents that exhibit epistemic self-awareness.  These agents must be aware of their own stage of knowledge and of possible states of knowledge of others.  Knowledge of what one knows and does not know, combined with communication with other knowledge agents, is the key to collaborative problem solving.  This is the first goal.
2. The second goal is to create agents that are able to control the execution of a Python program.  This is important as we wish to use agents as program decision and flow control elements.

### Epistemic self-awareness.

As of 1 June 2023, we have simulated a five agent system in which agent's are asked to solve a very simple logic puzzle.  Agents are numbered 0 through 4, and only agents
0 and 3 have the pieces needed to solve the puzzle.  The agents collaborate and communicate in order to solve the problem.  We have saved their conversational memory dumps as proof
that they are aware of their own knowledge states and that they can use this knowledge to facilitate collaborative problem solving.

1. The problem is that Igor is dating Natasha and has to purchase flowers for her.  There is only one florist available.
2. Agent 0 knows only that Natasha likes roses and orchids but not carnations.  Agent 0 does not know what the florist has in stock.
3. Agent 3 knows only that the florist has carnations and orchids but does not know Natasha's flower preferences.
4. Agents 1, 2, and 4 know neither Natasha's flower preferences nor the florist's inventory.
5. The five agents are asked to help Igor select flowers for Natasha.

We observe in the final memory dumps of the agents that no one agent has sufficient knowledge to solve the problem, and each agent
exhibits awareness of lacking adequate knowledge to solve the problem.  This knowledge drives the agents to ask each other for help and
to share the knowledge they do have.  When the knowledge from Agent 0 and from Agent 3 both become known, the agents are able to solve the
problem and recommend that Igor purchase orchids for Natasha.  Here, agents realize they lack enough knowledge to solve the problem,
and when enough knowledge is available, they are able to confidently give advice to Igor.  Agents act based on knowledge of their
state of knowledge, which is a limited form of self-awareness.

### Program control

No progress here as of 1 June 2023.
