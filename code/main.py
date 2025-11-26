import customtkinter as ctk
from tkinter import messagebox
import sys
from pathlib import Path

# Define o diretório base como o diretório pai do arquivo atual
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

# Caminho da rede onde ficará o users.json
DATABASE_DIR = Path(r"\\192.168.0.28\jsons")

# ================================
# CONFIGURA O BANCO DE DADOS AQUI
# ================================
import database.banco as banco  # importa o módulo inteiro primeiro
banco.set_diretorio_bd(str(DATABASE_DIR))  # envia o caminho da rede
# Só agora é seguro importar as funções
from database.banco import carregar_usuarios, salvar_usuarios, users_db, gerar_rm
# ================================

# Importa a função de verificação de senha
from infra.security import verificar_senha

# Importa telas
from screens.telas_professor import TelasProfessor
from screens.telas_aluno import TelasAluno
from screens.telas_admin import TelasAdmin

# Configura o CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
#import customtkinter as ctk # Importa o módulo para criar a interface gráfica
#from tkinter import messagebox # Importa a classe messagebox do tkinter para exibir caixas de diálogo (alertas, erros, sucesso)
#import sys # Importa o módulo sys para manipulação do sistema (ex: sair da aplicação)
#from pathlib import Path # Importa a classe Path do módulo pathlib para manipulação de caminhos de arquivos de forma orientada a objetos

# Define o diretório base como o diretório pai do arquivo atual
#BASE_DIR = Path(__file__).parent
# Insere o diretório base no caminho de busca do Python (necessário para importar módulos internos)
#sys.path.insert(0, str(BASE_DIR))

# Importa funções e variáveis do módulo de banco de dados local
#from database.banco import carregar_usuarios, salvar_usuarios, users_db, gerar_rm
# Importa a função de verificação de senha do módulo de segurança
#from infra.security import verificar_senha

# Importa as classes de tela para cada tipo de usuário
#from screens.telas_professor import TelasProfessor
#from screens.telas_aluno import TelasAluno
#from screens.telas_admin import TelasAdmin

# Configura o modo de aparência padrão do CustomTkinter para "dark"
#ctk.set_appearance_mode("dark")
# Configura o tema de cor padrão dos widgets para "blue"
#ctk.set_default_color_theme("blue")

# Define a classe principal da aplicação, herdando de ctk.CTk (a janela principal)
class SistemaGestaoEscolar(ctk.CTk):

    # Método construtor da classe
    def __init__(self):
        # Chama o construtor da classe pai (ctk.CTk)
        super().__init__()
        # Define o título da janela
        self.title("SGE - Sistema de Gestão Escolar")
        # Define o tamanho inicial da janela
        self.geometry("744x489")
        # Impede que a janela seja redimensionada
        self.resizable(False, False)
        # Chama o método para centralizar a janela na tela
        self.center_window()
        
        # Variáveis para armazenar o email e o papel (role) do usuário atualmente logado
        self.current_user_email = None
        self.current_user_role = None
        
        # Carrega os dados dos usuários do arquivo para a memória
        carregar_usuarios()
        
        # Exibe a tela inicial (Home Screen)
        self.show_home_screen()
    
    # Método para centralizar a janela na tela
    def center_window(self):
        # Atualiza o estado da janela para obter as dimensões corretas
        self.update_idletasks()
        # Obtém a largura da janela
        width = self.winfo_width()
        # Obtém a altura da janela
        height = self.winfo_height()
        # Calcula a coordenada X para centralizar a janela (metade da tela - metade da janela)
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        # Calcula a coordenada Y para centralizar a janela
        y = (self.winfo_screenheight() // 2) - (height // 2)
        # Aplica as novas dimensões e posição à janela
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    # Método para limpar todos os widgets da janela principal
    def clear_window(self):
        # Itera sobre todos os widgets filhos da janela
        for widget in self.winfo_children():
            # Destrói cada widget
            widget.destroy()
    
    # Método para exibir a tela inicial (Home Screen)
    def show_home_screen(self):
        # Limpa todos os widgets existentes na janela
        self.clear_window()

        # Cria um frame principal para conter o conteúdo da tela
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        # Empacota o frame para preencher toda a janela
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Rótulo do título principal do sistema
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🎓 SGE - Sistema de Gestão Escolar", 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        # Empacota o título com espaçamento
        title_label.pack(pady=(40, 10))

        # Rótulo de subtítulo/boas-vindas
        subtitle_label = ctk.CTkLabel(
            main_frame, 
            text="Bem-vindo! Acesse ou Crie uma Conta", 
            font=ctk.CTkFont(size=19)
        )
        subtitle_label.pack(pady=(0, 50))

        # Frame para agrupar os botões de ação (Login, Cadastro, Sair)
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)

        # Botão para ir para a tela de Login
        login_btn = ctk.CTkButton(
            buttons_frame, 
            text="🔐 Fazer Login", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            width=300, 
            height=60, 
            command=self.show_login_screen
        )
        login_btn.pack(pady=15)

        # Botão para ir para a tela de Cadastro
        cadastro_btn = ctk.CTkButton(
            buttons_frame, 
            text="📝 Criar Conta", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            width=300, 
            height=60, 
            command=self.show_cadastro_screen,
            fg_color="#2CC985", 
            hover_color="#25A066"
        )
        cadastro_btn.pack(pady=15)

        # Botão para Sair da Aplicação
        exit_btn = ctk.CTkButton(
            buttons_frame, 
            text="❌ Sair", 
            font=ctk.CTkFont(size=18), 
            width=300, 
            height=60, 
            command=self.quit_app,
            fg_color="#E74C3C", 
            hover_color="#C0392B"
        )
        exit_btn.pack(pady=15)

        # Rótulo de rodapé
        footer_label = ctk.CTkLabel(
            main_frame, 
            text="© 2024 SGE - Sistema de Gestão Escolar", 
            font=ctk.CTkFont(size=11), 
            text_color="gray"
        )
        # Empacota o rodapé no fundo da janela
        footer_label.pack(side="bottom", pady=27)
    
    # Método para exibir a tela de Cadastro de Novo Usuário
    def show_cadastro_screen(self):
        # Limpa todos os widgets existentes
        self.clear_window()

        # Cria um frame com barra de rolagem para o formulário de cadastro
        main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título da tela de Cadastro
        title_label = ctk.CTkLabel(
            main_frame, 
            text="📝 Criar Nova Conta", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        # Frame para agrupar os campos do formulário
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=10, padx=50, fill="x")

        # Rótulo e Rádio Buttons para seleção do Tipo de Usuário (Role)
        role_label = ctk.CTkLabel(
            form_frame, 
            text="Tipo de Usuário:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        role_label.grid(row=0, column=0, pady=(20, 5), padx=(20, 10), sticky="w")

        # Variável de controle para o Rádio Button, com valor padrão "USER" (Aluno)
        role_var = ctk.StringVar(value="USER")

        # Frame para agrupar os Rádio Buttons
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.grid(row=0, column=1, pady=(20, 5), padx=(10, 20), sticky="w")

        # Rádio Button para Aluno (USER)
        role_user = ctk.CTkRadioButton(
            role_frame, 
            text="👨‍🎓 Aluno", 
            variable=role_var, 
            value="USER"
        )
        role_user.pack(side="left", padx=5)

        # Rádio Button para Professor (INSTRUCTOR)
        role_instructor = ctk.CTkRadioButton(
            role_frame,
            text="👨‍🏫 Professor",
            variable=role_var,
            value="INSTRUCTOR"
        )
        role_instructor.pack(side="left", padx=5)

        # Campo Nome Completo
        name_label = ctk.CTkLabel(
            form_frame, 
            text="Nome Completo:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.grid(row=1, column=0, pady=(15, 5), padx=(20, 10), sticky="w")

        name_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Digite seu nome completo", 
            width=400, 
            height=40
        )
        name_entry.grid(row=1, column=1, pady=(15, 5), padx=(10, 20), sticky="w")

        # Campo Email
        email_label = ctk.CTkLabel(
            form_frame, 
            text="Email:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        email_label.grid(row=2, column=0, pady=(15, 5), padx=(20, 10), sticky="w")

        email_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="nome@aluno.sge.com.br ou nome@professor.sge.com.br", 
            width=400, 
            height=40
        )
        email_entry.grid(row=2, column=1, pady=(15, 5), padx=(10, 20), sticky="w")

        # Campo Senha
        password_label = ctk.CTkLabel(
            form_frame, 
            text="Senha:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        password_label.grid(row=3, column=0, pady=(15, 20), padx=(20, 10), sticky="w")

        password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Digite sua senha", 
            width=400, 
            height=40, 
            show="*" # Oculta a senha digitada
        )
        password_entry.grid(row=3, column=1, pady=(15, 20), padx=(10, 20), sticky="w")

        # Configuração das colunas do formulário (Coluna 0 fixa, Coluna 1 expansível)
        form_frame.grid_columnconfigure(0, weight=0, minsize=180)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Função interna para processar o cadastro ao clicar no botão
        def process_cadastro():
            # Obtém e limpa (remove espaços) os valores dos campos
            nome = name_entry.get().strip()
            email = email_entry.get().strip().lower()
            senha = password_entry.get()
            role = role_var.get()

            # Validação inicial: verifica se todos os campos foram preenchidos
            if not all([nome, email, senha]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            # Verifica se o email já está cadastrado no banco de dados
            if email in users_db:
                messagebox.showerror("Erro", "Este email já está cadastrado!")
                return
            
            # Importa a função de cadastro
            from modules.cadastro import cadastro_com_c
            # Chama a função de cadastro para validação de formato (email, etc.)
            sucesso, resultado = cadastro_com_c(role, nome, email, senha)

            # Se a validação da função cadastro_com_c falhar, exibe o erro
            if not sucesso:
                messagebox.showerror("Erro de Validação", resultado)
                return
            
            # Importa a função de criptografia de senha
            from infra.security import criptografar_senha
            # Obtém o email validado
            email_validado = resultado['email']
            # Cria um dicionário com os dados do novo usuário (incluindo senha criptografada)
            user_data = {"nome": nome, "email": email_validado, "role": role, "senha": criptografar_senha(senha)}

            # Se for aluno (USER), gera e adiciona um Registro de Matrícula (RM)
            if role == "USER":
                user_data['rm'] = gerar_rm()
            # Adiciona o novo usuário ao dicionário de usuários em memória
            users_db[email_validado] = user_data
            # Salva o dicionário de usuários no arquivo
            salvar_usuarios()
            # Recarrega os usuários
            carregar_usuarios()

            # Exibe mensagem de sucesso com RM, se for aluno
            if role == "USER":
                messagebox.showinfo("Sucesso", f"Conta criada com sucesso!\nBem-vindo, {nome}!\n\nSeu RM: {user_data['rm']}")
            # Exibe mensagem de sucesso para outros papéis (Professor/Admin)
            else:
                messagebox.showinfo("Sucesso", f"Conta criada com sucesso!\nBem-vindo, {nome}!")
            
            # Volta para a tela inicial
            self.show_home_screen()
        
        # Frame para os botões de ação do formulário
        buttons_frame = ctk.CTkFrame(
            form_frame, 
            fg_color="transparent"
        )
        # Posiciona o frame dos botões abaixo do formulário
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=30)

        # Botão para executar a ação de Cadastro
        cadastrar_btn = ctk.CTkButton(
            buttons_frame, 
            text="✓ Criar Conta", 
            font=ctk.CTkFont(size=16, weight="bold"), 
            width=200, 
            height=50, 
            command=process_cadastro,
            fg_color="#2CC985", 
            hover_color="#25A066"
        )
        cadastrar_btn.pack(side="left", padx=10)

        # Botão para Voltar à tela inicial
        back_btn = ctk.CTkButton(
            buttons_frame, 
            text="← Voltar", 
            font=ctk.CTkFont(size=16), 
            width=200, 
            height=50, 
            command=self.show_home_screen, 
            fg_color="gray", 
            hover_color="darkgray"
        )
        back_btn.pack(side="left", padx=10)
    
    # Método para exibir a tela de Login
    def show_login_screen(self):
        # Limpa todos os widgets existentes
        self.clear_window()

        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título da tela de Login
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🔐 Entrar no Sistema", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(50, 40))

        # Frame para agrupar o formulário de login
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=10, padx=100)

        # Campo Email
        email_label = ctk.CTkLabel(
            form_frame, 
            text="Email:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        email_label.pack(pady=(20, 5), anchor="w", padx=20)

        email_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="seu.email@aluno.sge.com.br", 
            width=400, 
            height=45
        )
        email_entry.pack(pady=(0, 20), padx=20)

        # Campo Senha
        password_label = ctk.CTkLabel(
            form_frame, 
            text="Senha:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        password_label.pack(pady=(10, 5), anchor="w", padx=20)

        password_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Digite sua senha", 
            width=400, 
            height=45, 
            show="*" # Oculta a senha digitada
        )
        password_entry.pack(pady=(0, 30), padx=20)
        
        # Função interna para processar o Login
        def process_login():
            # Obtém e normaliza o email para minúsculas
            email = email_entry.get().strip().lower()
            senha = password_entry.get()

            # Validação: verifica se os campos foram preenchidos
            if not email or not senha:
                messagebox.showerror("Erro", "Email e senha são obrigatórios!")
                return
            
            # Verifica se o usuário (email) existe no banco de dados em memória
            if email not in users_db:
                messagebox.showerror("Erro", "Usuário não encontrado!")
                return
            
            # Verifica a senha 
            if verificar_senha(senha, users_db[email]['senha']):
                # Login bem-sucedido: armazena as credenciais do usuário logado
                self.current_user_email = email
                self.current_user_role = users_db[email]['role']
                
                # Mensagem de boas-vindas
                messagebox.showinfo("Sucesso", f"Bem-vindo, {users_db[email]['nome']}!")
                
                # Redireciona o usuário para o menu apropriado
                self.redirect_to_menu()
            else:
                # Senha incorreta
                messagebox.showerror("Erro", "Senha incorreta!")
        
        # Frame para os botões de ação
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)

        # Botão para executar a ação de Login
        login_btn = ctk.CTkButton(
            buttons_frame, 
            text="✓ Entrar", 
            font=ctk.CTkFont(size=16, weight="bold"), 
            width=190, height=50, 
            command=process_login
        )
        login_btn.pack(side="left", padx=10)

        # Botão para Voltar à tela inicial
        back_btn = ctk.CTkButton(
            buttons_frame, 
            text="← Voltar", 
            font=ctk.CTkFont(size=16), 
            width=190, 
            height=50, 
            command=self.show_home_screen, 
            fg_color="gray", 
            hover_color="darkgray"
        )
        back_btn.pack(side="left", padx=10)
    
    # Método para redirecionar o usuário para a tela de menu correta com base no seu papel (role)
    def redirect_to_menu(self):
        # Redireciona para o menu do Administrador
        if self.current_user_role == "ADMIN":
            # Instancia TelasAdmin, passando a janela principal (self) e o email do usuário
            telas_admin = TelasAdmin(self, self.current_user_email)
            # Exibe o menu do administrador
            telas_admin.show_admin_menu()
        # Redireciona para o menu do Professor
        elif self.current_user_role == "INSTRUCTOR":
            telas_professor = TelasProfessor(self, self.current_user_email)
            telas_professor.show_professor_menu()
        # Redireciona para o menu do Aluno
        elif self.current_user_role == "USER":
            telas_aluno = TelasAluno(self, self.current_user_email)
            telas_aluno.show_aluno_menu()
        # Trata papéis de usuário inválidos
        else:
            messagebox.showerror("Erro", f"Tipo de usuário inválido: {self.current_user_role}")
            # Desloga o usuário em caso de erro
            self.logout()
    
    # Método para realizar o logout
    def logout(self):
        # Limpa as informações do usuário logado
        self.current_user_email = None
        self.current_user_role = None
        # Retorna para a tela inicial
        self.show_home_screen()
    
    # Método para fechar a aplicação
    def quit_app(self):
        # Salva o estado atual dos usuários antes de fechar
        salvar_usuarios()
        # Fecha o CustomTkinter
        self.quit()


# Função principal para iniciar a aplicação
def main():
    try:
        # Cria uma instância da classe principal da aplicação
        app = SistemaGestaoEscolar()
        # Inicia o loop principal do CustomTkinter (mantém a janela aberta)
        app.mainloop()
    # Bloco para capturar e tratar exceções (erros) durante a execução
    except Exception as e:
        # Importa o módulo traceback para obter a pilha de chamadas completa do erro
        import traceback
        # Imprime o cabeçalho do erro no console
        print("ERRO COMPLETO:")
        # Imprime o rastreamento completo do erro no console
        print(traceback.format_exc())
        # Exibe uma caixa de mensagem de erro fatal
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação:\n{str(e)}")
        # Sai da aplicação com código de erro 1
        sys.exit(1)

if __name__ == "__main__":
    main()
