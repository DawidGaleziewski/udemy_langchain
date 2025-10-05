from dotenv import load_dotenv
import os

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama

load_dotenv()


# prompt template will add parameters to templates.
# it is wrapper class around prompt
# modern LLMs are more conversational. That is they accept list of messages and feel better in "context" of the conversation

# just example of making our own runnable for LCEL
def custom_runnable_fn(x):
    print('\n ---> Howdy from runnable \n')
    return x

custom_runnable = RunnableLambda(custom_runnable_fn)

def main():
    print("Hello from udemy-langchain!")

    information = """
        Naruto Uzumaki is the titular protagonist of the Naruto franchise,
         a mischievous but determined young ninja from the Hidden Leaf Village who aspires to become its leader, the Hokage. Ostracized in his youth because the Nine-Tailed Fox demon was sealed inside him at birth,
          he eventually becomes a hero, known as the Hero of the Hidden Leaf, and later serves as the Seventh Hokage, marrying Hinata Hyuga and fathering two children.
    """

    summary_template = """
        Given the information {information} about the person I want you to create:
        1. A short summary of that person
        2. two interesting facts about them
    """

    # this could be just a f" lol
    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template
    )
    # llm = ChatOllama(temperature=0, model="gemma3")
    # llm = ChatOllama(temperature=0, model="llama3.2")
    llm = ChatOpenAI(temperature=0, model="gpt-5")

    # LCEL syntax. Uses output of left component as a input of right component
    # LCEL considers runnables (that are functions wrapped to be piped) and pipe operator that connects them

    chain = summary_prompt_template | custom_runnable | llm

    response = chain.invoke(input={"information": information})
    print(response)

if __name__ == "__main__":
    main()
