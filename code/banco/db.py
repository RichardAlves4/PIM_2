# Importando a biblioteca json para manipulação de arquivos JSON
import os
import json
import bcrypt

# Diretório onde os arquivos serão guardados
diretorio_bd = os.path.dirname(__file__)

# Definindo o nome dos arquivos
arquivo_usuarios = os.path.join(diretorio_bd, "users.json")

# Dicionários para armazenar os dados de alunos e professores
usuarios_alunos = {}
usuarios_professores = {}

# RF12 - Função para carregar os usuários de um arquivo JSON
def carregar_usuarios():
    global usuarios_alunos, usuarios_professores
    try:
        # Tenta abrir o arquivo e carregar os dados
        with open(arquivo_usuarios, "r") as json_aberto:
            dados = json.load(json_aberto)
            # Limpa o que já existe na memória 
            usuarios_alunos.clear()
            usuarios_professores.clear()
            # Depois atualiza com os dados do arquivo
            usuarios_alunos.update(dados.get("alunos", {}))
            usuarios_professores.update(dados.get("professores", {}))
    except FileNotFoundError:
        print('Arquivo "usuarios.json" não encontrado. Um novo será criado quando salvar.')

# RF12 - Função para salvar os dados de usuários de volta no arquivo JSON
def salvar_usuarios():
    with open(arquivo_usuarios, "w") as json_aberto:
        json.dump({
            "alunos": usuarios_alunos,
            "professores": usuarios_professores
        }, json_aberto, indent=4)

# RF13 - Função para editar os dados do aluno
# Função para editar dados
def editar_aluno(email):
    usuario = usuarios_alunos.get(email)

    if usuario:
        print("\nEditar conta\n(aperte Enter para manter o atual)")

        novo_nome = input(f"Nome atual ({usuario['nome']}): ")
        nova_idade = input(f"Idade atual ({usuario['idade']}): ")
        nova_senha = input("Nova senha (deixe vazio para não mudar): ")

        if novo_nome:
            usuario['nome'] = novo_nome

        if nova_idade:
            usuario['idade'] = nova_idade
            
        if nova_senha:
            usuario['senha'] = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        usuarios_alunos[email] = usuario
        salvar_usuarios()
        print("DADOS ATUALIZADOS COM SUCESSO!\n")

    else:
        print("Usuário não encontrado.\n")

# RF14 - Função para excluir a conta do aluno mediante confirmação
# Função para excluir conta
def excluir_aluno(email):
    while True: 

        confirmacao = input("Tem certeza que deseja excluir sua conta? Esta ação é irreversível! (S/N): ").lower().upper()

        if confirmacao not in ["S", "n"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue

        if confirmacao == 'S':
            usuarios_alunos.pop(email, None)
            salvar_usuarios()
            print("Conta excluída com sucesso!\n")
            break

        else:
            print("Exclusão cancelada.\n")
            break

# RF13 - Função para editar os dados do professor
# Função para editar dados
def editar_professor(email):
    usuario = usuarios_professores.get(email)

    if usuario:
        print("\nEditar conta\n(aperte Enter para manter o atual)")

        novo_nome = input(f"Nome atual ({usuario['nome']}): ")
        nova_idade = input(f"Idade atual ({usuario['idade']}): ")
        nova_senha = input("Nova senha (deixe vazio para não mudar): ")

        if novo_nome:
            usuario['nome'] = novo_nome

        if nova_idade:
            usuario['idade'] = nova_idade
            
        if nova_senha:
            usuario['senha'] = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        usuarios_professores[email] = usuario
        salvar_usuarios()
        print("DADOS ATUALIZADOS COM SUCESSO!\n")

    else:
        print("Usuário não encontrado.\n")

# RF14 - Função para excluir a conta do professor mediante confirmação
# Função para excluir conta
def excluir_professor(email):
    while True: 

        confirmacao = input("Tem certeza que deseja excluir sua conta? Esta ação é irreversível! (S/N): ").lower().upper()

        if confirmacao not in ["S", "n"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue

        if confirmacao == 'S':
            usuarios_professores.pop(email, None)
            salvar_usuarios()
            print("Conta excluída com sucesso!\n")
            break

        else:
            print("Exclusão cancelada.\n")
            break
