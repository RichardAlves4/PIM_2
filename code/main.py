from banco import carregar_usuarios, salvar_usuarios, update_user, delete_user
from modules.login import login
from infra.security import privacy_terms
from modules.cadastro import cadastro

def home(): 

    while True:

        options = str(input("Digite \"C\" para Cadastrar-se, \"L\" para fazer login ou aperte \"X\" para voltar\n")).upper()

        if options not in ["C", "L", "X"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue

        if options == "C":
            response = privacy_terms()
            if response:
                cadastro()
        elif options == "L":
            carregar_usuarios()
            email = login()
            menu(email)
            
        elif options == "X":
            salvar_usuarios() 
            print("Saiu!")  
            break

def menu(email):

    while True:

        options = str(input("Digite:\n\n\"E\" Para editar os dados de sua conta\n\"D\" Para deletar sua conta\n\"X\" Para desconectar\n")).upper()

        if options not in ["E", "D", "X"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue

        if options == "E":
            update_user(email)
        elif options == "D":
            response = delete_user(email)
            if response:
                main()
            delete_user(email)
        elif options == "X":
            print("Desconectar!")  # Desconecta o aluno
            break

def main():

    carregar_usuarios()  
    print("Bem-vindo ao nosso site.")
    home()

if __name__ == "__main__":
    main()