import os
import json
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer

DADOS_PATH = "data"
MODEL_NAME = "all-MiniLM-L6-v2"
COLECAO_NOME = "jarvis_docs"

modelo = SentenceTransformer(MODEL_NAME)
chroma_client = chromadb.PersistentClient(path="storage/chroma")
colecao = chroma_client.get_or_create_collection(COLECAO_NOME)

def ler_pdf(caminho: str) -> str:
    texto = ""
    with pdfplumber.open(caminho) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() or ""
    return texto

def ler_txt(caminho: str) -> str:
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

def chunk_texto(texto: str, tamanho: int = 500, sobreposicao: int = 100) -> list:
    """Divide o texto em pedaços com sobreposição."""
    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = inicio + tamanho
        chunks.append(texto[inicio:fim])
        inicio += tamanho - sobreposicao
    return chunks

def carregar_documentos():
    """Lê todos os arquivos de /data e indexa no ChromaDB."""
    arquivos = os.listdir(DADOS_PATH)
    total_chunks = 0

    for arquivo in arquivos:
        caminho = os.path.join(DADOS_PATH, arquivo)

        if arquivo.endswith(".pdf"):
            texto = ler_pdf(caminho)
        elif arquivo.endswith(".txt"):
            texto = ler_txt(caminho)
        else:
            continue

        chunks = chunk_texto(texto)
        embeddings = modelo.encode(chunks).tolist()

        ids = [f"{arquivo}_chunk_{i}" for i in range(len(chunks))]

        colecao.upsert(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=[{"fonte": arquivo} for _ in chunks]
        )
        total_chunks += len(chunks)
        print(f"  Indexado: {arquivo} ({len(chunks)} chunks)")

    print(f"\nTotal indexado: {total_chunks} chunks de {len(arquivos)} arquivo(s)")

def buscar(pergunta: str, n_resultados: int = 3) -> str:
    """Busca os chunks mais relevantes para a pergunta."""
    embedding_pergunta = modelo.encode([pergunta]).tolist()

    resultados = colecao.query(
        query_embeddings=embedding_pergunta,
        n_results=n_resultados
    )

    docs = resultados["documents"][0]
    fontes = [m["fonte"] for m in resultados["metadatas"][0]]

    if not docs:
        return "Nenhum material encontrado sobre esse tema."

    trechos = []
    for doc, fonte in zip(docs, fontes):
        trechos.append(f"[Fonte: {fonte}]\n{doc}")

    return "\n\n---\n\n".join(trechos)