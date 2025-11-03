import sys
import os

path_code = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if path_code not in sys.path:
    sys.path.append(path_code)

from tkinter import *
import tkinter as tk
import customtkinter as ctk
import infra
import banco

def login():
    print("\nLOGIN\n")

    email = var_email.get().strip()
    senha = var_senha.get().strip()

    if not email or not senha:
        tk.messagebox.showerror("Erro de Validação", "Todos os campos devem ser preenchidos.")
        return

    if banco.users_db[email]['role'] == "USER" and infra.verificar_senha(senha, banco.users_db[email]["senha"]):
        print(f"Bem-vindo, {banco.users_db[email]['nome']}!")
        return email
    elif banco.users_db[email]['role'] == "INSTRUCTOR" and infra.verificar_senha(senha, banco.users_db[email]["senha"]):
        print(f"Bem-vindo, {banco.users_db[email]['nome']}!")
        return email
    else:
        print("Email ou senha incorretos!")
        return None

#Configuração da Janela Principal
janela_login = ctk.CTk()
janela_login.title("Cadastro de Usuário (CustomTkinter)")
janela_login.geometry("450x400")

def limpar_campos():
    var_email.set("")
    var_senha.set("")

def show_pass():
    pass

var_email = StringVar(janela_login)
var_senha = StringVar(janela_login)

linha = 0

# CAMPO EMAIL
ctk.CTkLabel(janela_login, text= "Email:", width= 100).grid(row= linha, column= 0, padx= 10, pady= 5, sticky= 'w')
ctk.CTkEntry(janela_login, textvariable= var_email, width= 300).grid(row= linha, column= 1, columnspan= 2, padx= 10, pady= 5)
linha += 1

# CAMPO SENHA
ctk.CTkLabel(janela_login, text= "Senha:", width= 100).grid(row= linha, column= 0, padx= 10, pady= 5, sticky= 'w')
ctk.CTkEntry(janela_login, textvariable= var_senha, show= "*", width= 300).grid(row= linha, column= 1, columnspan= 2, padx= 10, pady= 5)
linha += 1

ctk.CTkButton(
    janela_login, 
    text= "CADASTRAR USUÁRIO", 
    command= login,
    width= 380,
    fg_color="#4CAF50",
    hover_color="#45a049"
).grid(row= linha, column= 0, columnspan= 3, padx= 10, pady= 20)
linha += 1

janela_login.mainloop()
     