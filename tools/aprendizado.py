from rag.pipeline import buscar

def gerar_exercicios(tema: str) -> str:
    material = buscar(tema, n_resultados=3)
    return (
        f"[MATERIAL RECUPERADO SOBRE '{tema}']:\n{material}\n\n"
        f"[INSTRUÇÃO]: Com base apenas no material acima, gere 3 questões "
        f"de múltipla escolha sobre '{tema}' com gabarito. "
        f"Numere as questões e indique a resposta correta ao final."
    )

def iniciar_active_recall(tema: str) -> str:
    material = buscar(tema, n_resultados=2)
    return (
        f"[MATERIAL SOBRE '{tema}']:\n{material}\n\n"
        f"[INSTRUÇÃO]: Com base no material acima, faça UMA pergunta curta e "
        f"direta ao usuário para testar seu conhecimento sobre '{tema}'. "
        f"Apenas a pergunta, sem resposta ainda."
    )

def avaliar_resposta(resposta_usuario: str, tema: str) -> str:
    material = buscar(tema, n_resultados=2)
    return (
        f"[MATERIAL DE REFERÊNCIA SOBRE '{tema}']:\n{material}\n\n"
        f"[RESPOSTA DO USUÁRIO]: {resposta_usuario}\n\n"
        f"[INSTRUÇÃO]: Avalie se a resposta do usuário está correta, "
        f"parcialmente correta ou incorreta com base no material. "
        f"Explique o que está certo, o que falta, e dê a resposta completa."
    )