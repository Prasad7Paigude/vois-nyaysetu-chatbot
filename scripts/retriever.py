from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory="chroma_day1",
        embedding_function=embeddings,
        collection_name="legal_knowledge"
    )

    return vectordb.as_retriever(search_kwargs={"k": 3})
