from collections import defaultdict
from math import log
import json
import redis
from src.search.load import load_documents
from src.search.timing import timing
from src.search.engine_utils import normalize_string, update_url_scores, get_top_urls
import time


class SearchEngine:
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0, k1: float = 1.5, b: float = 0.75):
        self.redis_client = redis.Redis(
            host=redis_host, port=redis_port, db=redis_db)
        self.k1 = k1
        self.b = b
        self._documents = {}   # stores all the documents
        self._index = defaultdict(lambda: defaultdict(int))

    @property
    def posts(self) -> list[str]:
        return list(self._documents.keys())

    @property
    def number_of_documents(self) -> int:
        return len(self._documents)

    @property
    def avdl(self) -> float:
        cached_avdl = self.redis_client.get("avdl")
        if cached_avdl is not None:
            return float(cached_avdl)
        calculated_avdl = sum(
            len(d) for d in self._documents.values()) / len(self._documents)
        self.redis_client.set("avdl", calculated_avdl)
        return calculated_avdl

    def get_documents(self):
        """
        Retrieve the documents from Redis and deserialize them
        """
        documents_json = self.redis_client.get("documents")
        if documents_json:
            return json.loads(documents_json)
        else:
            return {}

    def set_documents(self, documents):
        """
        Serialize the documents and saves them to Redis 
        """
        documents_json = json.dumps(documents)
        self.redis_client.set("documents", documents_json)


    def idf(self, kw: str) -> float:
        """
        using idf we calculate the priority of the word the more the words appears in the many documents less important it is
        """
        N = self.number_of_documents
        n_kw = len(self.get_urls(kw))
        return log((N - n_kw + 0.5) / (n_kw + 0.5) + 1)


    def bm25(self, kw: str) -> dict[str, float]:
        """
        we use bm25 to rank the retreived documents 
        """
        result = {}
        idf_score = self.idf(kw)
        avdl = self.avdl
        for url, freq in self.get_urls(kw).items():
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (
                1 - self.b + self.b * len(self._documents[url]) / avdl
            )
            result[url] = idf_score * numerator / denominator
        return result


    def search(self, query: str) -> dict[str, float]:
        """
        Defines a method search that takes a query string as input and returns a dictionary mapping URLs 
        (as strings) to their scores (as floats).
        """
        keywords = normalize_string(query)
        url_scores: dict[str, float] = {}
        for kw in keywords:
            kw_urls_score = self.bm25(kw)
            url_scores = update_url_scores(url_scores, kw_urls_score)
        return url_scores


    def index(self, url: str, content: str) -> None:
        """
        basically stores the word and their frequency in each docuemnt
        """
        self._documents[url] = content
        words = normalize_string(content)
        for word in words:
            self._index[word][url] += 1


    def bulk_index(self, documents: list[tuple[str, str]]):
        """
        process all document to creare the index
        """
        for url, content in documents:
            self.index(url, content)


    def store_index(self):
        """
        caches the calculated index in redis
        """
        i = 0
        for key, value in self._index.items():
            self.redis_client.set(key, json.dumps(value))
            i = i+1
            if i % 10000 == 0:
                print(f"indexed {i} words ", end="\r")


    def get_urls(self, keyword: str) -> dict[str, int]:
        """
        retreives all the documents which contain the given keyword
        """
        keyword = normalize_string(keyword)[0]
        urls = self.redis_client.get(keyword)
        if urls:
            return json.loads(urls)
        else:
            return {}


    @timing
    def handle_search(self, query, n):
        start = time.time()
        docs = self.get_documents()
        if docs == {}:
            documents = load_documents()
            self.bulk_index(documents)
            self.store_index()
            self.set_documents(self._documents)
        else:
            self._documents = docs
        results = self.search(query)
        end = time.time()
        results = get_top_urls(results, n)
        resp_time = end-start
        return results, resp_time


engine = SearchEngine()
