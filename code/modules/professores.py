from .utils import criptografar_senha, verificar_senha
import banco
import re

# RF01 - Cadastro de professores
# RF02 - Validação de idade mínima (18 anos)
# RF03 - Validação de email (@gmail.com)
# RF04 - Armazenamento seguro de senha
# Função para o cadastro de professores
def cadastro_professor():
    print("\nCadastro de Professores\n")
    while True:

        # Coleta o nome do professor para o cadastro
        while True:
            nome = str(input("Informe seu nome: ")).strip().title()
            # RF03 - Verifica se o nome é composto por apenas letras
            if not re.fullmatch(r"[A-Za-zÀ-ÿ ]+", nome):
                print("Nome Inválido. Use apenas letras")
                continue
            else:
                break
        
        # Coleta o email do aluno para o cadastro
        while True:
            email = input("Informe seu melhor email: ").strip().lower()
            # RF03 - Verifica se o e-mail é válido
            if not email.endswith("@gmail.com"):
                print("Email inválido. Use @gmail.com")
                continue

            elif email in banco.usuarios_professores: # Verifica se o e-mail já está cadastrado
                print("Usuário já cadastrado")
                continue

            else:
                break
        
        # RF02 - Valida e coleta a idade do professor
        while True:
            idade = int(input("Informe sua idade: ").strip())
            if idade < 18:
                print("\nIdade mínima: 18 anos\n")
                continue

            elif idade >100:
                print("\nIdade inválida! Tente novamente.\n")
                continue

            else:
                break
        while True: 
            # RF04 - Coleta e verifica a senha
            senha = input("Informe uma senha forte: ")
            repet_senha = input("Repita a senha: ")

            # Verifica se as senhas coincidem
            if senha != repet_senha:
                print("As senhas são diferentes. Tente novamente")
                continue
        
            # Criptografa a senha
            senha_criptografada = criptografar_senha(senha)
            banco.usuarios_professores[email] = {
                "nome": nome,
                "idade": idade,
                "senha": senha_criptografada
            }
            banco.salvar_usuarios() # RF12 - Salva os dados no arquivo
            print("Cadastro realizado com sucesso!")
            return

# RF05 - Função para o login do professor
def login_professor():
    print("\nLogin de Professor\n")

    # Coleta as credenciais do professor
    email = input("Email: ").strip().lower()
    senha = input("Senha: ").strip()

    # Verifica se o usuário existe
    if email in banco.usuarios_professores:
        # RF04 - Verificação segura de senha
        if verificar_senha(senha, banco.usuarios_professores[email]["senha"]):# Verifica se a senha está correta
            print(f"Bem-vindo, {banco.usuarios_professores[email]['nome']}!")
            return email
        
    print("Email ou senha incorretos!")
    return None