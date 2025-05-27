import os 
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from langchain_text_splitters import RecursiveCharacterTextSplitter


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "funny_stories"
CHUNK_SIZE = 500 



def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
      reader = PdfReader(pdf_path)
      text = ""
      for page in reader.pages:
          text += page.extract_text() + "\n"
      return text.strip()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""
    
def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Split text into chunks of a specified size."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=50,  # Overlap of 50 characters
        length_function=len
    )
    return text_splitter.split_text(text)


def load_stories_to_chroma(folder="pdfs"):   # importing this function in main file
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = SentenceTransformer(embedding_model_name)
    
    client = PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            full_text = extract_text_from_pdf(path)
            chunks = chunk_text(full_text)
            print(f"Processing {file} with {len(chunks)} chunks.")

            for i, chunk in enumerate(chunks):
                doc_id = f"{file}_{i}"
                embedding = model.encode(chunk).tolist()
                collection.add(
                    documents=[chunk],
                    metadatas=[{"filename": file, "chunk": i}],
                    embeddings=[embedding],
                    ids=[doc_id]
                )
            print(f"Added {file} to ChromaDB.")
                
        else:
            print(f"No text extracted from {file}.")
    print("All stories loaded into ChromaDB.")