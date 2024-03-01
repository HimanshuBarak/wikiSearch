## Wikisearch


https://github.com/HimanshuBarak/wikiSearch/assets/66054954/c3724cb3-7b05-4135-b184-5f6fdd2d4660


A simple search engine writtten in python. Wikisearch allows you to search over 1 million + wikipedia documents and get a result within just <strong>1 sec</strong>. 

## Working
### Indexing Documents: 
The search engine allows for indexing web pages or documents by storing the content of each document associated with a unique URL. This process involves normalizing the content (e.g., removing punctuation, converting to lowercase) to ensure consistency and effectiveness in keyword matching.

### Creating an Inverted Index: 
For each indexed document, the engine updates an inverted index that maps each unique word to a list of URLs where that word appears, along with the frequency of its appearance in each document. This data structure is crucial for efficient retrieval of documents based on keyword searches.

### Querying for Documents: 
Users can query the search engine with specific keywords. The engine uses the inverted index to quickly find and retrieve all documents containing those keywords, leveraging the precomputed word-to-URL mappings.

### Ranking with BM25: 
The engine employs the BM25 algorithm to rank the relevance of documents to a query. It calculates scores for each document based on the frequency of query terms within the document, the length of the document, and the average document length across the entire dataset, incorporating tunable parameters to adjust the influence of term frequency and document length.

### Comprehensive Search Results: 
By combining the inverted index for fast lookup and BM25 for relevance scoring, the search engine is capable of processing complex queries, ranking documents by relevance, and returning a list of URLs that best match the user's query. This ensures that users receive accurate and contextually relevant results for their searches.
## Getting started

#### Clone this repo

```bash
git clone https://github.com/HimanshuBarak/wikiSearch.git
```

#### Create the and activate the conda Environment ( use virtual env in case you don't have conda installed)
```
conda create -n wikiSearch python=3.10
```

#### Install dependencies

```
pip install pdm
```
```
pdm install
```

#### Running the Fast API app

```
uvicorn app.app:app --reload
```

#### Running the Script
```
python src/search/run.py
```

#### Running the app (if you have docker)
```
docker-compose up --build
```
