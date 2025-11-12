from database import banco
from infra import security as infra

def login():
    banco.carregar_usuarios()
    print("\nLOGIN\n")

    # Coleta as credenciais do aluno
    email = input("Email: ").strip().lower()
    senha = input("Senha: ").strip()

    if banco.users_db[email]['role'] == "USER" and infra.verificar_senha(senha, banco.users_db[email]["senha"]):
        print(f"Bem-vindo, {banco.users_db[email]['nome']}!")
        return email
    elif banco.users_db[email]['role'] == "INSTRUCTOR" and infra.verificar_senha(senha, banco.users_db[email]["senha"]):
        print(f"Bem-vindo, {banco.users_db[email]['nome']}!")
        return email
    else:
        print("Email ou senha incorretos!")
        return None