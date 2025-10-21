from modules import cadastro_aluno, login_aluno, cadastro_professor, login_professor
from banco import carregar_usuarios, salvar_usuarios, editar_aluno, editar_professor, excluir_aluno, excluir_professor, usuarios_alunos

# Função principal para verificar qual tipo de usuário está tentando acessar (aluno ou professor)
def verifica_user():
    estado_verifica_user = False

    while not estado_verifica_user:
        # Solicita ao usuário qual área deseja acessar
        menu_verifica_user = input("Digite:\n\n\"A\" Para acesso a área do aluno\n\"P\" Para acesso a área do professor\n\"X\" Para Sair\n").upper()

        # Verifica se a opção escolhida é válida
        if menu_verifica_user not in ["A", "P", "X"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue

        if menu_verifica_user == "A":
            aluno()  # Chama a função para o aluno
        elif menu_verifica_user == "P":
            professor()  # Chama a função para o professor
        elif menu_verifica_user == "X":
            salvar_usuarios()  # Salva os usuários antes de sair
            print("Saiu!")  # Sai do programa
            break

# Função para gerenciar as ações do aluno (cadastro, login ou voltar)
def aluno():
    estado = False

    while not estado:

        print("\nBem-vindo Aluno")

        # Solicita a opção ao aluno
        escolha = str(input("Digite \"C\" para Cadastrar-se, \"L\" para acessar sua conta ou aperte \"X\" para voltar\n")).upper()
        
        if escolha not in ["C", "L", "X"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue

        if escolha == "C":
            cadastro_aluno()  # Chama a função para cadastrar o aluno
        
        elif escolha == "L":
            aluno_email = login_aluno() # Chama a função para logar o aluno
            if aluno_email:
                menu_aluno(aluno_email)
                estado = True
        
        elif escolha == "X":
            print("Voltar!")  # Volta para o menu anterior
            estado = True
            return

# Função para gerenciar as ações do professor (cadastro, login ou voltar)
def professor():
    estado= False

    while not estado:
        print("Bem-vindo Professor")
        # Solicita a opção ao professor
        escolha = str(input("Digite \"C\" para Cadastrar-se, \"L\" para acessar sua conta ou aperte \"X\" para voltar\n")).upper()
        
        if escolha not in ["C", "L", "X"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue

        if escolha == "C":     
            cadastro_professor()  # Chama a função para cadastrar o professor
        elif escolha == "L":
            professor_email = login_professor() # Chama a função para logar o aluno
            if professor_email:
                menu_professor(professor_email)  # Chama a função para logar o professor
                estado = True
        
        elif escolha == "X":
            print("Voltar!")
            estado = True  # Volta para o menu anterior
            return
        
# Função para o menu principal do aluno (prova, ver resultado, desconectar)
def menu_aluno(email):
    estado_main_aluno = False

    while not estado_main_aluno:
        # Exibe as opções para o aluno
        menu_main_aluno = input("Digite:\n\n\"E\" Para editar os dados de sua conta\n\"D\" Para deletar sua conta\n\"X\" Para desconectar\n").upper()

        # Verifica as opções escolhidas pelo aluno
        if menu_main_aluno not in ["E","D","X"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue

        if menu_main_aluno == "E":
            editar_aluno(email) # Chama a função para editar a conta do aluno
        elif menu_main_aluno == "D":
            excluir_aluno(email) # Chama a função para excluir a conta do aluno
        elif menu_main_aluno == "X": 
            print("Desconectar!")  # Desconecta o aluno
            break

# Função para o menu principal do professor (relatório, gabarito, desconectar)
def menu_professor(email):

    while True:
        # Exibe as opções para o professor
        menu_main_professor = input("Digite:\n\n\"E\" Para editar os dados de sua conta\n\"D\" Para deletar sua conta\n\"X\" Para desconectar\n").upper()

        # Verifica as opções escolhidas pelo aluno
        if menu_main_professor not in ["E","D","X"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue

        # Verifica as opções escolhidas pelo professor
        if menu_main_professor == "E":
            editar_professor(email) # Chama a função para editar a conta do professor
        elif menu_main_professor == "D":
            excluir_professor(email) # Chama a função para excluir a conta do professor
        elif menu_main_professor == "X": 
            print("Desconectar!")  # Desconecta o aluno
            break

def main():
    carregar_usuarios()  # Carrega os dados dos usuários no início

    # Exibe uma mensagem de boas-vindas
    print("Bem-vindo ao nosso site.")
    verifica_user()

if __name__ == "__main__":
    main()