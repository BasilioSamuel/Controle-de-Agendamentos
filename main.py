
# Valor da hora por presença
# Valor da hora por falta
# Desmarcar criança
# Encaixe
segunda= []
terca= []
quarta= []
quinta= []
sexta= []
sabado= []
domingo= []
atendimento = []

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
  global segunda, terca, quarta, quinta, sexta, sabado, domingo

  if len(segunda) == 0 and len(terca) == 0 and len(quarta) == 0 and len(quinta) == 0 and len(sexta) == 0 and len(sabado) == 0 and len(domingo) == 0:
      print("Não há nenhum atendimento cadastrado.")
  else:
      print("Atendimentos cadastrados:")
      print("Segunda-feira:", segunda)
      print("Terça-feira:", terca)
      print("Quarta-feira:", quarta)
      print("Quinta-feira:", quinta)
      print("Sexta-feira:", sexta)
      print("Sábado:", sabado)
      print("Domingo:", domingo)

  return pros_selecao()

def adicionar_atendimento():
  global segunda, terca, quarta, quinta, sexta, sabado, domingo

  atendimento = input("Selecione o dia da semana para adicionar um atendimento: ")
  atd = normalizar_palavras(atendimento)

  cria = input("Digite o nome da criança atendida: ")

  if atd == "segunda-feira":
      segunda.append(cria)
  elif atd == "terça-feira":
      terca.append(cria)
  elif atd == "quarta-feira":
      quarta.append(cria)
  elif atd == "quinta-feira":
      quinta.append(cria)
  elif atd == "sexta-feira":
      sexta.append(cria)
  elif atd == "sábado":
      sabado.append(cria)
  elif atd == "domingo":
      domingo.append(cria)
  else:
      print("Dia da semana inválido.")
      return adicionar_atendimento()

  print("Atendimento adicionado com sucesso!")
  return pros_selecao()

def remover_atendimento():
    global segunda, terca, quarta, quinta, sexta, sabado, domingo
    
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
        
        if dia == 1:
            lista_dia = segunda
            nome_dia = "Segunda-feira"
        elif dia == 2:
            lista_dia = terca
            nome_dia = "Terça-feira"
        elif dia == 3:
            lista_dia = quarta
            nome_dia = "Quarta-feira"
        elif dia == 4:
            lista_dia = quinta
            nome_dia = "Quinta-feira"
        elif dia == 5:
            lista_dia = sexta
            nome_dia = "Sexta-feira"
        elif dia == 6:
            lista_dia = sabado
            nome_dia = "Sábado"
        elif dia == 7:
            lista_dia = domingo
            nome_dia = "Domingo"
        else:
            print("Opção inválida!")
            return remover_atendimento()
        
        if not lista_dia:
            print(f"Não há atendimentos cadastrados na {nome_dia}.")
            return pros_selecao()
        

        print(f"\nAtendimentos na {nome_dia}:")
        for i, atendimento in enumerate(lista_dia):
            print(f"{i}: {atendimento}")
        
        try:
            indice = int(input("Digite o número do atendimento que deseja remover: "))
            
            if 0 <= indice < len(lista_dia):
                removido = lista_dia.pop(indice)
                print(f"Atendimento '{removido}' removido com sucesso da {nome_dia}!")
            else:
                print("Índice inválido!")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    except ValueError:
        print("Por favor, digite um número válido para o dia da semana.")
    
    pros_selecao()

inicio()
menu()