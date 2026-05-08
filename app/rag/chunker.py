from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents):

    splillter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    final_chunks = []

    for doc in documents:

        chunks = splillter.split_text(doc["content"])

        for chunk in chunks:

            final_chunks.append({
                "file_path": doc["file_path"],
                "content":chunk
            })
        
    return final_chunks