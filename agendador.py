import mysql.connector
import bcrypt


def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456789",
        database="atendimento_db"
    )

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
    selecionar = input("Para voltar ao menu digite (1) ou para sair digite (2): ")
    if selecionar == "1":
        menu()
    elif selecionar == "2":
        sair()
    else:
        print("Opção inválida.")
        pros_selecao()

def pros_atd():
    selecionar = input("Para voltar ao menu digite (1) ou para adicionar outro atendimento(2): ")
    if selecionar == "1":
        menu()
    elif selecionar == "2":
        adicionar_atendimento()
    else:
        print("Opção inválida.")
        pros_atd()

def adicionar_atendimento_banco(nome_crianca, dia_semana):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO atendimento (nome_crianca, dia_semana) VALUES (%s, %s)"
    valores = (nome_crianca, dia_semana)
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()

def listar_atendimentos_banco():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_crianca, dia_semana FROM atendimento")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

def adicionar_atendimento():
    atendimento = input("Selecione o dia da semana para adicionar um atendimento: ")
    atd = normalizar_palavras(atendimento)

    cria = input("Digite o nome da criança atendida: ")

    dias_validos = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]

    if atd not in dias_validos:
        print("Dia da semana inválido.")
        return pros_atd()

    adicionar_atendimento_banco(cria, atd)

    print("Atendimento adicionado com sucesso no banco!")
    return pros_atd()

def calendario():
    atendimentos = listar_atendimentos_banco()

    dias = {
        "segunda-feira": [],
        "terça-feira": [],
        "quarta-feira": [],
        "quinta-feira": [],
        "sexta-feira": [],
        "sábado": [],
        "domingo": []
    }

    for _, nome, dia in atendimentos:
        dias[dia].append(nome)

    vazio = all(len(lista) == 0 for lista in dias.values())
    if vazio:
        print("Não há nenhum atendimento cadastrado.")
    else:
        print("Atendimentos cadastrados:")
        for dia_semana, nomes in dias.items():
            print(f"{dia_semana.capitalize()}: {nomes}")

    return pros_selecao()

def remover_atendimento():
    conn = conectar()
    cursor = conn.cursor()

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

        dias_map = {
            1: "segunda-feira",
            2: "terça-feira",
            3: "quarta-feira",
            4: "quinta-feira",
            5: "sexta-feira",
            6: "sábado",
            7: "domingo"
        }

        if dia not in dias_map:
            print("Opção inválida!")
            return pros_selecao()

        dia_escolhido = dias_map[dia]

        cursor.execute("SELECT id, nome_crianca FROM atendimento WHERE dia_semana = %s", (dia_escolhido,))
        resultados = cursor.fetchall()

        if not resultados:
            print(f"Não há atendimentos cadastrados na {dia_escolhido}.")
            cursor.close()
            conn.close()
            return pros_selecao()

        print(f"\nAtendimentos na {dia_escolhido}:")
        for idx, (id_atd, nome) in enumerate(resultados):
            print(f"{idx}: {nome} (ID {id_atd})")

        indice = int(input("Digite o número do atendimento que deseja remover: "))

        if 0 <= indice < len(resultados):
            id_remover = resultados[indice][0]
            cursor.execute("DELETE FROM atendimento WHERE id = %s", (id_remover,))
            conn.commit()
            print("Atendimento removido com sucesso!")
        else:
            print("Índice inválido!")

        cursor.close()
        conn.close()

    except ValueError:
        print("Por favor, digite um número válido.")

    return pros_selecao()

def cheia():
    conn = conectar()
    cursor = conn.cursor()

    valor = float(input("Digite o valor da sua hora cheia: "))
    print("Digite 1. para escolher um dia ou 2. para calcular o valor da semana toda")

    try:
        opcao = int(input("Você deseja saber o cálculo do dia (1) ou da semana (2)? "))

        if opcao == 1:
            print("\nDias da semana disponíveis:")
            print("1. Segunda-feira")
            print("2. Terça-feira")
            print("3. Quarta-feira")
            print("4. Quinta-feira")
            print("5. Sexta-feira")
            print("6. Sábado")
            print("7. Domingo")

            dia = int(input("Digite o número correspondente ao dia da semana: "))

            dias_map = {
                1: "segunda-feira",
                2: "terça-feira",
                3: "quarta-feira",
                4: "quinta-feira",
                5: "sexta-feira",
                6: "sábado",
                7: "domingo"
            }

            if dia not in dias_map:
                print("Opção inválida!")
            else:
                dia_escolhido = dias_map[dia]
                cursor.execute("SELECT COUNT(*) FROM atendimento WHERE dia_semana = %s", (dia_escolhido,))
                (quantidade,) = cursor.fetchone()
                total = valor * quantidade
                print(f"Total da {dia_escolhido.capitalize()}: R$ {total:.2f}")

        elif opcao == 2:
            cursor.execute("SELECT COUNT(*) FROM atendimento")
            (quantidade_total,) = cursor.fetchone()
            total = valor * quantidade_total
            print(f"Total da semana inteira: R$ {total:.2f}")

        else:
            print("Opção inválida!")

    except ValueError:
        print("Entrada inválida, tente novamente.")

    cursor.close()
    conn.close()

    return pros_selecao()

def menu():
    print("\nEste é o Menu de funcionalidades, escolha uma das funcionalidades abaixo:")
    print("1. Calendário")
    print("2. Adicionar atendimento")
    print("3. Remover atendimento")
    print("4. Sair")
    print("5. Calcular valor total de atendimentos (hora cheia)")
    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        calendario()
    elif opcao == "2":
        adicionar_atendimento()
    elif opcao == "3":
        remover_atendimento()
    elif opcao == "4":
        sair()
    elif opcao == "5":
        cheia()
    else:
        print("Opção inválida.")
        menu()

if __name__ == "__main__":
    inicio()
    menu()
