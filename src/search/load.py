import gzip
from lxml import etree
import time

# sample function using which you can extract information from the wikipidea data
def load_documents():
    documents = []
    start = time.time()
    with gzip.open('src/app/data/enwiki-latest-abstract24.xml.gz', 'rb') as f:
        doc_id = 0
        for _, element in etree.iterparse(f, events=('end',), tag='doc'):
            title = element.findtext('./title')
            url = element.findtext('./url')
            abstract = element.findtext('./abstract')
            content = (title+" "+abstract)
            documents.append((url, content))
            doc_id += 1
            if doc_id % 10000 == 0:
                print(f'Parsed {doc_id} documents', end='\r')
            if doc_id == 1100000:
                break
            element.clear()

    end = time.time()
    print(f'Parsing XML took {end - start} seconds')
    print(f"these are the documents baba {len(documents)}")
    return documents
