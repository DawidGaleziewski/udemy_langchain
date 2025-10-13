from dotenv import load_dotenv

load_dotenv()
from naruto_search import NarutoSearch
from search_agent import SearchAgent


def main():
    # naruto_search = NarutoSearch('gpt-5')
    # print(naruto_search.query_character("Naruto"))

    sa = SearchAgent()
    sa.main()


if __name__ == "__main__":
    main()
