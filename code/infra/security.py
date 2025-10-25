# Importando a biblioteca bcrypt para criptografar senhas de forma segura
import bcrypt

# RF04 - Função para criptografar a senha usando bcrypt
def criptografar_senha(senha):
    salt = bcrypt.gensalt()  # Gera um salt para a criptografia
    return bcrypt.hashpw(senha.encode(), salt).decode()  # Criptografa e retorna a senha

# Função para verificar se a senha digitada corresponde à senha armazenada
def verificar_senha(senha_digitada, senha_armazenada):
    return bcrypt.checkpw(senha_digitada.encode(), senha_armazenada.encode())  # Retorna True ou False

def privacy_terms():

    while True:
        options = str(input("\nPOLITICA DE PRIVACIDADE\n\nDigite:\n\"V\" para ver nossa politica de privacidade\n\"S\" para aceitar\n\"N\" para recusar\n")).upper()

        if options not in ["V", "N", "S"]:
                print("\nOpção inválida. Tente novamente.\n")
                continue
        
        if options == "V":
            print("\nOs dados que vão ser solicitados serão utilizados " \
            "para gerar sua conta e permitir seu acesso ao sistema escolar.\n")
            continue
        elif options == "N":
            print("\nCadastro cancelado. Você deve aceitar os termos para continuar.\n")
            return False
        elif options == "S":
            return True