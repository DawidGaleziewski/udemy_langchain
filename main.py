from dotenv import load_dotenv
from naruto_search import NarutoSearch

load_dotenv()

def main():
    naruto_search = NarutoSearch('gpt-5')
    print(naruto_search.query_character("Naruto"))

if __name__ == "__main__":
    main()
