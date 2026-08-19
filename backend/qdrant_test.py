from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

client = QdrantClient(url="http://localhost:6333")

if not client.collection_exists("test_collection"):
    client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=4, distance=Distance.COSINE),
    )

# Store one fake vector
client.upsert(
    collection_name="test_collection",
    points=[
        PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"note": "hello world"})
    ],
)

# Search for something close to it
response = client.query_points(
    collection_name="test_collection",
    query=[0.1, 0.2, 0.3, 0.35],
    limit=1,
)

for r in response.points:
    print(r.id, r.score, r.payload)