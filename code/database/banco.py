import os
import json
import bcrypt

# Obtém o caminho do diretório onde este script está sendo executado.
diretorio_bd = os.path.dirname(__file__)
# Constrói o caminho completo para o arquivo 'users.json' dentro do mesmo diretório.
arquivo_usuarios = os.path.join(diretorio_bd, "users.json")

# Dicionário global que armazenará os dados dos usuários em memória durante a execução do programa.
users_db = {}

def gerar_rm():
    
    # Define o ano atual como parte fixa do RM.
    ano_atual = "2024"
    # Carrega todos os dados brutos do arquivo JSON para verificar os RMs existentes.
    dados = carregar_usuarios_raw()
    # Obtém o dicionário de usuários (ou um dicionário vazio se não existir).
    usuarios = dados.get("users", {})
    # Cria uma lista de RMs existentes, filtrando entradas vazias.
    rms_existentes = [u.get('rm', '') for u in usuarios.values() if u.get('rm')]

    # Se não houver RMs existentes, retorna o primeiro RM do ano.
    if not rms_existentes:
        return f"{ano_atual}00001"
        
    # Extrai o número sequencial (os 5 últimos dígitos) dos RMs que começam com o ano atual.
    # Converte para inteiro e encontra o maior número, usando 0 como valor inicial seguro.
    ultimo_numero = max([
        int(rm[4:]) for rm in rms_existentes 
        if rm.startswith(ano_atual) and rm[4:].isdigit()
    ] + [0])
    
    # Incrementa para gerar o novo número sequencial.
    novo_numero = ultimo_numero + 1
    # Retorna o RM formatado: ano_atual + novo_numero com 5 dígitos preenchidos com zeros à esquerda.
    return f"{ano_atual}{novo_numero:05d}"

def carregar_usuarios_raw():
    
    try:
        # Abre o arquivo JSON no modo de leitura ("r").
        with open(arquivo_usuarios, "r") as json_aberto:
            # Carrega e retorna o conteúdo do JSON.
            return json.load(json_aberto)
        
    except FileNotFoundError:
        # Retorna um dicionário vazio se o arquivo não existir.
        return {"users": {}}
    
    except json.JSONDecodeError:
        # Retorna um dicionário vazio se o arquivo estiver corrompido ou mal formatado.
        return {"users": {}}

def carregar_usuarios():
   
    # Declara que a função irá modificar a variável global 'users_db'.
    global users_db

    try:
        # Abre o arquivo JSON no modo de leitura ("r").
        with open(arquivo_usuarios, "r") as json_aberto:
            # Carrega o dicionário completo do arquivo.
            dados = json.load(json_aberto)
            # Limpa o dicionário em memória para garantir que não haja dados antigos.
            users_db.clear()
            # Atualiza o dicionário em memória com o conteúdo da chave "users" do arquivo.
            users_db.update(dados.get("users", {}))

    except FileNotFoundError:
        # Informa que o arquivo não existe, mas será criado ao salvar.
        print('Arquivo "usuarios.json" não encontrado. Um novo será criado quando salvar.')

def salvar_usuarios():
    
    # Abre o arquivo JSON no modo de escrita ("w").
    with open(arquivo_usuarios, "w") as json_aberto:
        # Cria um dicionário com a chave "users" contendo os dados do users_db e o salva.
        # 'indent=5' formata o JSON para melhor legibilidade.
        json.dump({"users": users_db}, json_aberto, indent=5)

def update_user(email):
    
    # Verifica se o email existe no banco de dados.
    if email not in users_db:
        print("Usuário não encontrado.\n")
        return
    
    # Obtém o dicionário de dados do usuário específico.
    usuario = users_db[email]
    
    print("\nEditar conta\n(aperte Enter para manter o atual)")
    # Solicita novo nome, mostrando o nome atual. Se o input for vazio, o nome não muda.
    novo_nome = input(f"Nome atual ({usuario['nome']}): ")
    # Solicita nova senha. Se o input for vazio, a senha não muda.
    nova_senha = input("Nova senha (deixe vazio para não mudar): ")

    # Se um novo nome foi fornecido (string não vazia), atualiza o campo 'nome'.
    if novo_nome:
        usuario['nome'] = novo_nome

    # Se uma nova senha foi fornecida (string não vazia):
    if nova_senha:
        # Gera um novo hash da senha. 'bcrypt.gensalt()' gera um salt único.
        # '.decode('utf-8')' converte o resultado do hash (bytes) de volta para string para armazenamento.
        usuario['senha'] = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Atualiza o registro do usuário no dicionário em memória (users_db).
    users_db[email] = usuario
    # Salva o dicionário atualizado no arquivo JSON.
    salvar_usuarios()
    print("DADOS ATUALIZADOS COM SUCESSO!\n")

def delete_user(email):
    
    while True: 
        # Solicita confirmação de exclusão.
        confirmacao = input("Tem certeza que deseja excluir sua conta? Esta ação é irreversível! (S/N): ").upper()
        
        # Validação da entrada.
        if confirmacao not in ["S", "N"]:
            print("\nOpção inválida. Tente novamente.\n")
            continue # Volta ao início do loop
            
        if confirmacao == 'S':
            # Remove o usuário do dicionário em memória. 'None' impede erro se o email não existir.
            users_db.pop(email, None) 
            # Salva o dicionário atualizado (sem o usuário) no arquivo JSON.
            salvar_usuarios()
            print("Conta excluída com sucesso!\n")
            break 
            
        else: 
            print("Exclusão cancelada.\n")
            break 

# Chama a função para carregar os dados dos usuários na memória ao iniciar o módulo.
carregar_usuarios()