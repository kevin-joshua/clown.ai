from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings



def load_chroma():
  """Load the Chroma vector store."""
  embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

  db = Chroma(
      collection_name="funny_stories",
      embedding_function=embedding_model,
      persist_directory="chroma_db",
  )
  return db


def query_db(query, k=5):
    """Perform max marginal relevance search query on the Chroma vector store."""
    db = load_chroma()
    print(f"[✓] Loaded Chroma vector store with {db._collection.count()} documents.")
    
    # Simple similarity search, no lambda_mult or fetch_k needed
    results = db.max_marginal_relevance_search(
        query=query,
        k=k,
        lambda_mult=0.8,  # Adjust this value as needed
        fetch_k=20  # Fetch more documents to ensure we get enough results
    )
    print(f"[✓] {len(results)} mmr search results found.")
    for doc in results:
        print(doc.page_content[:100] + "...")  # Print first 100 chars of each result
    return results
