from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def create_vector_store(chunks):

    texts = [chunk["content"] for chunk in chunks]

    metadatas = [
        {"file_path": chunk["file_path"]}
        for chunk in chunks
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory="D:/Gen AI/chroma_db"
    )

    # Save database locally
    vectorstore.persist()

    return vectorstore
