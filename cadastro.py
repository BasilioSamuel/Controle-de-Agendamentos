from db_config import conectar        # Importa a função que faz conexão com o banco
from utils import criptografar_senha  # Importa a função para criptografar a senha

def cadastrar_usuario():
    # Entrada de dados do usuário
    nome = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")
    
    # Criptografa a senha com bcrypt antes de salvar no banco
    senha_criptografada = criptografar_senha(senha)

    try:
        # Conexão com o banco
        conn = conectar()
        cursor = conn.cursor()

        # Comando SQL para inserir nome e senha criptografada
        sql = "INSERT INTO usuarios (nome, senha) VALUES (%s, %s)"
        cursor.execute(sql, (nome, senha_criptografada.decode()))
        conn.commit()  # Confirma a inserção no banco

        print("✅ Usuário cadastrado com sucesso!")

    except Exception as e:
        print("❌ Erro ao cadastrar usuário:", e)  # Exibe qualquer erro (ex: nome duplicado)

    finally:
        # Fecha o cursor e a conexão mesmo se der erro
        cursor.close()
        conn.close()
