from tools.agenda import consultar_agenda
from tools.tarefas import listar_tarefas
from rag.pipeline import buscar

def planejar_estudos(foco: str = None) -> str:
    agenda = consultar_agenda("hoje")
    tarefas = listar_tarefas()
    
    tema = foco if foco else "estudos gerais"
    material = buscar(tema, n_resultados=2)
    
    return (
        f"=== AGENDA DE HOJE ===\n{agenda}\n\n"
        f"=== TAREFAS PENDENTES ===\n{tarefas}\n\n"
        f"=== MATERIAL RELEVANTE SOBRE '{tema.upper()}' ===\n{material}"
    ) 