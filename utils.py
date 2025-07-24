import bcrypt

def criptografar_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

def verificar_senha(senha_digitada, senha_banco):
    return bcrypt.checkpw(senha_digitada.encode(), senha_banco.encode())