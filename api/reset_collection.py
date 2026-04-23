import os
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

load_dotenv()

COLLECTION_NAME = "financial"

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# Recreate collection ensures it is deleted if it exists, and created with the correct schemas
qdrant.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config={
        "dense": models.VectorParams(size=384, distance=models.Distance.COSINE),
        "colbert": models.VectorParams(
            size=128,
            distance=models.Distance.COSINE,
            multivector_config=models.MultiVectorConfig(
                comparator=models.MultiVectorComparator.MAX_SIM
            ),
        ),
    },
    sparse_vectors_config={"sparse": models.SparseVectorParams()},
)
print("Collection 'financial' reset successfully with dense, colbert, and sparse vectors!")
