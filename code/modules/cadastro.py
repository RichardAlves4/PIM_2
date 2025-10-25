import infra
import banco
import re

def cadastro():
    print("\nCADASTRO\n")

    while True:

        while True:
            search_role = str(input("\nVocê é um estudante ou professor ?\nDigite:\n\n\"E\" para estudante\n\"P\" para professor\n")).upper()

            if search_role not in ["E","P"]:
                print("\nOpção inválida. Tente novamente.\n")
                continue

            if search_role == "E":
                role = "USER"
                break
            elif search_role == "P":
                role = "INSTRUCTOR"
                break

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
            elif email in banco.users_db: # Verifica se o e-mail já está cadastrado
                print("Usuário já cadastrado")
                continue
            else: 
                break
        
        # RF02 - Valida e coleta a idade do aluno
        while True:
            idade = int(input("Informe sua idade: ").strip())
            if idade < 7:
                print("\nIdade mínima: 7 anos\n")
                continue
            elif idade > 100:
                print("\nIdade inválida! Tente novamente.\n")
                continue
            else:
                break
        
        while True:
            # RF04 - Coleta e verifica a senha
            senha = input("Informe uma senha forte: ").strip()
            repet_senha = input("Repita a senha: ").strip()

            # Verifica se as senhas coincidem
            if senha != repet_senha:
                print("As senhas são diferentes. Tente novamente")
                continue

            senha_criptografada = infra.criptografar_senha(senha) # Criptografa a senha
            break

        banco.users_db[email] = {
            "nome": nome, 
            "idade": idade, 
            "senha": senha_criptografada,
            "role": role
            }

        banco.salvar_usuarios() # RF12 - Salva os dados no arquivo
        print("Cadastro realizado com sucesso!")
        return
