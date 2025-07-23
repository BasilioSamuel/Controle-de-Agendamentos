from db_config import conectar

try:
    conn = conectar()
    if conn.is_connected():
        print("Conexão bem-sucedida ao banco MySQL!")
    conn.close()
except Exception as e:
    print("Erro ao conectar:", e)