
from src.search.engine import SearchEngine
from src.search.timing import timing
engine = SearchEngine()

# sample file to run the search engine using your terminal
# To do : allow search query to be sepcifed using the cli and allow multiple search queries


@timing
def get_top_urls(scores_dict: dict, n: int):
    """
    Returns the top n URLS from the results
    """
    sorted_urls = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
    top_n_urls = sorted_urls[:n]
    top_n_dict = dict(top_n_urls)
    return top_n_dict


if __name__ == '__main__':
    query = "Procrastination"
    results = engine.handle_search(query)
    results = get_top_urls(results, n=5)
    print(results)