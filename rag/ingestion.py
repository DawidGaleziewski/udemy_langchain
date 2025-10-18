from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

if __name__ == "__main__":
    loader = TextLoader("/mnt/c/Users/Dawid/Desktop/projects/udemy_langchain/rag/medium.txt")
    document = loader.load()
    # good rule of thumb is to keep chunk size so it will fit in context window, and big enought to know what it means (for us as humman)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    texts= text_splitter.split_documents(document)
    print(f'split created {len(texts)} chunks')