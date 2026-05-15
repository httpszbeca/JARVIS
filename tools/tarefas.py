import json

TAREFAS_PATH = "storage/tarefas.json"

def carregar():
    with open(TAREFAS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar(tarefas):
    with open(TAREFAS_PATH, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)

def listar_tarefas() -> str:
    tarefas = carregar()
    pendentes = [t for t in tarefas if not t["concluida"]]
    if not pendentes:
        return "Nenhuma tarefa pendente."
    linhas = ["Tarefas pendentes:"]
    for t in pendentes:
        prazo = f" (prazo: {t['prazo']})" if t.get("prazo") else ""
        linhas.append(f"- [{t['id']}] {t['titulo']}{prazo}")
    return "\n".join(linhas)

def adicionar_tarefa(titulo: str, prazo: str = None) -> str:
    tarefas = carregar()
    novo_id = max((t["id"] for t in tarefas), default=0) + 1
    tarefas.append({"id": novo_id, "titulo": titulo, "concluida": False, "prazo": prazo})
    salvar(tarefas)
    return f"Tarefa '{titulo}' adicionada com ID {novo_id}."

def concluir_tarefa(id_tarefa: int) -> str:
    tarefas = carregar()
    for t in tarefas:
        if t["id"] == id_tarefa:
            t["concluida"] = True
            salvar(tarefas)
            return f"Tarefa '{t['titulo']}' marcada como concluída."
    return f"Tarefa com ID {id_tarefa} não encontrada."