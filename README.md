# JARVIS Acadêmico

Assistente pessoal acadêmico desenvolvido com RAG, Tool Calling e LLM (Gemma 3 12B).

## Funcionalidades (Trabalho 1)

- **3.1 RAG** — Consulta a materiais de estudo 
- **3.2 Agenda** — Consulta de aulas, provas e eventos
- **3.3 Tarefas** — Adicionar, listar e concluir tarefas

## Ferramentas implementadas

| Ferramenta | Descrição |
|---|---|
| `consultar_agenda` | Retorna eventos da agenda por dia |
| `listar_tarefas` | Lista tarefas pendentes |
| `adicionar_tarefa` | Adiciona nova tarefa com prazo opcional |
| `concluir_tarefa` | Marca tarefa como concluída pelo ID |
| `buscar_material_rag` | Busca semântica nos materiais de estudo |

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/httpszbeca/JARVIS.git
cd JARVIS

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\Activate.ps1  # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o .env
cp .env.example .env
```

## Configuração

Crie um arquivo `.env` na raiz com: GEMMA_TOKEN=Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A
GEMMA_URL=https://llm.liaufms.org/v1/gemma-3-12b-it

## Como usar

```bash
python main.py
```

Exemplos de perguntas:
- "O que tenho hoje?"
- "Quais minhas tarefas pendentes?"
- "Adiciona tarefa: estudar para prova com prazo 2025-06-10"
- "Explique o que é RAG"
- "O que são embeddings?"

## Dataset

Os documentos estão na pasta `/data` e incluem:

| Arquivo | Matéria | Tipo |
|---|---|---|
| intro_ia.txt | Inteligência Artificial | Texto manual |
| Módulo 1 ao 5 - GCS.pdf | Gerência de Configuração de Software | PDF de aula |
| NET - Aula 01 ao 04.pdf | Redes de Computadores | PDF de aula |

**Estratégia de chunking:** Janela deslizante de 500 caracteres com sobreposição de 100 caracteres. A sobreposição evita que conceitos que aparecem na fronteira entre chunks sejam perdidos na recuperação.

**Limitações:** PDFs com imagens ou tabelas complexas podem ter extração de texto incompleta. Arquivos escaneados (sem camada de texto) não são indexados.

## IAs utilizadas no desenvolvimento

- Claude — arquitetura, geração de código e depuração

## Estrutura do projeto

```
jarvis-academico/
├── main.py              # Orquestrador principal
├── tools/
│   ├── agenda.py        # Ferramenta de agenda
│   ├── tarefas.py       # Ferramenta de tarefas
│   └── rag.py           # Ferramenta RAG
├── rag/
│   └── pipeline.py      # Carregamento, chunking e busca
├── storage/
│   ├── agenda.json      # Dados da agenda
│   ├── tarefas.json     # Dados das tarefas
│   └── chroma/          # Banco vetorial (gerado automaticamente)
├── data/                # Documentos do dataset
├── logs/                # Logs de tool calling
└── .env                 # Credenciais (não vai ao GitHub)
```

