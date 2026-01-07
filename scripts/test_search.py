from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory="chroma_day1",   # SAME folder
    embedding_function=embeddings,
    collection_name="legal_knowledge"
)

print("DB COUNT:", vectordb._collection.count())

results = vectordb.similarity_search(
    "Explain FIR under Indian criminal law",
    k=3
)

print("Number of results:", len(results))
for r in results:
    print("METADATA:", r.metadata)
    print("CONTENT:", r.page_content[:300])
    print("-" * 80)

