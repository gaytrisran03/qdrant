from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import re
from PyPDF2 import PdfReader
import glob
from langchain.text_splitter import CharacterTextSplitter
from pathlib import Path

cache_folder = Path("/Users/gaytrisran/Desktop/qdrant/qdrant/")

model = SentenceTransformer('all-MiniLM-L6-v2')


client = QdrantClient(":memory:")

client.recreate_collection(
    collection_name="test_collection",
    vectors_config=models.VectorParams(
        size=model.get_sentence_embedding_dimension(), 
        distance=models.Distance.EUCLID
    )
)