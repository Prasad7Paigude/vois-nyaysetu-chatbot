from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def get_retriever():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectordb = Chroma(
        persist_directory="chroma_day1",
        embedding_function=embeddings,
        collection_name="legal_knowledge"
    )

    return vectordb.as_retriever(search_kwargs={"k": 3})
