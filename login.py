# login.py
from db_config import conectar
from utils import verificar_senha

def login():
    tentativas = 3

    while tentativas > 0:
        nome = input("Usuário: ")
        senha = input("Senha: ")

        try:
            conn = conectar()
            cursor = conn.cursor()

            sql = "SELECT senha FROM usuarios WHERE nome = %s"
            cursor.execute(sql, (nome,))
            resultado = cursor.fetchone()

            if resultado and verificar_senha(senha, resultado[0]):
                print("✅ Login bem-sucedido!")
                return True
            else:
                tentativas -= 1
                print(f"❌ Usuário ou senha incorretos. Tentativas restantes: {tentativas}")

        except Exception as e:
            print("Erro no login:", e)
            break

        finally:
            cursor.close()
            conn.close()

    print("❌ Tentativas excedidas. Encerrando o programa.")
    return False
