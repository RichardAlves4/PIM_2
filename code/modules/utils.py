# Importando a biblioteca bcrypt para criptografar senhas de forma segura
import bcrypt

# RF04 - Função para criptografar a senha usando bcrypt
def criptografar_senha(senha):
    salt = bcrypt.gensalt()  # Gera um salt para a criptografia
    return bcrypt.hashpw(senha.encode(), salt).decode()  # Criptografa e retorna a senha

# Função para verificar se a senha digitada corresponde à senha armazenada
def verificar_senha(senha_digitada, senha_armazenada):
    return bcrypt.checkpw(senha_digitada.encode(), senha_armazenada.encode())  # Retorna True ou False