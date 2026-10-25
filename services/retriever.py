from services.embeddings import create_embeddings
from services.vector_store import search_documents


def retrieve_context(query, top_k=3):
    query_embedding = create_embeddings([query])[0]

    results = search_documents(
        query_embedding,
        top_k=top_k
    )

    documents = results.get("documents", [[]])[0]

    return documents