import customtkinter as ctk
from tkinter import messagebox
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from database.banco import carregar_usuarios, salvar_usuarios, users_db, gerar_rm
from infra.security import verificar_senha

from screens.telas_professor import TelasProfessor
from screens.telas_aluno import TelasAluno
from screens.telas_admin import TelasAdmin

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class SistemaGestaoEscolar(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("SGE - Sistema de Gestão Escolar")
        self.geometry("744x489")
        self.resizable(False, False)
        self.center_window()
        self.current_user_email = None
        self.current_user_role = None
        carregar_usuarios()
        self.show_home_screen()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def show_home_screen(self):
        self.clear_window()
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text="🎓 SGE - Sistema de Gestão Escolar", font=ctk.CTkFont(size=32, weight="bold"))
        title_label.pack(pady=(40, 10))
        subtitle_label = ctk.CTkLabel(main_frame, text="Bem-vindo! Acesse ou Crie uma Conta", font=ctk.CTkFont(size=19))
        subtitle_label.pack(pady=(0, 50))
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)
        login_btn = ctk.CTkButton(buttons_frame, text="🔐 Fazer Login", font=ctk.CTkFont(size=18, weight="bold"), width=300, height=60, command=self.show_login_screen)
        login_btn.pack(pady=15)
        cadastro_btn = ctk.CTkButton(buttons_frame, text="📝 Criar Conta", font=ctk.CTkFont(size=18, weight="bold"), width=300, height=60, command=self.show_cadastro_screen, fg_color="#2CC985", hover_color="#25A066")
        cadastro_btn.pack(pady=15)
        exit_btn = ctk.CTkButton(buttons_frame, text="❌ Sair", font=ctk.CTkFont(size=18), width=300, height=60, command=self.quit_app, fg_color="#E74C3C", hover_color="#C0392B")
        exit_btn.pack(pady=15)
        footer_label = ctk.CTkLabel(main_frame, text="© 2024 SGE - Sistema de Gestão Escolar", font=ctk.CTkFont(size=11), text_color="gray")
        footer_label.pack(side="bottom", pady=27)
    
    def show_cadastro_screen(self):
        self.clear_window()
        main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text="📝 Criar Nova Conta", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=(20, 30))
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=10, padx=50, fill="x")
        role_label = ctk.CTkLabel(form_frame, text="Tipo de Usuário:", font=ctk.CTkFont(size=14, weight="bold"))
        role_label.grid(row=0, column=0, pady=(20, 5), padx=(20, 10), sticky="w")
        role_var = ctk.StringVar(value="USER")
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.grid(row=0, column=1, pady=(20, 5), padx=(10, 20), sticky="w")
        role_user = ctk.CTkRadioButton(role_frame, text="👨‍🎓 Aluno", variable=role_var, value="USER")
        role_user.pack(side="left", padx=5)
        role_instructor = ctk.CTkRadioButton(role_frame, text="👨‍🏫 Professor", variable=role_var, value="INSTRUCTOR")
        role_instructor.pack(side="left", padx=5)
        name_label = ctk.CTkLabel(form_frame, text="Nome Completo:", font=ctk.CTkFont(size=14, weight="bold"))
        name_label.grid(row=1, column=0, pady=(15, 5), padx=(20, 10), sticky="w")
        name_entry = ctk.CTkEntry(form_frame, placeholder_text="Digite seu nome completo", width=400, height=40)
        name_entry.grid(row=1, column=1, pady=(15, 5), padx=(10, 20), sticky="w")
        email_label = ctk.CTkLabel(form_frame, text="Email:", font=ctk.CTkFont(size=14, weight="bold"))
        email_label.grid(row=2, column=0, pady=(15, 5), padx=(20, 10), sticky="w")
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="nome@aluno.sge.com.br ou nome@professor.sge.com.br", width=400, height=40)
        email_entry.grid(row=2, column=1, pady=(15, 5), padx=(10, 20), sticky="w")
        password_label = ctk.CTkLabel(form_frame, text="Senha:", font=ctk.CTkFont(size=14, weight="bold"))
        password_label.grid(row=3, column=0, pady=(15, 20), padx=(20, 10), sticky="w")
        password_entry = ctk.CTkEntry(form_frame, placeholder_text="Digite sua senha", width=400, height=40, show="*")
        password_entry.grid(row=3, column=1, pady=(15, 20), padx=(10, 20), sticky="w")
        form_frame.grid_columnconfigure(0, weight=0, minsize=180)
        form_frame.grid_columnconfigure(1, weight=1)
        
        def process_cadastro():
            nome = name_entry.get().strip()
            email = email_entry.get().strip().lower()
            senha = password_entry.get()
            role = role_var.get()
            if not all([nome, email, senha]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            if email in users_db:
                messagebox.showerror("Erro", "Este email já está cadastrado!")
                return
            from modules.cadastro import cadastro_com_c
            sucesso, resultado = cadastro_com_c(role, nome, email, senha)
            if not sucesso:
                messagebox.showerror("Erro de Validação", resultado)
                return
            from infra.security import criptografar_senha
            email_validado = resultado['email']
            user_data = {"nome": nome, "email": email_validado, "role": role, "senha": criptografar_senha(senha)}
            if role == "USER":
                user_data['rm'] = gerar_rm()
            users_db[email_validado] = user_data
            salvar_usuarios()
            carregar_usuarios()
            if role == "USER":
                messagebox.showinfo("Sucesso", f"Conta criada com sucesso!\nBem-vindo, {nome}!\n\nSeu RM: {user_data['rm']}")
            else:
                messagebox.showinfo("Sucesso", f"Conta criada com sucesso!\nBem-vindo, {nome}!")
            self.show_home_screen()
        
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=30)
        cadastrar_btn = ctk.CTkButton(buttons_frame, text="✓ Criar Conta", font=ctk.CTkFont(size=16, weight="bold"), width=200, height=50, command=process_cadastro, fg_color="#2CC985", hover_color="#25A066")
        cadastrar_btn.pack(side="left", padx=10)
        back_btn = ctk.CTkButton(buttons_frame, text="← Voltar", font=ctk.CTkFont(size=16), width=200, height=50, command=self.show_home_screen, fg_color="gray", hover_color="darkgray")
        back_btn.pack(side="left", padx=10)
    
    def show_login_screen(self):
        self.clear_window()
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text="🔐 Entrar no Sistema", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=(50, 40))
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=10, padx=100)
        email_label = ctk.CTkLabel(form_frame, text="Email:", font=ctk.CTkFont(size=14, weight="bold"))
        email_label.pack(pady=(20, 5), anchor="w", padx=20)
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="seu.email@aluno.sge.com.br", width=400, height=45)
        email_entry.pack(pady=(0, 20), padx=20)
        password_label = ctk.CTkLabel(form_frame, text="Senha:", font=ctk.CTkFont(size=14, weight="bold"))
        password_label.pack(pady=(10, 5), anchor="w", padx=20)
        password_entry = ctk.CTkEntry(form_frame, placeholder_text="Digite sua senha", width=400, height=45, show="*")
        password_entry.pack(pady=(0, 30), padx=20)
        
        def process_login():
            email = email_entry.get().strip().lower()
            senha = password_entry.get()
            if not email or not senha:
                messagebox.showerror("Erro", "Email e senha são obrigatórios!")
                return
            if email not in users_db:
                messagebox.showerror("Erro", "Usuário não encontrado!")
                return
            if verificar_senha(senha, users_db[email]['senha']):
                self.current_user_email = email
                self.current_user_role = users_db[email]['role']
                messagebox.showinfo("Sucesso", f"Bem-vindo, {users_db[email]['nome']}!")
                self.redirect_to_menu()
            else:
                messagebox.showerror("Erro", "Senha incorreta!")
        
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        login_btn = ctk.CTkButton(buttons_frame, text="✓ Entrar", font=ctk.CTkFont(size=16, weight="bold"), width=190, height=50, command=process_login)
        login_btn.pack(side="left", padx=10)
        back_btn = ctk.CTkButton(buttons_frame, text="← Voltar", font=ctk.CTkFont(size=16), width=190, height=50, command=self.show_home_screen, fg_color="gray", hover_color="darkgray")
        back_btn.pack(side="left", padx=10)
    
    def redirect_to_menu(self):
        if self.current_user_role == "ADMIN":
            telas_admin = TelasAdmin(self, self.current_user_email)
            telas_admin.show_admin_menu()
        elif self.current_user_role == "INSTRUCTOR":
            telas_professor = TelasProfessor(self, self.current_user_email)
            telas_professor.show_professor_menu()
        elif self.current_user_role == "USER":
            telas_aluno = TelasAluno(self, self.current_user_email)
            telas_aluno.show_aluno_menu()
        else:
            messagebox.showerror("Erro", f"Tipo de usuário inválido: {self.current_user_role}")
            self.logout()
    
    def logout(self):
        self.current_user_email = None
        self.current_user_role = None
        self.show_home_screen()
    
    def quit_app(self):
        salvar_usuarios()
        self.quit()


def main():
    try:
        app = SistemaGestaoEscolar()
        app.mainloop()
    except Exception as e:
        import traceback
        print("ERRO COMPLETO:")
        print(traceback.format_exc())
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
