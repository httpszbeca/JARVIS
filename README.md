# JARVIS Acadêmico

Assistente pessoal acadêmico desenvolvido com RAG, Tool Calling e LLM (Qwen2.5-14B-Instruct-AWQ).

## Funcionalidades (Trabalho 1)

- **3.1 RAG** — Consulta a materiais de estudo (PDFs e textos)
- **3.2 Agenda** — Consulta de aulas, provas e eventos
- **3.3 Tarefas** — Adicionar, listar e concluir tarefas

## Funcionalidades (Trabalho 2)

- **3.4 Planejamento** — Combina agenda, tarefas e materiais para montar plano de estudos
- **Geração de exercícios** — Cria questões de múltipla escolha baseadas nos PDFs
- **Active Recall interativo** — Sistema pergunta, usuário responde, modelo avalia

## Ferramentas implementadas

| Ferramenta | Descrição |
|---|---|
| `consultar_agenda` | Retorna eventos da agenda por dia |
| `listar_tarefas` | Lista tarefas pendentes |
| `adicionar_tarefa` | Adiciona nova tarefa com prazo opcional |
| `concluir_tarefa` | Marca tarefa como concluída pelo ID |
| `buscar_material_rag` | Busca semântica nos materiais de estudo |
| `planejar_estudos` | Combina agenda + tarefas + RAG para sugerir prioridades |
| `gerar_exercicios` | Gera questões de múltipla escolha sobre um tema |
| `iniciar_active_recall` | Faz uma pergunta ao usuário para testar conhecimento |
| `avaliar_resposta` | Avalia a resposta do usuário com base no material |

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
# Edite o .env com seu token
```

## Configuração

Crie um arquivo `.env` na raiz com:
GEMMA_TOKEN=seu_token_aqui
GEMMA_URL=https://llm.liaufms.org/v1/qwen2-5-14b-instruct-awq

## Como usar

```bash
python main.py
```

Exemplos de perguntas:

**Agenda e tarefas:**
- "O que tenho hoje?"
- "Quais minhas tarefas pendentes?"
- "Adiciona tarefa: estudar para prova com prazo 2025-06-10"
- "Conclui a tarefa 1"

**Materiais (RAG):**
- "Explique o que é RAG"
- "O que são embeddings?"
- "Quais são os tipos de topologia de rede?"
- "O que é controle de mudanças em GCS?"

**Planejamento e aprendizado:**
- "Monte um plano de estudos para a prova de redes"
- "O que devo priorizar hoje?"
- "Gere 3 exercícios sobre gerência de configuração de software"
- "Quero ser testado sobre topologia de rede"

## Dataset

Os documentos estão na pasta `/data` e totalizam 10 arquivos com 354 chunks indexados.

| Arquivo | Matéria | Tipo | Origem |
|---|---|---|---|
| intro_ia.txt | Inteligência Artificial | Texto manual | Escrito pelos autores |
| Módulo 1 - Conceitos e terminologia.pdf | GCS | Slides de aula | Material do professor |
| Módulo 2 - Atividades de GCS.pdf | GCS | Slides de aula | Material do professor |
| Módulo 3 - Plano de GCS.pdf | GCS | Slides de aula | Material do professor |
| Módulo 4 - Sistemas de GCS.pdf | GCS | Slides de aula | Material do professor |
| Módulo 5 - Controle de Mudanças.pdf | GCS | Slides de aula | Material do professor |
| NET - Aula 01.pdf | Redes de Computadores | Slides de aula | Material do professor |
| NET - Aula 02.pdf | Redes de Computadores | Slides de aula | Material do professor |
| NET - Aula 03.pdf | Redes de Computadores | Slides de aula | Material do professor |
| NET - Aula 04.pdf | Redes de Computadores | Slides de aula | Material do professor |

**Estratégia de chunking:** Janela deslizante de 500 caracteres com sobreposição de 100 caracteres. A sobreposição evita que conceitos na fronteira entre chunks sejam perdidos na recuperação.

**Limitações:** PDFs com imagens ou tabelas complexas podem ter extração de texto incompleta. Arquivos escaneados sem camada de texto não são indexados. O dataset cobre apenas três áreas (IA, GCS e Redes).

## IAs utilizadas no desenvolvimento

- Claude (Anthropic) — arquitetura e geração de código

## Estrutura do projeto
jarvis-academico/

├── main.py                  # Orquestrador principal

├── tests.py                 # Testes básicos das ferramentas

├── requirements.txt         # Dependências do projeto

├── tools/

│   ├── agenda.py            # Ferramenta de agenda

│   ├── tarefas.py           # Ferramenta de tarefas

│   ├── rag.py               # Ferramenta RAG

│   ├── planejamento.py      # Ferramenta de planejamento de estudos

│   └── aprendizado.py       # Ferramentas de active recall e exercícios

├── rag/

│   └── pipeline.py          # Carregamento, chunking e busca

├── storage/

│   ├── agenda.json          # Dados da agenda

│   ├── tarefas.json         # Dados das tarefas

│   └── chroma/              # Banco vetorial (gerado automaticamente)

├── data/                    # Documentos do dataset (10 arquivos)

├── logs/                    # Logs de tool calling

├── avaliacao_sistema.md     # Avaliação com 10 perguntas classificadas

├── analise_erros.md         # Análise de 3 falhas identificadas

└── .env                     # Credenciais (não vai ao GitHub)
