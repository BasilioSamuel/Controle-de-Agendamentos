import mysql.connector
import bcrypt

# Constantes para os dias da semana
DIAS_SEMANA = {
    1: "segunda-feira",
    2: "terça-feira",
    3: "quarta-feira",
    4: "quinta-feira",
    5: "sexta-feira",
    6: "sábado",
    7: "domingo"
}

# Dicionário inverso, se precisar
DIAS_INVERSO = {v: k for k, v in DIAS_SEMANA.items()}
3

def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456789",
        database="atendimento_db"
    )

def cadastrar_usuario():
    conn = conectar()
    cursor = conn.cursor()

    username = input("Informe o nome de usuário: ").strip()
    senha = input("Informe a senha: ").strip()
    senha_bytes = senha.encode('utf-8')
    senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())    

    # Agora pedindo o valor da hora junto
    while True:
        try:
            valor_hora = float(input("Informe o valor da hora: ").strip()) 
            if valor_hora < 0:
                print("Valor da hora deve ser maior que zero.")
                continue
            break
        except ValueError:
            print("Valor inválido. Digite um número.")    

    try:
        cursor.execute(
            "INSERT INTO usuarios (username, senha_hash, valor_hora) VALUES (%s, %s, %s)", 
            (username, senha_hash.decode('utf-8'), valor_hora)
        )
        conn.commit()
        print("Usuário cadastrado com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar usuário: {err}")

    cursor.close()
    conn.close()


def login_usuario():
    conn = conectar()
    cursor = conn.cursor()

    username = input("Usuário: ").strip()
    senha = input("Senha: ").strip()

    cursor.execute("SELECT id, senha_hash, valor_hora FROM usuarios WHERE username = %s", (username,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado is None:
        print("Usuário não encontrado.")
        return None, None

    usuario_id, senha_hash, valor_hora = resultado
    senha_hash_bytes = senha_hash.encode('utf-8')
    senha_bytes = senha.encode('utf-8')

    if bcrypt.checkpw(senha_bytes, senha_hash_bytes):
        print("Login bem-sucedido.")
        return usuario_id, valor_hora
    else:
        print("Senha incorreta.")
        return None, None


# Agora, adaptamos suas funções de atendimento para receber o usuario_id:

def normalizar_palavras(texto):
    """
    Normaliza o texto removendo acentos, espaços excedentes e convertendo para minúsculas.
    """
    import unicodedata

    # Remove acentos
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) == 'Mn'
    )
    # Converte para minúsculas
    texto = texto.lower().strip()

    # Troca espaços por um único espaço
    while "  " in texto:
        texto = texto.replace("  ", " ")

    return texto

def adicionar_atendimento_banco(usuario_id, nome_crianca, dia_semana):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO atendimento (usuario_id, nome_crianca, dia_semana) VALUES (%s, %s, %s)"
    valores = (usuario_id, nome_crianca, dia_semana)
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()

def listar_atendimentos_banco(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_crianca, dia_semana FROM atendimento WHERE usuario_id = %s", (usuario_id,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

# As outras funções que listam ou removem atendimentos também devem usar o usuario_id para filtrar, vou ajustar a remover como exemplo:

def remover_atendimento(usuario_id):
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
            return pros_selecao(usuario_id)

        dia_escolhido = dias_map[dia]

        cursor.execute("SELECT id, nome_crianca FROM atendimento WHERE dia_semana = %s AND usuario_id = %s", (dia_escolhido, usuario_id))
        resultados = cursor.fetchall()

        if not resultados:
            print(f"Não há atendimentos cadastrados na {dia_escolhido}.")
            cursor.close()
            conn.close()
            return pros_selecao(usuario_id)

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

    return pros_selecao(usuario_id)

# Ajustar funções pros_selecao e pros_atd para passar usuario_id

def pros_selecao(usuario_id):
    selecionar = input("Para voltar ao menu digite (1) ou para sair digite (2): ")
    if selecionar == "1":
        menu(usuario_id)
    elif selecionar == "2":
        sair()
    else:
        print("Opção inválida.")
        pros_selecao(usuario_id)

def pros_atd(usuario_id):
    selecionar = input("Para voltar ao menu digite (1) ou para adicionar outro atendimento(2): ")
    if selecionar == "1":
        menu(usuario_id)
    elif selecionar == "2":
        adicionar_atendimento(usuario_id)
    else:
        print("Opção inválida.")
        pros_atd(usuario_id)

# Adaptar as funções que chamam o pros_selecao e pros_atd para passar o usuario_id

def adicionar_atendimento(usuario_id):
    atendimento = input("Selecione o dia da semana para adicionar um atendimento: ")
    atd = normalizar_palavras(atendimento)

    cria = input("Digite o nome da criança atendida: ")

    dias_validos = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]

    if atd not in dias_validos:
        print("Dia da semana inválido.")
        return pros_atd(usuario_id)

    adicionar_atendimento_banco(usuario_id, cria, atd)

    print("Atendimento adicionado com sucesso no banco!")
    return pros_atd(usuario_id)

def calendario(usuario_id):
    atendimentos = listar_atendimentos_banco(usuario_id)

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

    return pros_selecao(usuario_id)

def cheia(usuario_id):
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
                cursor.execute("SELECT COUNT(*) FROM atendimento WHERE dia_semana = %s AND usuario_id = %s", (dia_escolhido, usuario_id))
                (quantidade,) = cursor.fetchone()
                total = valor * quantidade
                print(f"Total da {dia_escolhido.capitalize()}: R$ {total:.2f}")

        elif opcao == 2:
            cursor.execute("SELECT COUNT(*) FROM atendimento WHERE usuario_id = %s", (usuario_id,))
            (quantidade_total,) = cursor.fetchone()
            total = valor * quantidade_total
            print(f"Total da semana inteira: R$ {total:.2f}")

        else:
            print("Opção inválida!")

    except ValueError:
        print("Entrada inválida, tente novamente.")

    cursor.close()
    conn.close()

    return pros_selecao(usuario_id)

# Ajustar menu para receber usuario_id e chamar funções passando ele

def menu(usuario_id):
    print("\nEste é o Menu de funcionalidades, escolha uma das funcionalidades abaixo:")
    print("1. Calendário")
    print("2. Adicionar atendimento")
    print("3. Remover atendimento")
    print("4. Sair")
    print("5. Calcular valor total de atendimentos (hora cheia)")
    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        calendario(usuario_id)
    elif opcao == "2":
        adicionar_atendimento(usuario_id)
    elif opcao == "3":
        remover_atendimento(usuario_id)
    elif opcao == "4":
        sair()
    elif opcao == "5":
        cheia(usuario_id)
    else:
        print("Opção inválida.")
        menu(usuario_id)

def inicio():
    print("Bem-vindo, o aplicativo está iniciando...")

def sair():
    print("Obrigado por utilizar o aplicativo, até a próxima!")

# Função principal para controlar o fluxo de login e menu

def main():
    inicio()
    while True:
        print("\n1 - Cadastrar usuário")
        print("2 - Login")
        print("3 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            cadastrar_usuario()
        elif escolha == "2":
            usuario_id = login_usuario()
            if usuario_id:
                menu(usuario_id)
            else:
                print("Falha no login. Tente novamente.")
        elif escolha == "3":
            sair()
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
