import json
import os
import logging
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from tools.agenda import consultar_agenda
from tools.tarefas import listar_tarefas, adicionar_tarefa, concluir_tarefa

from tools.rag import buscar_material_rag

load_dotenv()

# Configuração do log
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/tool_calls.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

# Cliente Gemma
client = OpenAI(
    base_url=os.getenv("GEMMA_URL"),
    api_key=os.getenv("GEMMA_TOKEN")
)

# Descrição das ferramentas para o Gemma
FERRAMENTAS = [
    {
        "type": "function",
        "function": {
            "name": "consultar_agenda",
            "description": "Consulta a agenda acadêmica do estudante. Use para perguntas sobre aulas, provas e eventos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dia": {
                        "type": "string",
                        "description": "Dia a consultar: 'hoje', 'amanha', nome do dia (ex: 'segunda') ou data (ex: '2025-06-10')"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_tarefas",
            "description": "Lista todas as tarefas pendentes do estudante.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "adicionar_tarefa",
            "description": "Adiciona uma nova tarefa à lista do estudante.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string", "description": "Título da tarefa"},
                    "prazo":  {"type": "string", "description": "Prazo no formato YYYY-MM-DD (opcional)"}
                },
                "required": ["titulo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "concluir_tarefa",
            "description": "Marca uma tarefa como concluída pelo ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id_tarefa": {"type": "integer", "description": "ID numérico da tarefa"}
                },
                "required": ["id_tarefa"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_material_rag",
            "description": "Busca informações nos materiais de estudo do estudante (PDFs e textos). Use para perguntas sobre conteúdo acadêmico, conceitos, resumos e explicações.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pergunta": {
                        "type": "string",
                        "description": "A pergunta ou tema a buscar nos materiais"
                    }
                },
                "required": ["pergunta"]
            }
        }
    }
]

# Mapa de nome -> função Python
MAPA_FERRAMENTAS = {
    "consultar_agenda": consultar_agenda,
    "listar_tarefas":   listar_tarefas,
    "adicionar_tarefa": adicionar_tarefa,
    "concluir_tarefa":  concluir_tarefa,
    "buscar_material_rag": buscar_material_rag,
}

def executar_ferramenta(nome: str, argumentos: dict) -> str:
    """Executa a ferramenta e registra no log."""
    func = MAPA_FERRAMENTAS.get(nome)
    if not func:
        return f"Ferramenta '{nome}' não encontrada."
    resultado = func(**argumentos)
    logging.info(f"FERRAMENTA: {nome} | ARGS: {argumentos} | RESULTADO: {resultado}")
    return resultado

def chat(historico: list, pergunta: str) -> str:
    """Envia a pergunta ao Gemma e executa ferramentas se necessário."""
    historico.append({"role": "user", "content": pergunta})

    resposta = client.chat.completions.create(
        model="google/gemma-3-12b-it",
        messages=historico,
        tools=FERRAMENTAS,
        tool_choice="auto"
    )

    mensagem = resposta.choices[0].message

    # O modelo quer chamar uma ferramenta?
    if mensagem.tool_calls:
        historico.append(mensagem)

        for tool_call in mensagem.tool_calls:
            nome = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            resultado = executar_ferramenta(nome, args)

            historico.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": resultado
            })

        # Pede ao Gemma para formular a resposta final com o resultado
        resposta_final = client.chat.completions.create(
            model="google/gemma-3-12b-it",
            messages=historico
        )
        resposta_texto = resposta_final.choices[0].message.content
        historico.append({"role": "assistant", "content": resposta_texto})
        return resposta_texto

    # Respondeu direto, sem ferramenta
    resposta_texto = mensagem.content
    historico.append({"role": "assistant", "content": resposta_texto})
    return resposta_texto

def main():
    print("=" * 50)
    print("   JARVIS Acadêmico — digite 'sair' para encerrar")
    print("=" * 50)

    sistema = {
        "role": "system",
        "content": (
            "Você é o JARVIS, um assistente acadêmico pessoal. "
            "Ajude o estudante com sua agenda, tarefas e materiais de estudo. "
            "Responda sempre em português brasileiro de forma clara e objetiva. "
            "Use as ferramentas disponíveis sempre que a pergunta envolver agenda ou tarefas."
        )
    }
    historico = [sistema]
    
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