# embed_store.py
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

def create_qdrant_client():
    return QdrantClient(":memory:")

def create_collection(client, collection_name="docs"):
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

def index_chunks(client, embed_model, chunks):
    vectors = embed_model.encode([c['content'] for c in chunks])
    points = []
    for i, vector in enumerate(vectors):
        points.append(PointStruct(
            id=i,
            vector=vector.tolist(),
            payload=chunks[i]
        ))
    client.upsert(collection_name="docs", points=points)

def retrieve_context(client, embed_model, query, k=1):
    query_vector = embed_model.encode(query).tolist()
    hits = client.search(collection_name="docs", query_vector=query_vector, limit=k)
    return hits
