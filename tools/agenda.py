import json
from datetime import datetime

AGENDA_PATH = "storage/agenda.json"

def carregar_agenda():
    with open(AGENDA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def consultar_agenda(dia: str = None) -> str:
    agenda = carregar_agenda()
    hoje = datetime.now().strftime("%Y-%m-%d")

    if dia in ("hoje", None):
        eventos = [e for e in agenda if e["data"] == hoje]
        label = "hoje"
    elif dia == "amanha":
        from datetime import timedelta
        amanha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        eventos = [e for e in agenda if e["data"] == amanha]
        label = "amanhã"
    else:
        eventos = [e for e in agenda if dia.lower() in (e["dia"], e["data"], e["materia"].lower())]
        label = dia

    if not eventos:
        return f"Nenhum evento encontrado para {label}."

    linhas = [f"Eventos para {label}:"]
    for e in eventos:
        linhas.append(f"- {e['horario']} | {e['tipo'].upper()} de {e['materia']} ({e['local']})")
    return "\n".join(linhas)