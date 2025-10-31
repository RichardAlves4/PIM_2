import os
import subprocess 
import json
import banco
import infra

C_exe = os.path.join(os.path.dirname(__file__), "..", "C", "cadastro.exe") 
TEMP_FILE = "temp_cadastro.json" 

def cadastro():
    print("\n--- INICIANDO CADASTRO ---")

    try:
        subprocess.run([C_exe], check=True, cwd=os.path.dirname(C_exe)) 
        
    except FileNotFoundError:
        print(f"\n ERRO: Executável C não encontrado em {C_exe}. Verifique o caminho e a compilação.")
        return
    except subprocess.CalledProcessError:
        print("\n ERRO: O programa C falhou. Verifique se o C gerou o arquivo JSON.")
        return
    
    # Define o caminho completo do arquivo temporário
    caminho_temp_file = os.path.join(os.path.dirname(C_exe), TEMP_FILE)

    # 2. LÊ OS DADOS DO ARQUIVO TEMPORÁRIO
    try:
        with open(caminho_temp_file, "r") as f:
            dados_novos = json.load(f)
    except Exception as e:
        print(f"\n ERRO: Falha ao ler ou decodificar o arquivo de dados do C. {e}")
        return
    finally:
        # Garante que o arquivo temporário seja removido após a leitura (limpeza)
        if os.path.exists(caminho_temp_file):
             os.remove(caminho_temp_file)

    # 3. VALIDAÇÃO DE EMAIL DUPLICADO E PROCESSAMENTO FINAL (Python)
    email = dados_novos.get('email', '').strip().lower()
    senha_simples = dados_novos.get('senha_simples', '') 

    # Validação de e-mail duplicado (crucial, pois o C não tem acesso ao banco)
    if email in banco.users_db: 
        print(f"\n ERRO: E-mail {email} já cadastrado.")
        return
    
    # Converte a senha (em Python, usando bcrypt/infra)
    try:
        senha_criptografada = infra.criptografar_senha(senha_simples)
    except Exception as e:
        print(f"\n ERRO: Falha na criptografia da senha. {e}")
        return

    # 4. SALVA NO BANCO DE DADOS PYTHON
    idade = int(dados_novos.get('idade', 0)) 
    
    banco.users_db[email] = {
        "nome": dados_novos.get('nome'), 
        "idade": idade, 
        "senha": senha_criptografada,
        "role": dados_novos.get('role')
    }

    banco.salvar_usuarios() 
    print("\n Cadastro realizado com sucesso e persistido no banco de dados Python!")
    return