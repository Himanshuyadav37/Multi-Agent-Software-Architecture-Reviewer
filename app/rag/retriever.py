from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def get_retriever():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="D:/Gen AI/chroma_db",
        embedding_function=embeddings
    )

    # Create Retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )

    return retriever