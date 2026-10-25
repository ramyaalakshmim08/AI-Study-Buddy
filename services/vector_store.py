import chromadb


CHROMA_PATH = "data/chroma_db"

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name="study_materials"
)


def add_documents(chunks, embeddings, source_name):
    ids = [
        f"{source_name}_{index}"
        for index in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=[
            {"source": source_name}
            for _ in chunks
        ]
    )


def search_documents(query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results