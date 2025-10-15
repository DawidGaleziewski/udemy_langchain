from dotenv import load_dotenv

from search_agent.prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS

load_dotenv()

# used to run community made prompts
from langchain import hub

# runtime of the agent. It is going to make the actuall calls
from langchain.agents import AgentExecutor

# creat react agent creates a chain. It recives a LLM model and makes it a agent (able to decide for itself what it wants to do). Tells LLM what we need to run
from langchain.agents.react.agent import create_react_agent

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from langchain_core.tools import tool

# tool we connect to agent to allow it to search the internet
from langchain_tavily import TavilySearch

# paring our responses.
from langchain_core.output_parsers import PydanticOutputParser

# create template in langchain-friendly format
from langchain_core.prompts import PromptTemplate

# custom runnable lambda we can add to the chain
from langchain_core.runnables import RunnableLambda, RunnableSerializable

from .schemas import AgentResponse


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

    # this generally will be more realiable. It is using LLM function call. This also saves us tokens
    def get_structured_llm(self, llm, tools):
        react_prompt = hub.pull("hwchase17/react-chat")
        react_prompt_with_format_instruction = PromptTemplate(
            template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
            input_variables=["input", "agent_scratchpad", "tool_names"],
            # partial prefils some values
        ).partial(format_instruction='')

        agent = create_react_agent(
            llm=llm, prompt=react_prompt_with_format_instruction, tools=tools
        )
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # We use LLMs build in method for serializing the data. This will create a instance of the model that will only return specific schema
        structured_llm = llm.with_structured_output(AgentResponse)
        extract_output = RunnableLambda(lambda x: x["output"])
        chain = agent_executor | extract_output | structured_llm
        return chain


    # Custom approach to customisation of data. We can implement this no matter the model. Problem is it will pass information that is not usefull across agent calls. Also if LLm is not the "best" quality it may simply fail at parsing
    def custom_parser(self, llm, tools) -> RunnableSerializable:
        # alternative is to use ready prompt
        # react_prompt = hub.pull("hwchase17/react-chat")

        # this will use our pydantic schema for data serialisation/validation
        output_parser = PydanticOutputParser(pydantic_object=AgentResponse)

        # practical way of using runnable lambdas is to transform data. So output of one LLM operation, formated by pydantic, can be formated and put into next sequence
        extract_output = RunnableLambda(lambda x: x["output"])
        parse_output = RunnableLambda(lambda x: output_parser.parse(x))

        # Our custom prompt, we coppied and changed. We use PromptTemplate to make it into better format for langchain
        react_prompt_with_format_instruction = PromptTemplate(
            template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
            input_variables=["input", "agent_scratchpad", "tool_names"],
            # partial prefils some values
        ).partial(format_instruction=output_parser.get_format_instructions())

        # creates a reasoning agent. This return a Runnable (chain) and allows LLM to reason and act (react)
        agent = create_react_agent(
            llm=llm, prompt=react_prompt_with_format_instruction, tools=tools
        )

        # agent executor is quite simple. This is really a while loop that will run this chain over and over again
        # as simple as it is, it is a orchestrator, giving the agent ability to call tools provided
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        chain = agent_executor | extract_output | parse_output

        return  chain

    def main(self):
        llm = ChatOpenAI(model="gpt-4")
        tools = [TavilySearch()]

        # requires gpt-4
        # chain = self.custom_parser(llm=llm, tools=tools)

        # requires gpt-5
        chain = self.get_structured_llm(llm=llm, tools=tools)
        result = chain.invoke(
            input={"input": "Search linkedin for react jobs",
                   "chat_history": []}
        )
        print("howdy", result)


if __name__ == "__main__":
    sa = SearchAgent()
    sa.main()
