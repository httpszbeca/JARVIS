import json
import os
import re
import logging
from openai import OpenAI
from dotenv import load_dotenv

from tools.agenda import consultar_agenda
from tools.tarefas import listar_tarefas, adicionar_tarefa, concluir_tarefa
from tools.rag import buscar_material_rag

load_dotenv()

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/tool_calls.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

client = OpenAI(
    base_url=os.getenv("GEMMA_URL"),
    api_key=os.getenv("GEMMA_TOKEN")
)

DESCRICAO_FERRAMENTAS = """
Você é o JARVIS, assistente acadêmico pessoal. Responda sempre em português brasileiro.

Você tem acesso às seguintes ferramentas. Quando precisar usar uma, responda APENAS com um bloco JSON nesse formato exato, sem mais nada:
{"tool": "nome_da_ferramenta", "args": {"parametro": "valor"}}

Ferramentas disponíveis:

1. consultar_agenda
   - Uso: quando perguntarem sobre aulas, provas ou eventos
   - Args: {"dia": "hoje" | "amanha" | "segunda" | "2025-06-10"}

2. listar_tarefas
   - Uso: quando perguntarem sobre tarefas pendentes
   - Args: {}

3. adicionar_tarefa
   - Uso: quando pedirem para adicionar/criar uma tarefa
   - Args: {"titulo": "texto da tarefa", "prazo": "2025-06-10"} (prazo é opcional)

4. concluir_tarefa
   - Uso: quando pedirem para marcar tarefa como feita/concluída
   - Args: {"id_tarefa": 1}

5. buscar_material_rag
   - Uso: quando perguntarem sobre conteúdo acadêmico, conceitos, matérias, resumos
   - Args: {"pergunta": "o que o usuário quer saber"}

Se a pergunta não precisar de ferramenta, responda normalmente em texto.
"""

MAPA_FERRAMENTAS = {
    "consultar_agenda":   lambda args: consultar_agenda(**args),
    "listar_tarefas":     lambda args: listar_tarefas(**args),
    "adicionar_tarefa":   lambda args: adicionar_tarefa(**args),
    "concluir_tarefa":    lambda args: concluir_tarefa(**args),
    "buscar_material_rag": lambda args: buscar_material_rag(**args),
}

def extrair_tool_call(texto: str):
    match = re.search(r'\{.*"tool".*\}', texto, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None

def executar_ferramenta(nome: str, args: dict) -> str:
    func = MAPA_FERRAMENTAS.get(nome)
    if not func:
        return f"Ferramenta '{nome}' não encontrada."
    resultado = func(args)
    logging.info(f"FERRAMENTA: {nome} | ARGS: {args} | RESULTADO: {resultado}")
    return resultado

def chat(historico: list, pergunta: str) -> str:
    historico.append({"role": "user", "content": pergunta})

    # Primeira chamada: o modelo decide se usa ferramenta ou responde direto
    resposta = client.chat.completions.create(
        model="google/gemma-3-12b-it",
        messages=historico
    )
    texto = resposta.choices[0].message.content

    # Verifica se o modelo quer chamar uma ferramenta
    tool_call = extrair_tool_call(texto)

    if tool_call:
        nome = tool_call.get("tool")
        args = tool_call.get("args", {})
        resultado = executar_ferramenta(nome, args)

        # Segunda chamada: modelo formula resposta com o resultado da ferramenta
        historico.append({"role": "assistant", "content": texto})
        historico.append({
            "role": "user",
            "content": f"[Resultado da ferramenta {nome}]: {resultado}\n\nAgora responda ao usuário em português com base nesse resultado."
        })

        resposta_final = client.chat.completions.create(
            model="google/gemma-3-12b-it",
            messages=historico
        )
        resposta_texto = resposta_final.choices[0].message.content
        historico.append({"role": "assistant", "content": resposta_texto})
        return resposta_texto

    # Respondeu direto, sem ferramenta
    historico.append({"role": "assistant", "content": texto})
    return texto

def main():
    print("=" * 50)
    print("   JARVIS Acadêmico — digite 'sair' para encerrar")
    print("=" * 50)

    historico = [{"role": "system", "content": DESCRICAO_FERRAMENTAS}]

    print("Carregando materiais de estudo...")
    from rag.pipeline import carregar_documentos
    carregar_documentos()
    print("Pronto!\n")

    while True:
        pergunta = input("\nVocê: ").strip()
        if pergunta.lower() in ("sair", "exit", "quit"):
            print("JARVIS: Até mais! Bons estudos.")
            break
        if not pergunta:
            continue
        try:
            resposta = chat(historico, pergunta)
            print(f"\nJARVIS: {resposta}")
        except Exception as e:
            print(f"\n[ERRO] {e}")

if __name__ == "__main__":
    main()