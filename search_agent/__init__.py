from dotenv import load_dotenv
load_dotenv()

# used to run community made prompts
from langchain import hub

# runtime of the agent. It is going to make the actuall calls
from langchain.agents import AgentExecutor

# creat react agent creates a chain. It recives a LLM model and makes it a agent (able to decide for itself what it wants to do). Tells LLM what we need to run
from langchain.agents.react.agent import create_react_agent

from  langchain_openai import  ChatOpenAI
from dotenv import load_dotenv

from langchain_core.tools import tool

# tool we connect to agent to allow it to search the internet
from langchain_tavily import  TavilySearch

# this is how we can make any function a tool. By decorator. Description will provide info to the LLM on when to use the tool and what is it
@tool(description="A tool for multiplying two ints")
def multiply(a: int, b: int) -> int:
    return a * b

# langchain hub will allow us to expploire commuity made prompts
# TAVILY_API_KEY
class SearchAgent:
    # tools that LLM can use
    # model does not execute the tool itself. It just creates arguments for the tool call
    # system running langchain will execute the tool and propagate the answer back to the model
    # react_prompt = None
    # llm=None

    def main(self):
        llm=ChatOpenAI(model="gpt-4")
        react_prompt= hub.pull("hwchase17/react-chat")
        tools = [TavilySearch()]
        # creates a reasoning agent. This return a Runnable (chain) and allows LLM to reason and act (react)
        agent = create_react_agent(llm=llm, prompt=react_prompt, tools=tools)
        # agent executor is quite simple. This is really a while loop that will run this chain over and over again
        # as simple as it is, it is a orchestrator, giving the agent ability to call tools provided
        chain = AgentExecutor(agent=agent, tools=tools, verbose=True)
        result = chain.invoke(
            input={
                "input": "Search linkedin for react jobs",
                "chat_history": []
            }
        )
        print('howdy', result)

if __name__ == "__main__":
    sa = SearchAgent()
    sa.main()
