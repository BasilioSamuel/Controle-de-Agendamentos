import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",      # servidor do banco, geralmente localhost para sua máquina
        user="root",           # seu usuário do MySQL (ex: root)
        password="123456789",           # sua senha do MySQL (deixe vazio se não tiver)
        database="sistema_atendimento"  # nome do banco que criamos
    )
