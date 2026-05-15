from rag.pipeline import buscar

def buscar_material_rag(pergunta: str) -> str:
    """Ferramenta que o Gemma chama para buscar nos materiais de estudo."""
    return buscar(pergunta)