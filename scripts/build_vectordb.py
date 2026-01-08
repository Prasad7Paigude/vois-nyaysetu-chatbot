from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from load_documents import load_documents

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

DATA_FILES = [
    DATA_DIR / "normalized_ipc.json",
    DATA_DIR / "normalized_crpc.json",
    DATA_DIR / "normalized_glossary.json",
    DATA_DIR / "normalized_amendments.json"
]

# Load all documents
all_docs = []
for path in DATA_FILES:
    all_docs.extend(load_documents(path))

# Use REMOTE embeddings (same as runtime)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# Build and persist vector DB
vectordb = Chroma.from_documents(
    documents=all_docs,
    embedding=embeddings,
    persist_directory="chroma_day1",
    collection_name="legal_knowledge"
)

vectordb.persist()

print(f"Vector DB created with {len(all_docs)} documents.")
print("DB COUNT:", vectordb._collection.count())
