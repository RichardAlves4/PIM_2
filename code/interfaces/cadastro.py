import sys
import os

path_code = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if path_code not in sys.path:
    sys.path.append(path_code)

from tkinter import *
import tkinter as tk
import customtkinter as ctk
import subprocess 
import json
import infra 
from banco import db as banco_db

# --- FUNÇÕES DE CONTROLE (Sem Alterações) ---
C_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "C", "cadastro.exe")
TEMP_FILE = "temp_cadastro.json"

# A função 'executar_cadastro()' permanece exatamente a mesma,
# pois ela lida apenas com as variáveis de controle (var_nome.get(), etc.)
# e com a lógica de negócio (subprocesso, JSON, banco).

# --- INTERFACE GRÁFICA CUSTOMTKINTER (PROGRAMA PRINCIPAL) ---

# 1. Configuração Inicial do CustomTkinter
ctk.set_appearance_mode("System")  # Ou "Dark", "Light"
ctk.set_default_color_theme("blue") # Ou "green", "dark-blue"

# 2. Configuração da Janela Principal (Substituição de tk.Tk por customtkinter.CTk)
janela = ctk.CTk()
janela.title("Cadastro de Usuário (CustomTkinter)")
janela.geometry("450x400") # Aumentei um pouco para melhor visualização

def limpar_campos():
    
    var_nome.set("")
    var_email.set("")
    var_idade.set(0) 
    var_senha1.set("")
    var_senha2.set("")
    var_role.set("USER") 

def executar_cadastro():
    
    # -----------------------------------------------------------
    # 1. COLETA E VALIDAÇÃO DA INTERFACE (Substitui o scanf/printf do C)
    # -----------------------------------------------------------
    
    # Coleta os dados dos campos de entrada (que são variáveis StringVar)
    nome = var_nome.get().strip()
    email = var_email.get().strip()
    senha1 = var_senha1.get().strip()
    senha2 = var_senha2.get().strip()
    role = var_role.get()
    
    try:
        idade = int(var_idade.get())
    except ValueError:
        tk.messagebox.showerror("Erro de Entrada", "Idade deve ser um número inteiro.")
        return

    # Validação de campos vazios (Sua lógica Python)
    if not nome or not email or not senha1 or not senha2:
        tk.messagebox.showerror("Erro de Validação", "Todos os campos devem ser preenchidos.")
        return

    # Validação de senhas (Sua lógica Python)
    if senha1 != senha2:
        tk.messagebox.showerror("Erro de Validação", "As senhas informadas são diferentes.")
        return
        
    # Validação de e-mail duplicado (crucial, sua lógica original)
    if email.lower() in banco_db.users_db: 
        # Substitui print("\n ERRO: E-mail já cadastrado.") por uma messagebox
        tk.messagebox.showerror("Erro de Cadastro", f"E-mail '{email}' já cadastrado. Tente outro.")
        return
    
    # -----------------------------------------------------------
    # 2. CHAMA O EXECUTÁVEL C COM ARGUMENTOS (Substitui a chamada sem args)
    # -----------------------------------------------------------
    
    caminho_temp_file = os.path.join(os.path.dirname(C_exe), TEMP_FILE)

    # Argumentos para o C: [role, nome, email, idade(str), senha]
    args_c = [C_exe, role, nome, email, str(idade), senha1]
    
    try:
        # Chama o C, passando os dados do formulário como argumentos.
        # Captura a saída de erro (stderr) para pegar erros de validação do C.
        subprocess.run(
            args_c, 
            check=True, 
            capture_output=True, 
            text=True, 
            cwd=os.path.dirname(C_exe)
        ) 
        
    except FileNotFoundError:
        # Substitui o print de erro do C por uma messagebox
        tk.messagebox.showerror("Erro Crítico", f"Executável C não encontrado em: {C_exe}")
        return
        
    except subprocess.CalledProcessError as e:
        # Trata erros de validação que vieram do C (ex: nome com números, email sem @gmail.com)
        erro_c = e.stderr.strip() if e.stderr else "O programa C falhou por erro desconhecido."
        
        # Tenta extrair a mensagem de erro de validação do C
        if erro_c.startswith("ERRO_VALIDACAO:"):
            mensagem_final = erro_c.split(":", 1)[-1].strip()
        else:
            mensagem_final = erro_c

        # Substitui o print de erro do C por uma messagebox
        tk.messagebox.showerror("Erro de Validação (C)", mensagem_final)
        return
    
    # -----------------------------------------------------------
    # 3. LÊ, PROCESSA E SALVA OS DADOS (Sua lógica original)
    # -----------------------------------------------------------

    # LÊ OS DADOS DO ARQUIVO TEMPORÁRIO
    try:
        with open(caminho_temp_file, "r") as f:
            dados_novos = json.load(f)
    except Exception as e:
        # Substitui print de erro por messagebox
        tk.messagebox.showerror("Erro de Leitura", f"Falha ao ler o JSON do C. {e}")
        return
    finally:
        # Garante a remoção do arquivo temporário
        if os.path.exists(caminho_temp_file):
            os.remove(caminho_temp_file)

    # PROCESSAMENTO E CRIPTOGRAFIA (Sua lógica original)
    email_limpo = dados_novos.get('email', '').strip().lower()
    senha_simples = dados_novos.get('senha_simples', '') 

    try:
        # Converte a senha (infra.py)
        senha_criptografada = infra.criptografar_senha(senha_simples)
    except Exception as e:
        # Substitui print de erro por messagebox
        tk.messagebox.showerror("Erro de Criptografia", f"Falha na criptografia da senha. {e}")
        return

    # SALVA NO BANCO DE DADOS PYTHON (Sua lógica original)
    banco_db.users_db[email_limpo] = {
        "nome": dados_novos.get('nome'), 
        "idade": dados_novos.get('idade', 0), 
        "senha": senha_criptografada,
        "role": dados_novos.get('role')
    }

    banco_db.salvar_usuarios() 
    
    # -----------------------------------------------------------
    # 4. SUCESSO E LIMPEZA
    # -----------------------------------------------------------
    
    # Substitui o print de sucesso por uma messagebox
    tk.messagebox.showinfo("Sucesso", "Cadastro realizado e persistido no banco de dados!")
    
    # Limpa os campos após o sucesso (Função auxiliar que você precisa implementar)
    limpar_campos() 
    
    return


# 3. Variáveis de Controle (permanecem as mesmas)
var_nome = StringVar(janela)
var_email = StringVar(janela)
var_idade = StringVar(janela, value=0)
var_senha1 = StringVar(janela)
var_senha2 = StringVar(janela)
var_role = StringVar(janela, value="USER")

# 4. Criação e Posicionamento dos Widgets (Substituição de prefixos)
linha = 0

# CAMPO ROLE (Estudante/Professor)
# customtkinter.CTkLabel no lugar de tk.Label
ctk.CTkLabel(janela, text="Perfil:", width=100).grid(row=linha, column=0, padx=10, pady=5, sticky='w')
# customtkinter.CTkRadioButton no lugar de tk.Radiobutton
ctk.CTkRadioButton(janela, text="Estudante", variable=var_role, value="USER").grid(row=linha, column=1, padx=5, pady=5, sticky='w')
ctk.CTkRadioButton(janela, text="Professor", variable=var_role, value="INSTRUCTOR").grid(row=linha, column=2, padx=5, pady=5, sticky='w')
linha += 1

# CAMPO NOME
ctk.CTkLabel(janela, text="Nome:", width=100).grid(row=linha, column=0, padx=10, pady=5, sticky='w')
# customtkinter.CTkEntry no lugar de tk.Entry
ctk.CTkEntry(janela, textvariable=var_nome, width=300).grid(row=linha, column=1, columnspan=2, padx=10, pady=5)
linha += 1

# CAMPO EMAIL
ctk.CTkLabel(janela, text="Email:", width=100).grid(row=linha, column=0, padx=10, pady=5, sticky='w')
ctk.CTkEntry(janela, textvariable=var_email, width=300).grid(row=linha, column=1, columnspan=2, padx=10, pady=5)
linha += 1

# CAMPO IDADE
ctk.CTkLabel(janela, text="Idade:", width=100).grid(row=linha, column=0, padx=10, pady=5, sticky='w')
ctk.CTkEntry(janela, textvariable=var_idade, width=100).grid(row=linha, column=1, padx=10, pady=5, sticky='w')
linha += 1

# CAMPO SENHA 1
ctk.CTkLabel(janela, text="Senha:", width=100).grid(row=linha, column=0, padx=10, pady=5, sticky='w')
ctk.CTkEntry(janela, textvariable=var_senha1, show="*", width=300).grid(row=linha, column=1, columnspan=2, padx=10, pady=5)
linha += 1

# CAMPO SENHA 2 (Repetição)
ctk.CTkLabel(janela, text="Repetir Senha:", width=100).grid(row=linha, column=0, padx=10, pady=5, sticky='w')
ctk.CTkEntry(janela, textvariable=var_senha2, show="*", width=300).grid(row=linha, column=1, columnspan=2, padx=10, pady=5)
linha += 1

# BOTÃO DE CADASTRO
# customtkinter.CTkButton no lugar de tk.Button
ctk.CTkButton(
    janela, 
    text="CADASTRAR USUÁRIO", 
    command=executar_cadastro,
    width=380,
    fg_color="#4CAF50", # Cor de fundo mais escura para o CustomTkinter
    hover_color="#45a049"
).grid(row=linha, column=0, columnspan=3, padx=10, pady=20)
linha += 1

# 5. Loop Principal (Mantém a janela aberta)
janela.mainloop()