from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings



if __name__ == "__main__":
    loader = TextLoader("/mnt/c/Users/Dawid/Desktop/projects/udemy_langchain/rag/medium.txt")
    document = loader.load()