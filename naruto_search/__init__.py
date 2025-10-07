from langchain.chains.qa_with_sources.stuff_prompt import template
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama

# just example of making our own runnable for LCEL
def custom_runnable_fn(x):
    print('\n ---> Howdy from runnable \n')
    return x

custom_runnable = RunnableLambda(custom_runnable_fn)


class NarutoSearch:
    ollama_valid_models: tuple[str] = ("llama3.2", "gemma3")
    open_ai_model: tuple[str] = ('gpt-5')
    model=None
    chain=None

    def __init__(self, model_name):
       self.model = self.get_model(model_name=model_name)
       template_in = self.get_template()
       self.chain = self.get_chain(self.model, template=template_in)

    summary_template = """
        Given the information {information} about the person I want you to create:
        1. A short summary of that person
        2. two interesting facts about them
    """

    information = """
        Naruto Uzumaki is the titular protagonist of the Naruto franchise,
         a mischievous but determined young ninja from the Hidden Leaf Village who aspires to become its leader, the Hokage. Ostracized in his youth because the Nine-Tailed Fox demon was sealed inside him at birth,
          he eventually becomes a hero, known as the Hero of the Hidden Leaf, and later serves as the Seventh Hokage, marrying Hinata Hyuga and fathering two children.
    """

    def get_model(self, model_name: str):
        if model_name in self.ollama_valid_models:
            return ChatOllama(temperature=0, model=model_name)
        if model_name in self.open_ai_model:
            return ChatOpenAI(temperature=0, model=model_name)

        raise ValueError('Model name not found')

    def get_template(self):
        # prompt template will add parameters to templates.
        # it is wrapper class around prompt
        # modern LLMs are more conversational. That is they accept list of messages and feel better in "context" of the conversation
        summary_prompt_template = PromptTemplate(
            input_variables=["information"],
            template=self.summary_template
        )
        return summary_prompt_template

    def get_chain(self, model, template):
        # LCEL syntax. Uses output of left component as a input of right component
        # LCEL considers runnables (that are functions wrapped to be piped) and pipe operator that connects them
        chain = template | custom_runnable | model
        return chain

    def query_character(self, character_name: str):
        response = self.chain.invoke(input={"information": character_name})
        return response