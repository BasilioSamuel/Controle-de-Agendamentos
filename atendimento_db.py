from db_config import conectar


def adicionar_atendimento_db(dia_semana, nome_crianca):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO atendimentos (dia_semana, nome_crianca) VALUES (%s, %s)"
        cursor.execute(sql, (dia_semana, nome_crianca))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Erro ao adicionar atendimento no banco:", e)  # Mostrar o erro real
        return False

def listar_atendimentos_db(dia_semana):
    conn = conectar()
    cursor = conn.cursor()
    sql = "SELECT id, nome_crianca FROM atendimentos WHERE dia_semana = %s"
    cursor.execute(sql, (dia_semana,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados  # lista de tuplas (id, nome_crianca)

def listar_todos_atendimentos_db():
    conn = conectar()
    cursor = conn.cursor()
    sql = "SELECT id, dia_semana, nome_crianca FROM atendimentos"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados  # Agora retorna (id, dia, nome)



def remover_atendimento_db(id_atendimento):
    conn = conectar()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM atendimentos WHERE id = %s"
        cursor.execute(sql, (id_atendimento,))
        conn.commit()
        sucesso = cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao remover atendimento: {e}")
        sucesso = False
    cursor.close()
    conn.close()
    return sucesso

