import os
import json
import bcrypt

diretorio_bd = os.path.dirname(__file__)
arquivo_usuarios = os.path.join(diretorio_bd, "users.json")

users_db = {}

def gerar_rm():
    """Gera RM único para alunos no formato: 2024XXXXX"""
    ano_atual = "2024"
    dados = carregar_usuarios_raw()
    usuarios = dados.get("users", {})
    rms_existentes = [u.get('rm', '') for u in usuarios.values() if u.get('rm')]
    if not rms_existentes:
        return f"{ano_atual}00001"
    ultimo_numero = max([int(rm[4:]) for rm in rms_existentes if rm.startswith(ano_atual) and rm[4:].isdigit()] + [0])
    novo_numero = ultimo_numero + 1
    return f"{ano_atual}{novo_numero:05d}"

def carregar_usuarios_raw():
    """Carrega dados brutos do JSON"""
    try:
        with open(arquivo_usuarios, "r") as json_aberto:
            return json.load(json_aberto)
    except FileNotFoundError:
        return {"users": {}}
    except json.JSONDecodeError:
        return {"users": {}}

def carregar_usuarios():
    global users_db
    try:
        with open(arquivo_usuarios, "r") as json_aberto:
            dados = json.load(json_aberto)
            users_db.clear()
            users_db.update(dados.get("users", {}))
    except FileNotFoundError:
        print('Arquivo "usuarios.json" não encontrado. Um novo será criado quando salvar.')

def salvar_usuarios():
    with open(arquivo_usuarios, "w") as json_aberto:
        json.dump({"users": users_db}, json_aberto, indent=5)

def update_user(email):
    if email not in users_db:
        print("Usuário não encontrado.\n")
        return
    usuario = users_db[email]
    print("\nEditar conta\n(aperte Enter para manter o atual)")
    novo_nome = input(f"Nome atual ({usuario['nome']}): ")
    nova_senha = input("Nova senha (deixe vazio para não mudar): ")
    if novo_nome:
        usuario['nome'] = novo_nome
    if nova_senha:
        usuario['senha'] = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    users_db[email] = usuario
    salvar_usuarios()
    print("DADOS ATUALIZADOS COM SUCESSO!\n")

def delete_user(email):
    while True: 
        confirmacao = input("Tem certeza que deseja excluir sua conta? Esta ação é irreversível! (S/N): ").upper()
        if confirmacao not in ["S", "N"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue
        if confirmacao == 'S':
            users_db.pop(email, None)
            salvar_usuarios()
            print("Conta excluída com sucesso!\n")
            break
        else:
            print("Exclusão cancelada.\n")
            break

carregar_usuarios()
