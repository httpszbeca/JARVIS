import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()
print("✓ .env carregado, token:", os.getenv("GEMMA_TOKEN")[:8] + "...")

model = SentenceTransformer("all-MiniLM-L6-v2")
print("Modelo de embeddings carregado")

client = chromadb.Client()
print("ChromaDB funcionando")

print("\nTudo pronto!")