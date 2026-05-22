from tools.agenda import consultar_agenda
from tools.tarefas import listar_tarefas, adicionar_tarefa, concluir_tarefa

erros = 0

def checar(descricao, condicao):
    global erros
    if condicao:
        print(f"  ✓ {descricao}")
    else:
        print(f"  ✗ FALHOU: {descricao}")
        erros += 1

print("=== Testes de Agenda ===")
resultado = consultar_agenda("hoje")
checar("consultar_agenda retorna uma string", isinstance(resultado, str))
checar("consultar_agenda não retorna vazio", len(resultado) > 0)

print("\n=== Testes de Tarefas ===")
resultado = adicionar_tarefa("Tarefa de teste automatizado", "2025-12-31")
checar("adicionar_tarefa confirma criação", "adicionada" in resultado.lower())

lista = listar_tarefas()
checar("listar_tarefas retorna string", isinstance(lista, str))
checar("tarefa adicionada aparece na lista", "Tarefa de teste automatizado" in lista)

print("\n=== Resultado ===")
if erros == 0:
    print("Todos os testes passaram!")
else:
    print(f"{erros} teste(s) falharam.")