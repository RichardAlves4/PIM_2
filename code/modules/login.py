from database import banco 
from infra import security as infra 

def login():
    # Carrega os dados dos usuários do "banco de dados".
    banco.carregar_usuarios() 
    
    print("\nLOGIN\n")
    
    # Solicita o email, remove espaços em branco (strip) e converte para minúsculas (lower).
    email = input("Email: ").strip().lower() 
    # Solicita a senha, removendo espaços em branco.
    senha = input("Senha: ").strip() 

    # Bloco try-except para lidar com o caso em que o email não é encontrado no banco de dados.
    try:
        # Acessa os dados do usuário pelo email.
        user_data = banco.users_db[email] 

        # 1. Verifica se o papel (role) é "USER" E se a senha confere com a do banco de dados.
        if user_data['role'] == "USER" and infra.verificar_senha(senha, user_data["senha"]):
            print(f"Bem-vindo, {user_data['nome']}!")
            return email # Retorna o email em caso de sucesso.
        
        # 2. Verifica se o papel (role) é "INSTRUCTOR" E se a senha confere com a do banco de dados.
        elif user_data['role'] == "INSTRUCTOR" and infra.verificar_senha(senha, user_data["senha"]):
            print(f"Bem-vindo, {user_data['nome']}!")
            return email # Retorna o email em caso de sucesso.
        
        # 3. Caso o email exista, mas a senha ou o papel (role) não correspondam.
        else:
            print("Email ou senha incorretos!")
            return None
            
    # Lida com o erro se a chave (email) não for encontrada em banco.users_db.
    except KeyError:
        print("Email ou senha incorretos!")
        return None