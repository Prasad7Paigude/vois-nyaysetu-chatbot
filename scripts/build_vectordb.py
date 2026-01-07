from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from load_documents import load_documents

DATA_FILES = [
    "../data/normalized_ipc.json",
    "../data/normalized_crpc.json",
    "../data/normalized_glossary.json",
    "../data/normalized_amendments.json"
]

all_docs = []
for path in DATA_FILES:
    all_docs.extend(load_documents(path))

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma.from_documents(
    documents=all_docs,
    embedding=embeddings,
    persist_directory="chroma_day1",
    collection_name="legal_knowledge"
)


vectordb.persist()

print(f"Vector DB created with {len(all_docs)} documents.")
print("DB COUNT:", vectordb._collection.count())

