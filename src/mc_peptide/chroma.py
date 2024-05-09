import pprint
import chromadb

pp = pprint.PrettyPrinter()

client = chromadb.HttpClient()
# collection = client.create_collection("collection")
collection = client.get_collection("collection")

# Add docs to the collection. Can also update and delete. Row-based API coming soon!
collection.delete(
    ids=["doc1", "doc2"], # must be unique for each doc 
)
collection.add(
    documents=["This is document1. It's about cats. Cats, cats, cats.", "This is document2. It's about dogs. Dogs, dogs, dogs."], # we embed for you, or bring your own
    metadatas=[{"source": "notion"}, {"source": "google-docs"}], # filter on arbitrary metadata!
    ids=["doc1", "doc2"], # must be unique for each doc 
)

query = "Woof woof."
results = collection.query(
    query_texts=[query],
    n_results=2,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
)  

print(f"Query: {query}\n")
pp.pprint(results)
