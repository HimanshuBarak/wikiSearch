import re 
import string 



STOPWORDS = set(['the','is','what', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
                 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
                 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'wikipedia'])
PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))
# STEMMER = Stemmer.Stemmer('english')


def tokenize(text):
    return text.split()


def lowercase_filter(tokens):
    return [token.lower() for token in tokens]


def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]


def stopword_filter(tokens):
    return [token for token in tokens if token not in STOPWORDS]

# def stem_filter(tokens):
#     return STEMMER.stemWords(tokens)


def update_url_scores(old: dict[str, float], new: dict[str, float]):
    """
    this function allows us to aggregate scores for the given url across the keywords present in the dicitonary
    """
    for url, score in new.items():
        if url in old:
            old[url] += score
        else:
            old[url] = score
    return old


def get_top_urls(scores_dict: dict, n: int):
    """
    Returns the top n URLS from the results
    """
    sorted_urls = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
    top_n_urls = sorted_urls[:n]
    top_n_dict = dict(top_n_urls)
    return top_n_dict


def normalize_string(input_string: str) -> str:
    """
    Convert the string into lowercase tokens and removes punctuation and repetitve words 
    """
    tokens = tokenize(input_string)
    tokens = lowercase_filter(tokens)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    # tokens = stem_filter(tokens)
    return [token for token in tokens if token]