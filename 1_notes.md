Project needs to be using OPEN_API_KEY var name as langchain will be using it

# Intro
Langchain chain is a list of components combined into a sequence.
Output of one step, becomes input of next step

# Prompt templates
Prompt temples are basically a template steings like f" strings. Only diffrenece really si that they enforce that we provide the interpolated values and provide clear error messages if we dont

# LCEL - langChain Expression language
Used to build chains. | is a operator used to chain components together

# models
gpt-oss is generally god for agentic workflows


# observability with langSmith
You just need to add env variables as per langSmith docs. Rest will happen automatiaclly

# chain vs agent
Agent is diffrent from a achain as chain can use LLM for one of the components, while agent is deciding which step to choose.

chain = developer decides control flow
agent = LLM decides control flow

# ReAct Agent architecture. LLM first thinks what to do and then starts acting on it