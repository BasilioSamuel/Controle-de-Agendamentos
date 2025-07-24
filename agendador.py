
# Valor da hora por presença
# Valor da hora por falta
# Desmarcar criança
# Encaixe
from atendimento_db import adicionar_atendimento_db, listar_atendimentos_db, remover_atendimento_db, listar_todos_atendimentos_db
from cadastro import cadastrar_usuario
from login import login

def tela_inicial():
    print("1. Login")
    print("2. Cadastrar novo usuário")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        if login():
            inicio()
    elif opcao == "2":
        cadastrar_usuario()
        tela_inicial()
    else:
        print("Opção inválida.")
        tela_inicial()


def normalizar_palavras(texto):
    substituicoes = {
        "segunda feira": "segunda-feira",
        "segunda": "segunda-feira",
        "terca feira": "terça-feira",
        "terca": "terça-feira",
        "terça": "terça-feira",
        "quarta feira": "quarta-feira",
        "quarta": "quarta-feira",
        "quinta feira": "quinta-feira",
        "quinta": "quinta-feira",
        "sexta feira": "sexta-feira",
        "sexta": "sexta-feira",
        "sabado": "sábado",
        "domingo": "domingo"
    }

    texto = texto.lower()
    for forma_livre, forma_padrao in substituicoes.items():
        if forma_livre in texto:
            texto = texto.replace(forma_livre, forma_padrao)
    return texto

def inicio():
  print("Bem-vindo, o aplicativo está iniciando...")
  menu()

def sair():
  print("Obrigado por utilizar o aplicativo, até a próxima!")

def pros_selecao():
  selecionar= int(input("Para voltar ao menu digite (1) ou para sair digite (2):"))
  if selecionar == 1:
    menu()
  elif selecionar ==2:
    sair()

def menu():
  print("Este é o Menu de funcionalidades, escolha uma das funcionalidades abaixo:")
  print("1. Calendário")
  print("2. Adicionar atendimento ")
  print("3. Remover atendimento")
  print("4. Sair")
  opcao = int(input("Digite a opção desejada: "))
  if opcao == 1:
    calendario()
  elif opcao == 2:
    adicionar_atendimento()
  elif opcao == 3:
    remover_atendimento()
  elif opcao == 4:
    sair()

def calendario():
    atendimentos = listar_todos_atendimentos_db()  # retorna tuplas com (id, dia_semana, nome_crianca)

    if not atendimentos:
        print("Não há nenhum atendimento cadastrado.")
    else:
        print("Atendimentos cadastrados:")

        dias = {
            "segunda-feira": [],
            "terça-feira": [],
            "quarta-feira": [],
            "quinta-feira": [],
            "sexta-feira": [],
            "sábado": [],
            "domingo": []
        }

        for id_atendimento, dia, nome in atendimentos:
            if dia in dias:
                dias[dia].append(nome)
            else:
                dias.setdefault(dia, []).append(nome)

        for dia_semana, nomes in dias.items():
            print(f"{dia_semana.capitalize()}: {nomes if nomes else 'Nenhum atendimento'}")

    return pros_selecao()



def adicionar_atendimento():
    atendimento = input("Selecione o dia da semana para adicionar um atendimento: ")
    atd = normalizar_palavras(atendimento)

    cria = input("Digite o nome da criança atendida: ")

    # Tenta adicionar no banco
    sucesso = adicionar_atendimento_db(atd, cria)

    if sucesso:
        print("Atendimento adicionado com sucesso no banco!")
    else:
        print("Falha ao adicionar atendimento.")

    return pros_selecao()

def remover_atendimento():
    atendimentos = listar_todos_atendimentos_db()

    if not atendimentos:
        print("Não há atendimentos para remover.")
        return pros_selecao()

    print("Atendimentos cadastrados:")
    for i, (id_atendimento, dia, nome) in enumerate(atendimentos):
        print(f"{i}. {nome} ({dia}) [ID: {id_atendimento}]")

    try:
        indice = int(input("Digite o número do atendimento que deseja remover: "))
        if 0 <= indice < len(atendimentos):
            id_atendimento, dia, nome = atendimentos[indice]
            sucesso = remover_atendimento_db(id_atendimento)
            if sucesso:
                print(f"Atendimento de {nome} em {dia} removido com sucesso!")
            else:
                print("Erro ao remover atendimento.")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Por favor, digite um número válido.")

    pros_selecao()



def cheia():
   global segunda, terca, quarta, quinta, sexta, sabado, domingo


   valor =float(input("Digite o valor da sua hora cheia:"))
   print("Digite 1. para escolher um dia ou 2. para a semana toda")
   opcao= int(float("Você deseja saber o calculo do dia ou da semana?"))
   if opcao ==1:
    print("\nDias da semana disponíveis:")
    print("1. Segunda-feira")
    print("2. Terça-feira")
    print("3. Quarta-feira")
    print("4. Quinta-feira")
    print("5. Sexta-feira")
    print("6. Sábado")
    print("7. Domingo")
    try:
      dia = int(input("Digite o número correspondente ao dia da semana: "))
      if dia== 1:
        calculo= valor * len(dia)
      print(calculo)
    except ValueError:
      print("Por favor, digite um número válido.")
        
tela_inicial()


