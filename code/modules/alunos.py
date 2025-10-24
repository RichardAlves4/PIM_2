import infra
import banco
import re

# RF01 - Cadastro de alunos
# RF02 - Validação de idade mínima (7 anos)
# RF03 - Validação de email (@gmail.com)
# RF04 - Armazenamento seguro de senha
# RF15 - Exigir aceite dos termos de privacidade antes do cadastro
# RF01 - Função para o cadastro de alunos
def cadastro_aluno():
    print("\nCadastro de Alunos\n")

    # RF15 - Termos de privacidade antes do cadastro
    print("\nAntes de se cadastrar, você deve aceitar nossa Política de Privacidade.\n\nUsaremos seus dados apenas para criar sua conta e permitir seu acesso ao sistema.")

    permissao = input("\nVocê aceita nossa Política de Privacidade? (S/N): ").lower().upper()

    if permissao == 'N':
        print("Cadastro cancelado. Você deve aceitar os termos para continuar.\n")
        return None
    
    elif permissao not in ["S","X"]:
        print("Resposta inválida.")
        return None

    while True:
        
        # Coleta o nome do aluno para o cadastro
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

            elif email in banco.usuarios_alunos: # Verifica se o e-mail já está cadastrado
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
            banco.usuarios_alunos[email] = {
                "nome": nome, 
                "idade": idade, 
                "senha": senha_criptografada
            }
            banco.salvar_usuarios() # RF12 - Salva os dados no arquivo
            print("Cadastro realizado com sucesso!")
            return

# RF05 - Função para o login do aluno
def login_aluno():
    print("\nLogin de Aluno\n")

    # Coleta as credenciais do aluno
    email = input("Email: ").strip().lower()
    senha = input("Senha: ").strip()

    # Verifica se o usuário existe
    if email in banco.usuarios_alunos:
        # RF04 - Verificação segura de senha
        if infra.verificar_senha(senha, banco.usuarios_alunos[email]["senha"]):# Verifica se a senha está correta
            print(f"Bem-vindo, {banco.usuarios_alunos[email]['nome']}!")
            return email            
        
    print("Email ou senha incorretos!")
    return None

