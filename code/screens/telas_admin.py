# Importa as bibliotecas necessárias para a interface gráfica e funções utilitárias
import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime


# Define a classe para as telas administrativas/de professor, centralizando a lógica da UI
class TelasAdmin:
    
    # Construtor da classe, recebe a aplicação principal (app) e o email do usuário logado
    def __init__(self, app, user_email):
        self.app = app # Referência à janela principal do customtkinter
        self.user_email = user_email # Email do administrador/professor logado
        
    def show_editar_turma(self, turma):
        """
        Cria e exibe uma janela pop-up (Toplevel) para editar os detalhes de uma turma existente.
        """
        # Cria a janela pop-up
        dialog = ctk.CTkToplevel(self.app)
        dialog.title(f"Editar Turma: {turma['nome']}")
        dialog.geometry("700x750")  
        dialog.grab_set() # Bloqueia interação com a janela principal (modal)
        dialog.resizable(height=False, width=False)

        # Frame principal com barra de rolagem
        main_frame = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título da janela de edição
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"✏️ Editar Turma: {turma['nome']}",
            font=ctk.CTkFont(size=24, weight="bold"),
            wraplength=400
        )
        title_label.pack(pady=(20, 30))
        
        # Frame para agrupar os campos do formulário
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=10, padx=80, fill="x")
        
        # Campo: Nome da Turma
        nome_label = ctk.CTkLabel(
            form_frame, 
            text="Nome da Turma:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        nome_label.pack(pady=(20, 5), padx=20, anchor="w")

        nome_entry = ctk.CTkEntry(
            form_frame, 
            height=40
        )
        nome_entry.insert(0, turma.get('nome', ''))
        nome_entry.pack(pady=(0, 15), padx=20, fill="x")
        
        # Campo: Disciplina
        disciplina_label = ctk.CTkLabel(
            form_frame, 
            text="Disciplina:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        disciplina_label.pack(pady=(15, 5), padx=20, anchor="w")

        disciplina_entry = ctk.CTkEntry(
            form_frame, 
            height=40
        )
        disciplina_entry.insert(0, turma.get('disciplina', ''))
        disciplina_entry.pack(pady=(0, 15), padx=20, fill="x")
        
        # Campo: Ano Letivo
        ano_label = ctk.CTkLabel(
            form_frame, 
            text="Ano Letivo:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        ano_label.pack(pady=(15, 5), padx=20, anchor="w")

        ano_entry = ctk.CTkEntry(
            form_frame, 
            height=40
        )
        ano_entry.insert(0, turma.get('ano', ''))
        ano_entry.pack(pady=(0, 15), padx=20, fill="x")
        
        # Campo: Período
        periodo_label = ctk.CTkLabel(
            form_frame, 
            text="Período:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        periodo_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        periodo_var = ctk.StringVar(value=turma.get('periodo', 'Manhã'))

        periodo_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        periodo_frame.pack(pady=(0, 15), padx=20, anchor="w")
        
        periodos = ["Manhã", "Tarde", "Noite", "Integral"]

        for periodo in periodos:
            rb = ctk.CTkRadioButton(
                periodo_frame, 
                text=periodo, 
                variable=periodo_var, 
                value=periodo
            )
            rb.pack(side="left", padx=5)
        
        # Campo: Professor Responsável
        prof_label = ctk.CTkLabel(
            form_frame, 
            text="Professor:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        prof_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        # Importa função para listar professores
        from backend.turmas_backend import get_professores_disponiveis
        professores = get_professores_disponiveis()
        
        if not professores:
            # Mensagem de erro se não houver professores
            ctk.CTkLabel(
                form_frame,
                text="⚠️ Nenhum professor cadastrado no sistema",
                text_color="#E74C3C"
            ).pack(pady=(0, 15), padx=20, anchor="w")
            professor_var = None
        else:
            # Prepara as opções do menu
            professor_options = [f"{p['nome']} ({p['email']})" for p in professores]
            professor_map = {f"{p['nome']} ({p['email']})": p['email'] for p in professores}
            
            # Tenta preselecionar o professor atual da turma
            professor_atual = f"{turma.get('professor_nome', 'N/A')} ({turma.get('professor_email', 'N/A')})"

            if professor_atual not in professor_options:
                professor_atual = professor_options[0] if professor_options else None
            
            professor_var = ctk.StringVar(value=professor_atual)
            
            # Cria o OptionMenu
            professor_menu = ctk.CTkOptionMenu(
                form_frame,
                variable=professor_var,
                values=professor_options,
                width=600,
                height=40
            )
            professor_menu.pack(pady=(0, 15), padx=20)

        # Campo: Descrição
        descricao_label = ctk.CTkLabel(
            form_frame, 
            text="Descrição:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        descricao_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        descricao_text = ctk.CTkTextbox(
            form_frame, 
            height=100
        )
        descricao_text.insert("0.0", turma.get('descricao', ''))
        descricao_text.pack(pady=(0, 20), padx=20, fill="x")
        
        # Função chamada ao clicar em "Salvar Alterações"
        def salvar_edicao():
            # Coleta os dados dos campos
            nome = nome_entry.get().strip()
            disciplina = disciplina_entry.get().strip()
            ano = ano_entry.get().strip()
            periodo = periodo_var.get()
            descricao = descricao_text.get("1.0", "end-1c").strip()
            
            # Validação básica
            if not all([nome, disciplina, ano]):
                messagebox.showerror("Erro", "Nome, Disciplina e Ano são obrigatórios!")
                return
            
            # Importa funções para edição e atribuição
            from backend.turmas_backend import editar_turma, atribuir_professor_turma, get_detalhes_completos_turma
            sucesso = editar_turma(turma['id'], nome, disciplina, ano, periodo, descricao)
            
            if not sucesso:
                messagebox.showerror("Erro", "Erro ao salvar edição da turma.")
                return
            
            # Atribui o novo professor, se houver opções disponíveis
            if professor_var and professores:
                professor_email = professor_map.get(professor_var.get())
                if professor_email:
                    sucesso_prof, msg_prof = atribuir_professor_turma(turma['id'], professor_email)
                    if not sucesso_prof:
                        # Exibe aviso se a atribuição do professor falhar, mas a turma foi editada
                        messagebox.showwarning("Aviso", f"Turma editada, mas: {msg_prof}")
            
            messagebox.showinfo("Sucesso", "Turma atualizada com sucesso!")
            dialog.destroy() # Fecha a janela de edição
            
            # Recarrega os detalhes completos e exibe a tela de detalhes atualizada
            turma_atualizada = get_detalhes_completos_turma(turma['id'])
            self.show_detalhes_turma(turma_atualizada) 
        
        # Frame para os botões na parte inferior
        button_wrapper_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_wrapper_frame.pack(pady=(10, 20))

        # Botão Salvar
        create_btn = ctk.CTkButton(
            button_wrapper_frame,
            text="✓ Salvar Alterações",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=50,
            command=salvar_edicao,
            fg_color="#2CC985",
            hover_color="#25A066"
        )
        create_btn.pack(side="left", padx=10)
        
        # Botão Cancelar
        cancel_btn = ctk.CTkButton(
            button_wrapper_frame,
            text="← Cancelar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=dialog.destroy, # Fecha a janela
            fg_color="gray",
            hover_color="darkgray"
        )
        cancel_btn.pack(side="left", padx=10)
        
    # Função para exibir as turmas de um professor
    def show_turmas_professor(self):
        """
        Exibe a lista de turmas associadas ao usuário logado (professor).
        Permite visualizar detalhes e editar turmas.
        """
        self.app.clear_window() # Limpa o conteúdo da janela principal
        
        # Frame principal com barra de rolagem
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="📚 Minhas Turmas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Busca as turmas do professor logado
        from backend.turmas_backend import get_turmas_professor
        turmas = get_turmas_professor(self.user_email)
        
        if not turmas:
            # Mensagem se não houver turmas
            empty_label = ctk.CTkLabel(
                main_frame,
                text="Você ainda não possui turmas cadastradas.\nClique em 'Criar Nova Turma' para começar!",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            # Itera sobre as turmas e cria um item de lista para cada uma
            for turma in turmas:
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=10, padx=40, fill="x")
                
                # Frame para informações da turma (lado esquerdo)
                info_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                # Nome da Turma
                nome_label = ctk.CTkLabel(
                    info_frame,
                    text=f"📖 {turma['nome']}",
                    font=ctk.CTkFont(size=18, weight="bold")
                )
                nome_label.pack(anchor="w")
                
                # Disciplina
                disciplina_label = ctk.CTkLabel(
                    info_frame,
                    text=f"Disciplina: {turma['disciplina']}",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                disciplina_label.pack(anchor="w", pady=2)
                
                # Total de Alunos e Ano
                info_label = ctk.CTkLabel(
                    info_frame,
                    text=f"Alunos: {turma['total_alunos']} | Ano: {turma['ano']}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                )
                info_label.pack(anchor="w", pady=2)
                
                # Frame para os botões (lado direito)
                buttons_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                buttons_frame.pack(side="right", padx=10, pady=10)
                
                # Botão Ver Detalhes
                view_btn = ctk.CTkButton(
                    buttons_frame,
                    text="Ver Detalhes",
                    width=120,
                    height=35,
                    # Chama show_detalhes_turma
                    command=lambda t=turma: self.show_detalhes_turma(t)
                )
                view_btn.pack(pady=3)
                
                # Botão Editar
                edit_btn = ctk.CTkButton(
                    buttons_frame,
                    text="Editar",
                    width=120,
                    height=35,
                    fg_color="#9B59B6",
                    hover_color="#7D3C98",
                    # Chama show_editar_turma
                    command=lambda t=turma: self.show_editar_turma(t)
                )
                edit_btn.pack(pady=3)
        
        # Botão Voltar
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_professor_menu,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
        
    def show_criar_turma(self):
        """
        Exibe a tela com o formulário para a criação de uma nova turma.
        """
        self.app.clear_window() # Limpa o conteúdo da janela principal

        # Container com scroll
        scroll_container = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        main_frame = ctk.CTkFrame(scroll_container, corner_radius=0)
        main_frame.pack(padx=20, pady=20, fill="x")
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="➕ Criar Nova Turma",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Frame do Formulário
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=10, padx=80, fill="x") 
        
        # Campo: Professor Responsável
        prof_label = ctk.CTkLabel(
            form_frame, 
            text="Professor Responsável:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        prof_label.pack(pady=(20, 5), padx=20, anchor="w")

        # Busca professores disponíveis
        from backend.turmas_backend import get_professores_disponiveis
        professores = get_professores_disponiveis()

        if not professores:
            # Mensagem de erro se não houver professores
            ctk.CTkLabel(
                form_frame,
                text="⚠️ Cadastre professores antes de criar turmas!",
                text_color="#E74C3C"
            ).pack(pady=(0, 15), padx=20, anchor="w")
            professor_var = None
        else:
            # Prepara opções e mapeamento de email
            professor_options = [f"{p['nome']} ({p['email']})" for p in professores]
            professor_map = {f"{p['nome']} ({p['email']})": p['email'] for p in professores}
            
            professor_var = ctk.StringVar(value=professor_options[0]) # Seleciona o primeiro por padrão
            
            professor_menu = ctk.CTkOptionMenu(
                form_frame,
                variable=professor_var,
                values=professor_options,
                width=600,
                height=40
            )
            professor_menu.pack(pady=(0, 15), padx=20)
        
        # Campo: Nome da Turma
        nome_label = ctk.CTkLabel(
            form_frame, 
            text="Nome da Turma:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        nome_label.pack(pady=(20, 5), padx=20, anchor="w") 
        
        nome_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Ex: Turma A - 2024", 
            height=40
        )
        nome_entry.pack(pady=(0, 15), padx=20, fill="x") 
        
        # Campo: Disciplina
        disciplina_label = ctk.CTkLabel(
            form_frame, 
            text="Disciplina:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        disciplina_label.pack(pady=(15, 5), padx=20, anchor="w") 
        
        disciplina_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Ex: Matemática", 
            height=40
        )
        disciplina_entry.pack(pady=(0, 15), padx=20, fill="x") 
        
        # Campo: Ano Letivo
        ano_label = ctk.CTkLabel(
            form_frame, 
            text="Ano Letivo:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        ano_label.pack(pady=(15, 5), padx=20, anchor="w") 
        
        ano_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Ex: 2024", 
            height=40
        )
        ano_entry.pack(pady=(0, 15), padx=20, fill="x") 
        
        # Campo: Período
        periodo_label = ctk.CTkLabel(
            form_frame, 
            text="Período:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        periodo_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        periodo_var = ctk.StringVar(value="Manhã")

        periodo_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        periodo_frame.pack(pady=(0, 15), padx=20, anchor="w") 
        
        periodos = ["Manhã", "Tarde", "Noite", "Integral"]
        for periodo in periodos:
            rb = ctk.CTkRadioButton(
                periodo_frame, 
                text=periodo, 
                variable=periodo_var, 
                value=periodo
            )
            rb.pack(side="left", padx=5) 
        
        # Campo: Descrição
        descricao_label = ctk.CTkLabel(
            form_frame, 
            text="Descrição:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        descricao_label.pack(pady=(15, 5), padx=20, anchor="w") 
        
        descricao_text = ctk.CTkTextbox(
            form_frame, 
            height=100
        )
        descricao_text.pack(pady=(0, 20), padx=20, fill="x")
        
        # Função chamada ao criar a turma
        def process_criar():
            # Coleta os dados
            nome = nome_entry.get().strip()
            disciplina = disciplina_entry.get().strip()
            ano = ano_entry.get().strip()
            periodo = periodo_var.get()
            descricao = descricao_text.get("1.0", "end-1c").strip()
            
            # Validação
            if not all([nome, disciplina, ano]):
                messagebox.showerror("Erro", "Nome, Disciplina e Ano são obrigatórios!")
                return
            
            if not professor_var or not professores:
                messagebox.showerror("Erro", "Selecione um professor!")
                return
            
            professor_email = professor_map.get(professor_var.get())
            
            # Chama a função para criar a turma
            from backend.turmas_backend import criar_turma, get_turma_por_id
            turma_id = criar_turma(professor_email, nome, disciplina, ano, periodo, descricao)
            
            if turma_id:
                messagebox.showinfo("Sucesso", "Turma criada com sucesso!")
                # Redireciona para a tela de detalhes da turma recém-criada
                turma = get_turma_por_id(turma_id)
                if turma:
                    self.show_detalhes_turma_criada(turma)
                else:
                    self.show_admin_menu()
            else:
                messagebox.showerror("Erro", "Erro ao criar turma!")
        
        # Frame dos botões
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(pady=20) 
        
        # Botão Criar
        create_btn = ctk.CTkButton(
            buttons_frame,
            text="✓ Criar Turma",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=50,
            command=process_criar,
            fg_color="#2CC985",
            hover_color="#25A066"
        )
        create_btn.pack(side="left", padx=10)
        
        # Botão Voltar
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_admin_menu, # Volta para o menu do administrador
            fg_color="gray",
            hover_color="darkgray"
        )
        cancel_btn.pack(side="left", padx=10)
    
    # Exibe os detalhes de uma turma (usado após a criação)
    def show_detalhes_turma_criada(self, turma):
        """
        Exibe a tela de detalhes de uma turma recém-criada, focando na matrícula de alunos.
        """
        self.app.clear_window() 
        
        # Frame principal com scroll
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título da Turma
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📖 {turma['nome']}",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Informações da Turma
        info_label = ctk.CTkLabel(
            main_frame,
            text=f"{turma['disciplina']} | {turma['ano']} | {turma['periodo']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info_label.pack(pady=(0, 30))
        
        # Busca alunos matriculados na turma
        from backend.turmas_backend import get_alunos_turma
        alunos = get_alunos_turma(turma['id'])
        
        # Frame de Alunos Matriculados
        alunos_frame = ctk.CTkFrame(main_frame)
        alunos_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Subtítulo Alunos
        ctk.CTkLabel(
            alunos_frame,
            text="👥 Alunos Matriculados",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15)
        
        if not alunos:
            # Mensagem se não houver alunos
            ctk.CTkLabel(
                alunos_frame,
                text="Nenhum aluno matriculado ainda.",
                text_color="gray"
            ).pack(pady=20)
        else:
            # Lista os alunos
            for aluno in alunos:
                aluno_frame = ctk.CTkFrame(alunos_frame)
                aluno_frame.pack(pady=5, padx=10, fill="x")
                
                ctk.CTkLabel(
                    aluno_frame,
                    text=f"👤 {aluno['nome']} - {aluno['email']}",
                    font=ctk.CTkFont(size=14)
                ).pack(side="left", padx=20, pady=10)
        
        # Botão para adicionar aluno (chama a função de adicionar aluno)
        add_aluno_btn = ctk.CTkButton(
            alunos_frame,
            text="➕ Adicionar Aluno",
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2CC985",
            hover_color="#25A066",
            command=lambda: self.show_adicionar_aluno_criada(turma)
        )
        add_aluno_btn.pack(pady=15)
        
        # Botão Voltar para o menu principal
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar ao Menu",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_admin_menu, # Volta para o menu do administrador
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    # Importa o módulo CustomTkinter (ctk) e messagebox do Tkinter
    import customtkinter as ctk
    from tkinter import messagebox

    # Define a função para exibir a janela de adição de aluno
    def show_adicionar_aluno_criada(self, turma):
        # Cria uma nova janela de nível superior que é uma janela flutuante sobre a principal
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Adicionar Aluno")
        dialog.geometry("550x500")
        # Captura todos os eventos de mouse e teclado, forçando interação apenas com este diálogo
        dialog.grab_set()
        # Impede que o usuário redimensione a janela
        dialog.resizable(height=False, width=False)
        
        # Cria um frame rolável para conter os elementos do diálogo
        main_scroll = ctk.CTkScrollableFrame(dialog, width=500, height=420)
        # Empacota o frame, preenchendo o espaço e expandindo
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cria um rótulo de título dentro do frame rolável
        title = ctk.CTkLabel(
            main_scroll,
            text="Adicionar Aluno à Turma",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=20)
        
        # Importa a função para obter alunos que ainda não estão na turma
        from backend.turmas_backend import get_alunos_disponiveis
        # Chama a função para obter a lista de alunos disponíveis
        alunos_disponiveis = get_alunos_disponiveis(turma['id'])
        
        # Verifica se há alunos disponíveis
        if not alunos_disponiveis:
            # Se não houver, exibe uma mensagem no frame rolável
            ctk.CTkLabel(
                main_scroll,
                text="Não há alunos disponíveis",
                text_color="gray"
            ).pack(pady=20)
            # Retorna, encerrando a função
            return
        
        # Cria uma variável de controle StringVar para armazenar o email do aluno selecionado. Inicializa com o primeiro da lista.
        selected_aluno = ctk.StringVar(value=alunos_disponiveis[0]['email'])
        
        # Itera sobre a lista de alunos disponíveis para criar um RadioButton para cada um
        for aluno in alunos_disponiveis:
            rb = ctk.CTkRadioButton(
                main_scroll,
                text=f"{aluno['nome']} - {aluno['email']}",
                variable=selected_aluno, # Vincula ao StringVar
                value=aluno['email']    # Define o valor que será armazenado ao selecionar
            )
            # Empacota o RadioButton, alinhado à esquerda
            rb.pack(pady=5, padx=20, anchor="w")
        
        # Define a função de callback para o botão "Adicionar"
        def add_aluno():
            # Importa a funçãopara adicionar o aluno à turma
            from backend.turmas_backend import adicionar_aluno_turma
            # Chama a função com o ID da turma e o email do aluno selecionado
            sucesso = adicionar_aluno_turma(turma['id'], selected_aluno.get())

            if sucesso:
                # Exibe mensagem de sucesso
                messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
                # Fecha a janela de diálogo
                dialog.destroy()
                # Chama função para atualizar e exibir os detalhes da turma
                self.show_detalhes_turma_criada(turma)
            else:
                # Exibe mensagem de erro
                messagebox.showerror("Erro", "Erro ao adicionar aluno!")
        
        # Cria e empacota o botão "Adicionar"
        ctk.CTkButton(
            main_scroll,
            text="Adicionar",
            command=add_aluno,
            width=200,
            fg_color="#2CC985"
        ).pack(pady=20)

    # Função para exibir a tela de detalhes de uma turma
    def show_detalhes_turma(self, turma):
        # Limpa o conteúdo da janela principal do aplicativo
        self.app.clear_window()
        
        # Cria um frame rolável principal para a tela de detalhes
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Rótulo para o título da turma
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📖 {turma['nome']}",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Rótulo para informações adicionais da turma (disciplina, ano, período)
        info_label = ctk.CTkLabel(
            main_frame,
            text=f"{turma['disciplina']} | {turma['ano']} | {turma['periodo']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info_label.pack(pady=(0, 30))
        
        # Cria uma visualização de abas (Tabview) para organizar Alunos, Aulas e Atividades
        tabs = ctk.CTkTabview(
            main_frame, 
            width=800, 
            height=400
        )
        tabs.pack(pady=20, padx=40)
        
        # Adiciona as abas
        tabs.add("👥 Alunos")
        tabs.add("📝 Aulas")
        tabs.add("📋 Atividades")
        
        # Importa as funções para obter dados da turma
        from backend.turmas_backend import get_alunos_turma, get_aulas_turma, get_atividades_turma
        # Obtém a lista de alunos matriculados
        alunos = get_alunos_turma(turma['id'])

        # Itera sobre os alunos para exibir na aba "Alunos"
        for aluno in alunos:
            # Cria um frame para cada aluno
            aluno_frame = ctk.CTkFrame(tabs.tab("👥 Alunos"))
            aluno_frame.pack(pady=5, padx=10, fill="x")
            
            # Rótulo com nome e email do aluno
            ctk.CTkLabel(
                aluno_frame,
                text=f"👤 {aluno['nome']} - {aluno['email']}",
                font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=20, pady=10)
        
        # Botão para adicionar novo aluno, chama show_adicionar_aluno
        add_aluno_btn = ctk.CTkButton(
            tabs.tab("👥 Alunos"),
            text="➕ Adicionar Aluno",
            width=200,
            command=lambda: self.show_adicionar_aluno(turma) # Usa lambda para passar o argumento 'turma'
        )
        add_aluno_btn.pack(pady=10)
        
        # Obtém a lista de aulas
        aulas = get_aulas_turma(turma['id'])

        # Verifica se há aulas registradas
        if not aulas:
            # Exibe mensagem se não houver aulas
            ctk.CTkLabel(tabs.tab("📝 Aulas"), text="Nenhuma aula registrada", text_color="gray").pack(pady=20)
        else:
            # Itera sobre as aulas para exibição na aba "Aulas"
            for aula in aulas:
                # Cria um frame para cada aula
                aula_frame = ctk.CTkFrame(tabs.tab("📝 Aulas"))
                aula_frame.pack(pady=5, padx=10, fill="x")
                
                # Rótulo com a data e título da aula
                ctk.CTkLabel(
                    aula_frame,
                    text=f"📅 {aula['data']} - {aula['titulo']}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    wraplength=550 # Limita o comprimento do texto antes de quebrar a linha
                ).pack(anchor="w", padx=20, pady=(10, 5))
                
                # Campo de texto (Textbox) para exibir o conteúdo da aula
                conteudo_aula = ctk.CTkTextbox(
                    aula_frame,
                    font=ctk.CTkFont(size=13),
                    text_color="gray",
                    wrap="word",
                    height=120,
                )
                conteudo_aula.pack(anchor="w", pady=(5, 2), fill="x", expand=True)
                # Insere o conteúdo e desabilita a edição
                conteudo_aula.insert("0.0", aula['conteudo'])
                conteudo_aula.configure(state="disabled")
        
        # Obtém a lista de atividades
        atividades = get_atividades_turma(turma['id'])

        # Verifica se há atividades criadas
        if not atividades:
            # Exibe mensagem se não houver atividades
            ctk.CTkLabel(tabs.tab("📋 Atividades"), text="Nenhuma atividade criada", text_color="gray").pack(pady=20)
        else:
            # Itera sobre as atividades para exibição na aba "Atividades"
            for atividade in atividades:
                # Cria um frame para cada atividade
                ativ_frame = ctk.CTkFrame(tabs.tab("📋 Atividades"))
                ativ_frame.pack(pady=5, padx=10, fill="x")
                
                # Rótulo com detalhes da atividade
                ctk.CTkLabel(
                    ativ_frame,
                    text=f"📄 {atividade['titulo']} | Criado em: {atividade['data_criacao']} | Entrega: {atividade['data_entrega']} | Valor: {atividade['valor']} pts",
                    font=ctk.CTkFont(size=13),
                    wraplength=500
                ).pack(side="left", padx=20, pady=10)
        
        # Botão para criar nova atividade
        add_ativ_btn = ctk.CTkButton(
            tabs.tab("📋 Atividades"),
            text="➕ Criar Atividade",
            width=200,
            command=lambda: self.show_criar_atividade(turma)
        )
        add_ativ_btn.pack(pady=10)
        
        # Botão de "Voltar" que retorna para o menu do administrador
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_admin_menu,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)

    # Função para exibir a janela de adição de aluno
    def show_adicionar_aluno(self, turma):
        # Cria e configura a janela de diálogo
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Adicionar Aluno")
        dialog.geometry("550x500")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)
        
        # Cria o frame rolável
        main_scroll = ctk.CTkScrollableFrame(dialog, width=500, height=420)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Rótulo de título
        title = ctk.CTkLabel(
            main_scroll,
            text="Adicionar Aluno à Turma",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=20)
        
        # Obtém a lista de alunos disponíveis para a turma
        from backend.turmas_backend import get_alunos_disponiveis
        alunos_disponiveis = get_alunos_disponiveis(turma['id'])
        
        # Se não houver alunos disponíveis, exibe mensagem e retorna
        if not alunos_disponiveis:
            ctk.CTkLabel(
                main_scroll,
                text="Não há alunos disponíveis",
                text_color="gray"
            ).pack(pady=20)
            return
        
        # Variável de controle para o RadioButton (email do aluno selecionado)
        selected_aluno = ctk.StringVar(value=alunos_disponiveis[0]['email'])
        
        # Cria RadioButton para cada aluno disponível
        for aluno in alunos_disponiveis:
            rb = ctk.CTkRadioButton(
                main_scroll,
                text=f"{aluno['nome']} - {aluno['email']}",
                variable=selected_aluno,
                value=aluno['email']
            )
            rb.pack(pady=5, padx=20, anchor="w")
        
        # Função de callback para adicionar o aluno
        def add_aluno():
            # Importa a função para adicionar o aluno
            from backend.turmas_backend import adicionar_aluno_turma
            # Executa a adição
            sucesso = adicionar_aluno_turma(turma['id'], selected_aluno.get())

            if sucesso:
                # Exibe sucesso, fecha diálogo e recarrega os detalhes da turma
                messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
                dialog.destroy()
                self.show_detalhes_turma(turma)
            else:
                # Exibe erro
                messagebox.showerror("Erro", "Erro ao adicionar aluno!")
        
        # Cria e empacota o botão "Adicionar"
        ctk.CTkButton(
            main_scroll,
            text="Adicionar",
            command=add_aluno,
            width=200,
            fg_color="#2CC985"
        ).pack(pady=20)

    # Função para exibir o menu principal do administrador
    def show_admin_menu(self):
        # Limpa a janela principal
        self.app.clear_window()
        
        # Cria um container rolável para o menu
        scroll_container = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Cria um frame principal dentro do container rolável
        main_frame = ctk.CTkFrame(scroll_container, corner_radius=0)
        main_frame.pack(padx=20, pady=20, fill="x")
        
        # Obtém dados do usuário logado (administrador)
        from backend.turmas_backend import get_user_data
        user_data = get_user_data(self.user_email)
        
        # Frame para o cabeçalho
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=20, pady=(20, 30))
        
        # Rótulo de título do painel
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"👨‍💼 Painel do Administrador",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Rótulo de boas-vindas e informações do usuário
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=f"Bem-vindo, {user_data['nome']} | {self.user_email}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack()
        
        # Frame para os botões do menu
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)
        
        # Lista de dados dos botões: (Texto, Comando, Cor)
        buttons_data = [
            ("👥 Gerenciar Usuários", self.show_gerenciar_usuarios, "#3498DB"),
            ("📚 Gerenciar Turmas", self.show_gerenciar_turmas, "#9B59B6"),
            ("➕ Criar Turmas", self.show_criar_turma, "#16A085"),
            ("📄 Relatórios de Aulas", self.show_relatorios_aulas_admin, "#D4AA2C"),
            ("📊 Relatórios Gerais", self.show_relatorios_gerais, "#2CC985"),
            ("📈 Estatísticas do Sistema", self.show_estatisticas, "#E67E22"),
            ("🗑️ Limpeza de Dados", self.show_limpeza_dados, "#E74C3C"),
            ("🚪 Sair", lambda: self.app.logout(), "#34495E") # Usa lambda para chamar o método logout
        ]
        
        # Cria e empacota os botões iterando sobre a lista
        for text, command, color in buttons_data:
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                font=ctk.CTkFont(size=16, weight="bold", ),
                width=450,
                height=55,
                command=command,
                fg_color=color,
                text_color="#dfdfdf",
                hover_color=self.darken_color(color)
            )
            btn.pack(pady=8)

    # Função para exibir a tela de gerenciamento de usuários
    def show_gerenciar_usuarios(self):
        # Inicializa variáveis de controle de filtro e pesquisa (se ainda não existirem)
        if not hasattr(self, 'filter_var'):
            self.filter_var = ctk.StringVar(value="TODOS")
        
        if not hasattr(self, 'search_var'):
            self.search_var = ctk.StringVar(value="")

        # Limpa a janela principal
        self.app.clear_window()
        
        # Cria um frame rolável principal
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Rótulo de título
        title_label = ctk.CTkLabel(
            main_frame,
            text="👥 Gerenciar Usuários",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 20))

        # Frame para controles de busca
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(pady=10, padx=40, fill="x")
        
        # Frame para a caixa de busca
        search_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        search_frame.pack(pady=(5, 10), padx=5, fill="x")
        
        # Campo de entrada para a busca
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por nome ou email...",
            width=500,
            textvariable=self.search_var
        )
        search_entry.pack(side="left", fill="x", expand=True)
        
        # Botão de busca
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            width=80,
            command=self.show_gerenciar_usuarios
        ).pack(side="left", padx=10)
        
        # Frame para os botões de filtro
        filter_frame = ctk.CTkFrame(main_frame)
        filter_frame.pack(pady=10, padx=40, fill="x")
        
        # Rótulo "Filtrar"
        ctk.CTkLabel(
            filter_frame, 
            text="Filtrar:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=15, pady=10)
        
        # Cria RadioButtons para as opções de filtro de função (role)
        for option in ["TODOS", "ADMIN", "INSTRUCTOR", "USER"]:
            rb = ctk.CTkRadioButton(
                filter_frame,
                text=option,
                variable=self.filter_var,
                value=option,
                command=lambda: self.show_gerenciar_usuarios() # Recarrega a tela ao mudar o filtro
            )
            rb.pack(side="left", padx=10)
        
        # Obtém a lista de usuários aplicando filtro e termo de busca
        from backend.turmas_backend import get_todos_usuarios
        search_term = self.search_var.get() if self.search_var.get() else None
        usuarios = get_todos_usuarios(self.filter_var.get(), search_term=search_term)
        
        # Frame para exibir estatísticas
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(pady=10, padx=40, fill="x")
        
        # Calcula e exibe estatísticas resumidas dos usuários
        total = len(usuarios)
        admins = len([u for u in usuarios if u['role'] == 'ADMIN'])
        professores = len([u for u in usuarios if u['role'] == 'INSTRUCTOR'])
        alunos = len([u for u in usuarios if u['role'] == 'USER'])
        
        ctk.CTkLabel(
            stats_frame,
            text=f"📊 Total: {total} | 👨‍💼 Admins: {admins} | 👨‍🏫 Profs: {professores} | 👨‍🎓 Alunos: {alunos}",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=12)
        
        # Exibe mensagem se não houver usuários
        if not usuarios:
            ctk.CTkLabel(
                main_frame, 
                text="Nenhum usuário encontrado.", 
                text_color="gray"
            ).pack(pady=30)
        else:
            # Itera sobre os usuários para exibir cada um
            for usuario in usuarios:
                # Frame para o item do usuário
                user_frame = ctk.CTkFrame(main_frame)
                user_frame.pack(pady=5, padx=40, fill="x")
                
                # Frame para as informações do usuário
                info_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
                
                # Define o ícone com base na função (role)
                icon = "👨‍💼" if usuario['role'] == 'ADMIN' else "👨‍🏫" if usuario['role'] == 'INSTRUCTOR' else "👨‍🎓"
                
                # Rótulo para o nome
                ctk.CTkLabel(
                    info_frame,
                    text=f"{icon} {usuario['nome']}",
                    font=ctk.CTkFont(size=15, weight="bold")
                ).pack(anchor="w")
                
                # Rótulo para o email
                ctk.CTkLabel(
                    info_frame,
                    text=f"{usuario['email']}",
                    font=ctk.CTkFont(size=11),
                    text_color="gray"
                ).pack(anchor="w")
                
                # Frame para os botões de ação (Visualizar, Editar, Excluir)
                btn_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
                btn_frame.pack(side="right", padx=8)
                
                # Botão "Visualizar Detalhes"
                ctk.CTkButton(
                    btn_frame,
                    text="👁️",
                    width=45,
                    height=32,
                    anchor="center",
                    command=lambda u=usuario: self.show_detalhes_usuario(u)
                ).pack(side="left", padx=2)
                
                # Botão "Editar Usuário"
                ctk.CTkButton(
                    btn_frame,
                    text="✏️",
                    width=45,
                    height=32,
                    anchor="center",
                    fg_color="#9B59B6",
                    hover_color="#7D3C98",
                    command=lambda u=usuario: self.show_editar_usuario(u)
                ).pack(side="left", padx=2)
                
                # Botão "Excluir Usuário"
                if usuario['email'] != self.user_email:
                    ctk.CTkButton(
                        btn_frame,
                        text="🗑️",
                        width=45,
                        height=32,
                        anchor="center",
                        fg_color="#E74C3C",
                        hover_color="#C0392B",
                        command=lambda u=usuario: self.confirmar_excluir_usuario(u)
                    ).pack(side="left", padx=2)
        
        # Frame para botões de ação na parte inferior
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(pady=20)
        
        # Botão "Adicionar Usuário"
        ctk.CTkButton(
            action_frame,
            text="➕ Adicionar Usuário",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=200,
            height=45,
            command=self.show_adicionar_usuario,
            fg_color="#2CC985",
            hover_color="#25A066"
        ).pack(side="left", padx=5)
        
        # Botão "Voltar"
        ctk.CTkButton(
            action_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=15),
            width=150,
            height=45,
            command=self.show_admin_menu,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(side="left", padx=5)

    # Função para exibir os detalhes completos de um usuário em um diálogo
    def show_detalhes_usuario(self, usuario):
        # Cria e configura a janela de diálogo
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Detalhes do Usuário")
        dialog.geometry("700x500")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)

        # Cria o frame principal
        main = ctk.CTkFrame(dialog, corner_radius=0)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Rótulo de título com o nome do usuário
        title = ctk.CTkLabel(
            main,
            text=f"👤 {usuario['nome']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Frame para as informações detalhadas
        info_frame = ctk.CTkFrame(main)
        info_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Importa a função para obter detalhes adicionais do usuário (ex: turmas, atividades)
        from backend.turmas_backend import get_detalhes_completos_usuario
        detalhes = get_detalhes_completos_usuario(usuario['email'])
        
        # Mapeamento de 'role' (função) para texto em português
        role_map = {
            'ADMIN': 'Administrador',
            'INSTRUCTOR': 'Professor',
            'USER': 'Aluno'
        }
        
        # Lista de dados básicos a serem exibidos
        dados = [
            ("📧 Email:", usuario['email']),

            ("👤 Tipo:", role_map.get(usuario['role'], usuario['role'])),
        ]
        
        # Adiciona detalhes específicos se o usuário for um INSTRUTOR
        if usuario['role'] == 'INSTRUCTOR':
            dados.extend([
                ("📚 Turmas:", str(detalhes.get('total_turmas', 0))),
                ("👥 Total Alunos:", str(detalhes.get('total_alunos', 0))),
                ("📝 Atividades:", str(detalhes.get('total_atividades', 0))),
            ])
        # Adiciona detalhes específicos se o usuário for um ALUNO
        elif usuario['role'] == 'USER':
            # Formata a média geral com duas casas decimais
            media_formatada = f"{detalhes.get('media_geral', 0):.2f}"
            dados.extend([
                ("📚 Matriculado em:", f"{detalhes.get('total_turmas', 0)} turma(s)"),
                ("📅 dia da matricula:", detalhes.get('data_matricula', 'N/A')),
                ("✅ Entregas:", str(detalhes.get('atividades_entregues', 0))),
                ("📊 Média:", media_formatada),
            ])
        
        # Itera sobre a lista de dados para exibir rótulos e valores
        for label, valor in dados:
            # Frame para a linha de rótulo-valor
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(pady=6, padx=15, fill="x")
            
            # Rótulo do campo
            ctk.CTkLabel(
                row_frame,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                width=150,
                anchor="w"
            ).pack(side="left")
            
            # Rótulo do valor
            ctk.CTkLabel(
                row_frame,
                text=valor,
                font=ctk.CTkFont(size=14),
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
        
        # Botão "Fechar" para destruir o diálogo
        ctk.CTkButton(
            dialog,
            text="Fechar",
            command=dialog.destroy,
            width=150,
            height=40,
            fg_color="gray"
        ).pack(pady=20)
    
    # A função abre uma nova janela para editar os dados de um usuário existente.
    def show_editar_usuario(self, usuario):
        # Cria uma nova janela de nível superior (dialog) vinculada à aplicação principal (self.app)
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Editar Usuário")
        dialog.geometry("700x500")
        # Define o foco da aplicação para esta janela (modal), bloqueando interações com outras janelas
        dialog.grab_set()
        # Impede o redimensionamento da janela
        dialog.resizable(height=False, width=False)

        # Cria um frame com barra de rolagem para acomodar o conteúdo
        main_scroll = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título da janela de edição
        title = ctk.CTkLabel(
            main_scroll, 
            text=f"✏️ Editar: {usuario['nome']}", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Frame para agrupar os campos do formulário
        form_frame = ctk.CTkFrame(main_scroll)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Rótulo para o campo Nome
        ctk.CTkLabel(
            form_frame, 
            text="Nome:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 3))
        
        # Campo de entrada para o Nome, preenchido com o nome atual do usuário
        nome_entry = ctk.CTkEntry(form_frame, width=450, height=38)
        nome_entry.insert(0, usuario['nome'])
        nome_entry.pack(padx=15, pady=(0, 10))
        
        # Rótulo para o campo Tipo (Role)
        ctk.CTkLabel(
            form_frame, 
            text="Tipo:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 3))
        
        # Variável de controle para os RadioButtons (define o tipo/role atual do usuário)
        role_var = ctk.StringVar(value=usuario['role'])
        # Frame para agrupar os RadioButtons (Tipo)
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Lista de opções de Tipo (Role)
        roles = [("👨‍💼 Admin", "ADMIN"), ("👨‍🏫 Prof", "INSTRUCTOR"), ("👨‍🎓 Aluno", "USER")]
        # Cria e posiciona os RadioButtons
        for text, value in roles:
            rb = ctk.CTkRadioButton(role_frame, text=text, variable=role_var, value=value)
            rb.pack(side="left", padx=8)
        
        # Rótulo para o campo Nova Senha
        ctk.CTkLabel(
            form_frame, 
            text="Nova Senha (deixe vazio para não alterar):", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 3))

        # Campo de entrada para a Nova Senha (mostra asteriscos ao digitar)
        nova_senha_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Nova Senha", 
            width=450, 
            height=38, 
            show="*"
        )
        nova_senha_entry.pack(padx=15, pady=(0, 10))

        # Rótulo para o campo Repetir Senha
        ctk.CTkLabel(
            form_frame, 
            text="Repetir Senha:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 3))

        # Campo de entrada para Repetir Senha
        repetir_senha_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Repita a Nova Senha", 
            width=450, 
            height=38, 
            show="*"
        )
        repetir_senha_entry.pack(padx=15, pady=(0, 10))
        
        
        # Função interna chamada ao clicar em "Salvar"
        def salvar_edicao():
            # Obtém e formata os novos valores dos campos
            novo_nome = nome_entry.get().strip().title()
            novo_role = role_var.get()
            nova_senha = nova_senha_entry.get().strip()
            repetir_senha = repetir_senha_entry.get().strip()
            senha_criptografada = None

            # 1. Validação de senhas: verifica se as senhas coincidem
            if nova_senha != repetir_senha:
                messagebox.showerror("Erro de Senha", "As novas senhas não coincidem!")
                return
            
            # 2. Validação de senhas: se houver nova senha, verifica o comprimento mínimo (6 caracteres)
            if nova_senha != "":
                if len(nova_senha) < 6:
                    messagebox.showerror("Erro de Senha", "A nova senha deve ter pelo menos 6 caracteres.")
                    return
                
                # Criptografa a nova senha (importa a função de infraestrutura)
                from infra import security as infra
                senha_criptografada = infra.criptografar_senha(nova_senha)
            
            # 3. Validação de Nome: verifica se o nome foi preenchido
            if not novo_nome:
                messagebox.showerror("Erro", "O campo nome é obrigatório!")
                return
            
            # Chama a função para realizar a edição no banco de dados
            from backend.turmas_backend import editar_usuario
            sucesso = editar_usuario(usuario['email'], novo_nome, novo_role, senha_criptografada)
            
            # Trata o resultado da operação
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário editado!")

                # Recarrega a lista de usuários após a edição
                from database import banco
                banco.carregar_usuarios()

                # Fecha a janela de edição e recarrega a tela de gerenciamento
                dialog.destroy()
                self.show_gerenciar_usuarios()
            else:
                messagebox.showerror("Erro", "Erro ao editar!")
        
        # Frame para agrupar os botões Salvar e Cancelar
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        # Botão Salvar Edição
        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar",
            command=salvar_edicao, # Chama a função de salvar
            width=160,
            height=42,
            fg_color="#2CC985"
        ).pack(side="left", padx=5)
        
        # Botão Cancelar (fecha a janela)
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=dialog.destroy,
            width=160,
            height=42,
            fg_color="gray"
        ).pack(side="left", padx=5)
    
    # Função que exibe a caixa de diálogo de confirmação para exclusão de usuário
    def confirmar_excluir_usuario(self, usuario):
        # Abre a caixa de diálogo de confirmação (Sim/Não)
        result = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Excluir usuário?\n\n{usuario['nome']}\n{usuario['email']}\n\n⚠️ IRREVERSÍVEL!",
            icon='warning'
        )
        
        # Se o usuário confirmar a exclusão
        if result:
            # Chama a função para excluir o usuário
            from backend.turmas_backend import excluir_usuario
            sucesso = excluir_usuario(usuario['email'])
            
            # Trata o resultado
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário excluído!")
                # Recarrega a tela de gerenciamento após a exclusão
                self.show_gerenciar_usuarios()
            else:
                messagebox.showerror("Erro", "Erro ao excluir!")
    
    # A função abre uma nova janela para cadastrar um novo usuário.
    def show_adicionar_usuario(self):
        # Cria a nova janela de nível superior
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Adicionar Usuário")
        dialog.geometry("550x600")
        dialog.grab_set() # Torna a janela modal
        
        # Frame com barra de rolagem
        main_scroll = ctk.CTkScrollableFrame(dialog, width=500, height=530)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título da janela
        title = ctk.CTkLabel(
            main_scroll, 
            text="➕ Novo Usuário", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Frame para agrupar os campos do formulário
        form_frame = ctk.CTkFrame(main_scroll)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Rótulo e Campo de entrada para Nome
        ctk.CTkLabel(
            form_frame, 
            text="Nome:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 3))

        nome_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Nome completo", 
            width=450, 
            height=38
        )
        nome_entry.pack(padx=15, pady=(0, 10))
        
        # Rótulo e Campo de entrada para Email
        ctk.CTkLabel(
            form_frame, 
            text="Email:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 3))

        email_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="email@exemplo.com", 
            width=450, 
            height=38
        )
        email_entry.pack(padx=15, pady=(0, 10))
        
        # Rótulo e Campo de entrada para Senha
        ctk.CTkLabel(
            form_frame, 
            text="Senha:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 3))

        senha_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Senha", 
            width=450, 
            height=38, 
            show="*"
        )
        senha_entry.pack(padx=15, pady=(0, 10))
        
        # Rótulo para o campo Tipo (Role)
        ctk.CTkLabel(
            form_frame, 
            text="Tipo:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 3))
        
        # Variável de controle e Frame para os RadioButtons (Tipo)
        role_var = ctk.StringVar(value="USER") # Padrão é 'USER' (Aluno)
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Opções de Tipo (Role) e criação dos RadioButtons
        roles = [("👨‍💼 Admin", "ADMIN"), ("👨‍🏫 Prof", "INSTRUCTOR"), ("👨‍🎓 Aluno", "USER")]
        for text, value in roles:
            rb = ctk.CTkRadioButton(role_frame, text=text, variable=role_var, value=value)
            rb.pack(side="left", padx=8)
        
        # Função interna chamada ao clicar em "Adicionar"
        def adicionar():
            # Obtém os valores dos campos
            nome = nome_entry.get().strip()
            email = email_entry.get().strip()
            senha = senha_entry.get()
            role = role_var.get()
            
            # Validação: verifica se todos os campos obrigatórios foram preenchidos
            if not all([nome, email, senha]):
                messagebox.showerror("Erro", "Todos os campos obrigatórios!")
                return
            
            # Chama a função para adicionar o novo usuário
            from backend.turmas_backend import adicionar_usuario
            sucesso = adicionar_usuario(nome, email, senha, role)
            
            # Trata o resultado
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário adicionado!")
                # Fecha a janela e recarrega a tela de gerenciamento
                dialog.destroy()
                self.show_gerenciar_usuarios()
            else:
                messagebox.showerror("Erro", "Email já existe!") # Email é único
        
        # Frame para agrupar os botões Adicionar e Cancelar
        btn_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        # Botão Adicionar
        ctk.CTkButton(
            btn_frame,
            text="➕ Adicionar",
            command=adicionar, # Chama a função de adicionar
            width=160,
            height=42,
            fg_color="#2CC985"
        ).pack(side="left", padx=5)
        
        # Botão Cancelar (fecha a janela)
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=dialog.destroy,
            width=160,
            height=42,
            fg_color="gray"
        ).pack(side="left", padx=5)
    
    # A função exibe a tela de gerenciamento de turmas para o administrador.
    def show_gerenciar_turmas(self):
        self.app.clear_window() # Limpa o conteúdo da janela principal
        
        # Cria o frame principal com rolagem
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título da tela
        title_label = ctk.CTkLabel(
            main_frame,
            text="📚 Gerenciar Turmas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 20))
        
        # Busca todas as turmas no backend
        from backend.turmas_backend import get_todas_turmas
        turmas = get_todas_turmas()
        
        # Frame para exibir as estatísticas gerais
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(pady=10, padx=40, fill="x")
        
        # Calcula estatísticas
        total_turmas = len(turmas)
        total_alunos = sum([t['total_alunos'] for t in turmas])
        
        # Exibe as estatísticas
        ctk.CTkLabel(
            stats_frame,
            text=f"📊 {total_turmas} turma(s) | {total_alunos} aluno(s) matriculado(s)",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=12)
        
        # Se não houver turmas cadastradas, exibe uma mensagem
        if not turmas:
            ctk.CTkLabel(
                main_frame, 
                text="Nenhuma turma cadastrada.", 
                text_color="gray"
            ).pack(pady=30)
        # Se houver turmas, itera sobre elas e cria um item para cada
        else:
            for turma in turmas:
                # Frame individual para cada turma
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=5, padx=40, fill="x")
                
                # Frame para as informações de texto da turma
                info_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
                
                # Nome da turma
                ctk.CTkLabel(
                    info_frame,
                    text=f"📖 {turma['nome']}",
                    font=ctk.CTkFont(size=15, weight="bold")
                ).pack(anchor="w")
                
                # Detalhes da turma (disciplina, professor, alunos)
                ctk.CTkLabel(
                    info_frame,
                    text=f"{turma['disciplina']} | {turma['professor_nome']} | {turma['total_alunos']} alunos",
                    font=ctk.CTkFont(size=11),
                    text_color="gray"
                ).pack(anchor="w")
                
                # Frame para os botões de ação (Visualizar, Editar, Excluir)
                btn_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                btn_frame.pack(side="right", padx=8)
                
                # Botão Visualizar (chama show_detalhes_turma_admin)
                ctk.CTkButton(
                    btn_frame,
                    text="👁️",
                    width=45,
                    height=32,
                    command=lambda t=turma: self.show_detalhes_turma_admin(t)
                ).pack(side="left", padx=2)
                
                # Botão Editar (chama show_editar_turma)
                ctk.CTkButton(
                    btn_frame,
                    text="✏",
                    width=45,
                    height=32,
                    fg_color="#9B59B6",
                    hover_color="#7D3C98",
                    command=lambda t=turma: self.show_editar_turma(t)
                ).pack(side="left", padx=2)
                
                # Botão Excluir (chama confirmar_excluir_turma)
                ctk.CTkButton(
                    btn_frame,
                    text="🗑️",
                    width=45,
                    height=32,
                    fg_color="#E74C3C",
                    hover_color="#C0392B",
                    command=lambda t=turma: self.confirmar_excluir_turma(t)
                ).pack(side="left", padx=2)
        
        # Botão Voltar para o menu Admin
        ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=15),
            width=150,
            height=45,
            command=self.show_admin_menu,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(pady=20)
    
    # A função exibe os detalhes completos de uma turma em uma nova janela.
    def show_detalhes_turma_admin(self, turma):
        # Cria a nova janela de nível superior
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Detalhes da Turma")
        dialog.geometry("700x600")
        dialog.grab_set() # Torna a janela modal
        dialog.resizable(height=False, width=False)

        # Frame principal com barra de rolagem
        main_scroll = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título da turma
        title = ctk.CTkLabel(
            main_scroll, 
            text=f"📖 {turma['nome']}", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Busca detalhes adicionais da turma no backend
        from backend.turmas_backend import get_detalhes_completos_turma
        detalhes = get_detalhes_completos_turma(turma['id'])
        
        # Frame para exibir os dados principais
        info_frame = ctk.CTkFrame(main_scroll)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        # Lista de dados a serem exibidos (mesclando dados da turma e detalhes)
        dados = [
            ("📚 Disciplina:", turma['disciplina']),
            ("👨‍🏫 Professor:", turma['professor_nome']),
            ("📅 Ano:", turma['ano']),
            ("🕐 Período:", turma['periodo']),
            ("👥 Alunos:", str(turma['total_alunos'])),
            ("📝 Aulas:", str(detalhes.get('total_aulas', 0))),
            ("📋 Atividades:", str(detalhes.get('total_atividades', 0))),
        ]
        
        # Cria e posiciona rótulos para cada dado
        for label, valor in dados:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(pady=6, padx=15, fill="x")
            
            # Rótulo (Nome do campo)
            ctk.CTkLabel(
                row_frame, 
                text=label, 
                font=ctk.CTkFont(size=13, weight="bold"), 
                width=140, 
                anchor="w"
            ).pack(side="left")
            
            # Rótulo (Valor do campo)
            ctk.CTkLabel(
                row_frame, 
                text=valor, 
                font=ctk.CTkFont(size=13), 
                anchor="w"
            ).pack(side="left")
        
        # Se houver descrição, exibe o campo de descrição
        if detalhes.get('descricao'):
            ctk.CTkLabel(
                main_scroll, 
                text="📄 Descrição:", 
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(anchor="w", padx=35, pady=(15, 5))

        # Campo de texto (Textbox) para a Descrição (somente leitura)
        desc_text = ctk.CTkTextbox(
            main_scroll,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="gray",
            wrap="word", # Quebra de linha por palavra
            width=500,
        )
        desc_text.pack(anchor="w", pady=(15, 5),fill="x", expand=True)
        desc_text.insert("1.0", detalhes['descricao'])
        desc_text.configure(state="disabled") # Define como somente leitura
        
        # Botão Fechar
        ctk.CTkButton(
            dialog, 
            text="Fechar", 
            command=dialog.destroy, 
            width=150,
            height=40,
            fg_color="gray"
        ).pack(pady=15)
    
    # Função que exibe a caixa de diálogo de confirmação para exclusão de turma
    def confirmar_excluir_turma(self, turma):
        # Abre a caixa de diálogo de confirmação, com alerta de perda de dados
        result = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Excluir turma?\n\n{turma['nome']}\n{turma['disciplina']}\n\n⚠️ TODOS os dados (aulas, atividades, notas) serão perdidos!\n\nIRREVERSÍVEL!",
            icon='warning'
        )
        
        # Se o usuário confirmar a exclusão
        if result:
            # Chama a função de backend para excluir a turma
            from backend.turmas_backend import excluir_turma
            sucesso = excluir_turma(turma['id'])
            
            # Trata o resultado
            if sucesso:
                messagebox.showinfo("Sucesso", "Turma excluída!")
                # Recarrega a tela de gerenciamento
                self.show_gerenciar_turmas()
            else:
                messagebox.showerror("Erro", "Erro ao excluir!")
    
    # A função exibe uma tela com estatísticas gerais do sistema.
    def show_relatorios_gerais(self):
        self.app.clear_window() # Limpa o conteúdo da janela principal
        
        # Cria o frame principal com rolagem
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título da tela
        title_label = ctk.CTkLabel(
            main_frame,
            text="📊 Relatórios do Sistema",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 25))
        
        # Busca os dados do relatório geral no backend
        from backend.turmas_backend import get_relatorio_geral
        relatorio = get_relatorio_geral()
        
        # Estrutura os dados do relatório em seções e itens
        sections = [
            ("👥 Usuários", [
                ("Total:", str(relatorio['total_usuarios'])),
                ("Admins:", str(relatorio['total_admins'])),
                ("Professores:", str(relatorio['total_professores'])),
                ("Alunos:", str(relatorio['total_alunos'])),
            ]),
            ("📚 Turmas", [
                ("Total:", str(relatorio['total_turmas'])),
                ("Matrículas:", str(relatorio['total_matriculas'])),
                ("Média alunos/turma:", f"{relatorio['media_alunos_turma']:.1f}"),
            ]),
            ("📝 Atividades", [
                ("Criadas:", str(relatorio['total_atividades'])),
                ("Entregues:", str(relatorio['total_entregas'])),
                ("Taxa entrega:", f"{relatorio['taxa_entrega']:.1f}%"),
                ("Corrigidas:", str(relatorio['total_corrigidas'])),
            ]),
            ("📊 Desempenho", [
                ("Média geral:", f"{relatorio['media_geral_sistema']:.2f}"),
                ("Taxa aprovação:", f"{relatorio['taxa_aprovacao']:.1f}%"),
            ]),
        ]
        
        # Itera sobre as seções e seus itens para exibição
        for section_title, items in sections:
            # Frame para a seção
            section_frame = ctk.CTkFrame(main_frame)
            section_frame.pack(pady=8, padx=40, fill="x")
            
            # Título da seção
            ctk.CTkLabel(
                section_frame,
                text=section_title,
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", padx=15, pady=(12, 8))
            
            # Itera sobre os itens da seção
            for label, valor in items:
                row_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
                row_frame.pack(pady=4, padx=30, fill="x")
                
                # Rótulo (Nome do dado)
                ctk.CTkLabel(
                    row_frame,
                    text=label,
                    font=ctk.CTkFont(size=13),
                    width=180,
                    anchor="w"
                ).pack(side="left")
                
                # Rótulo (Valor do dado)
                ctk.CTkLabel(
                    row_frame,
                    text=valor,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    anchor="w"
                ).pack(side="left")
            
            # Espaçador entre as seções
            ctk.CTkLabel(section_frame, text="").pack(pady=6)
        
        # Frame para os botões de ação
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        # Botão Exportar Relatório (chama a função de exportação)
        ctk.CTkButton(
            btn_frame,
            text="📄 Exportar",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=150,
            height=45,
            command=lambda: self.exportar_relatorio(relatorio), # Passa os dados do relatório para a função
            fg_color="#2CC985"
        ).pack(side="left", padx=5)
        
        # Botão Voltar para o menu Admin
        ctk.CTkButton(
            btn_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=15),
            width=150,
            height=45,
            command=self.show_admin_menu,
            fg_color="gray"
        ).pack(side="left", padx=5)
    
    def exportar_relatorio(self, relatorio):
    # Abre uma caixa de diálogo 'Salvar Como' para o usuário escolher o local e nome do arquivo.
    # Define a extensão padrão como '.txt', filtros para arquivos de texto e todos os arquivos.
    # Sugere um nome de arquivo baseado na data e hora atuais.
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")],
            initialfile=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        # Verifica se o usuário selecionou um caminho de salvamento (não cancelou a caixa de diálogo).
        if save_path:
            # Importa a função de exportação do backend.
            from backend.turmas_backend import exportar_relatorio_txt
            
            # Chama a função do backend para salvar o relatório no caminho especificado.
            sucesso = exportar_relatorio_txt(relatorio, save_path)
            
            # Exibe uma caixa de mensagem de sucesso ou erro, dependendo do resultado da exportação.
            if sucesso:
                messagebox.showinfo("Sucesso", "Relatório exportado!")
            else:
                messagebox.showerror("Erro", "Erro ao exportar!")
    
    def show_estatisticas(self):
        # Limpa a janela principal do aplicativo para exibir o novo conteúdo.
        self.app.clear_window()
        
        # Cria um frame rolável para conter o conteúdo das estatísticas.
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Rótulo de título para a seção de estatísticas.
        title_label = ctk.CTkLabel(
            main_frame,
            text="📈 Estatísticas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 25))
        
        # Importa e chama a função do backend para obter todos os dados estatísticos.
        from backend.turmas_backend import get_estatisticas_detalhadas
        stats = get_estatisticas_detalhadas()
        
        # --- Seção Top 5 Alunos ---
        ctk.CTkLabel(
            main_frame,
            text="🏆 Top 5 Alunos",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))
        
        # Cria um frame para listar os alunos.
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.pack(pady=8, padx=40, fill="x")
        
        # Verifica se há dados de top alunos.
        if stats['top_alunos']:
            # Itera sobre a lista de top alunos (enumerate para obter a posição).
            for i, aluno in enumerate(stats['top_alunos'], 1):
                # Define o emoji da medalha com base na posição.
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🎖️"
                
                # Exibe o nome e a média do aluno.
                ctk.CTkLabel(
                    top_frame,
                    text=f"{medal} {i}º - {aluno['nome']} | {aluno['media']:.2f}",
                    font=ctk.CTkFont(size=13),
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=4)
        else:
            # Mensagem se não houver dados de alunos.
            ctk.CTkLabel(
                top_frame,
                text="Nenhum dado disponível",
                text_color="gray"
            ).pack(pady=10)
        
        # --- Seção Professores Ativos ---
        ctk.CTkLabel(
            main_frame,
            text="👨‍🏫 Professores Ativos",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))
        
        # Cria um frame para listar os professores.
        prof_frame = ctk.CTkFrame(main_frame)
        prof_frame.pack(pady=8, padx=40, fill="x")
        
        # Verifica se há dados de professores ativos.
        if stats['professores_ativos']:
            # Itera sobre a lista de professores ativos.
            for prof in stats['professores_ativos']:
                # Exibe o nome, número de turmas e atividades do professor.
                ctk.CTkLabel(
                    prof_frame,
                    text=f"👨‍🏫 {prof['nome']} | {prof['turmas']} turma(s) | {prof['atividades']} atividade(s)",
                    font=ctk.CTkFont(size=13),
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=4)
        else:
            # Mensagem se não houver dados de professores.
            ctk.CTkLabel(
                prof_frame,
                text="Nenhum dado disponível",
                text_color="gray"
            ).pack(pady=10)
        
        # --- Seção Melhores Turmas ---
        ctk.CTkLabel(
            main_frame,
            text="📚 Melhores Turmas",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))
        
        # Cria um frame para listar as turmas.
        turmas_frame = ctk.CTkFrame(main_frame)
        turmas_frame.pack(pady=8, padx=40, fill="x")
        
        # Verifica se há dados de melhores turmas.
        if stats['melhores_turmas']:
            # Itera sobre a lista de melhores turmas.
            for turma in stats['melhores_turmas']:
                # Exibe o nome, média da turma e taxa de aprovação.
                ctk.CTkLabel(
                    turmas_frame,
                    text=f"📖 {turma['nome']} | Média: {turma['media']:.2f} | Aprovação: {turma['taxa_aprovacao']:.1f}%",
                    font=ctk.CTkFont(size=13),
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=4)
        else:
            # Mensagem se não houver dados de turmas.
            ctk.CTkLabel(
                turmas_frame,
                text="Nenhum dado disponível",
                text_color="gray"
            ).pack(pady=10)
        
        # Botão para voltar ao menu do administrador.
        ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=15),
            width=150,
            height=45,
            command=self.show_admin_menu,
            fg_color="gray"
        ).pack(pady=25)
    
    def show_limpeza_dados(self):
        # Limpa a janela principal para a seção de limpeza de dados.
        self.app.clear_window()
        
        # Cria um frame rolável para o conteúdo.
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Rótulo de título.
        title_label = ctk.CTkLabel(
            main_frame,
            text="🗑️ Limpeza de Dados",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 15))
        
        # Rótulo de aviso para as operações irreversíveis.
        warning_label = ctk.CTkLabel(
            main_frame,
            text="⚠️ ATENÇÃO: OPERAÇÕES IRREVERSÍVEIS! ⚠️",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#E74C3C" # Cor de aviso/perigo
        )
        warning_label.pack(pady=(10, 25))
        
        # Lista de operações de limpeza de dados: (Título, Descrição, Comando/Função).
        operations = [
            ("Limpar Turmas Antigas", "Excluir turmas de anos anteriores", lambda: self.limpar_turmas_antigas()),
            ("Remover Atividades Antigas", "Excluir atividades com +1 ano", lambda: self.limpar_atividades_antigas()),
            ("Arquivar Inativos", "Remover usuários inativos (+1 ano)", lambda: self.arquivar_inativos()),
        ]
        
        # Itera sobre a lista de operações para criar a interface.
        for titulo, descricao, comando in operations:
            op_frame = ctk.CTkFrame(main_frame)
            op_frame.pack(pady=8, padx=40, fill="x")
            
            # Frame para as informações (título e descrição).
            info_frame = ctk.CTkFrame(op_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=12)
            
            # Rótulo do título da operação.
            ctk.CTkLabel(
                info_frame,
                text=titulo,
                font=ctk.CTkFont(size=15, weight="bold")
            ).pack(anchor="w")
            
            # Rótulo da descrição da operação.
            ctk.CTkLabel(
                info_frame,
                text=descricao,
                font=ctk.CTkFont(size=11),
                text_color="gray"
            ).pack(anchor="w", pady=(2, 0))
            
            # Botão para executar a operação.
            ctk.CTkButton(
                op_frame,
                text="Executar",
                width=100,
                height=36,
                command=comando, # O comando a ser executado
                fg_color="#E74C3C",
                hover_color="#C0392B"
            ).pack(side="right", padx=15, pady=12)
        
        # Botão para voltar ao menu do administrador.
        ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=15),
            width=150,
            height=45,
            command=self.show_admin_menu,
            fg_color="gray"
        ).pack(pady=25)
    
    def limpar_turmas_antigas(self):
        # Pede confirmação do usuário com um aviso de irreversibilidade.
        result = messagebox.askyesno(
            "Confirmar",
            "Excluir turmas de anos anteriores?\n\n⚠️ IRREVERSÍVEL!",
            icon='warning'
        )
        
        # Se o usuário confirmar.
        if result:
            # Importa e chama a função de limpeza do backend.
            from backend.turmas_backend import limpar_turmas_antigas
            total = limpar_turmas_antigas()
            # Informa o total de turmas removidas.
            messagebox.showinfo("Concluído", f"{total} turma(s) removida(s).")
    
    def limpar_atividades_antigas(self):
        # Pede confirmação para exclusão de atividades antigas.
        result = messagebox.askyesno(
            "Confirmar",
            "Excluir atividades com +1 ano?\n\n⚠️ IRREVERSÍVEL!",
            icon='warning'
        )
        
        # Se o usuário confirmar.
        if result:
            # Importa e chama a função de limpeza do backend.
            from backend.turmas_backend import limpar_atividades_antigas
            total = limpar_atividades_antigas()
            # Informa o total de atividades removidas.
            messagebox.showinfo("Concluído", f"{total} atividade(s) removida(s).")
    
    def arquivar_inativos(self):
        # Pede confirmação para arquivar usuários inativos.
        result = messagebox.askyesno(
            "Confirmar",
            "Arquivar inativos (+1 ano)?\n\n⚠️ IRREVERSÍVEL!",
            icon='warning'
        )
        
        # Se o usuário confirmar.
        if result:
            # Importa e chama a função de arquivamento do backend.
            from backend.turmas_backend import arquivar_usuarios_inativos
            total = arquivar_usuarios_inativos()
            # Informa o total de usuários arquivados.
            messagebox.showinfo("Concluído", f"{total} usuário(s) arquivado(s).")
    
    def show_relatorios_aulas_admin(self):
        # Limpa a janela principal para a seção de relatórios de aulas.
        self.app.clear_window()
        
        # Cria um frame rolável para o conteúdo.
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Rótulo de título.
        title_label = ctk.CTkLabel(
            main_frame,
            text="📄 Relatórios de Aulas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Subtítulo explicativo.
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Visualize todos os relatórios de aulas registrados pelos professores",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Importa e chama a função para obter todos os relatórios.
        from backend.turmas_backend import get_todos_relatorios
        relatorios = get_todos_relatorios()
        
        # Verifica se há relatórios.
        if not relatorios:
            # Exibe mensagem se não houver relatórios.
            empty_label = ctk.CTkLabel(
                main_frame,
                text="Nenhum relatório registrado no sistema ainda.",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            # Cria um frame para os filtros.
            filter_frame = ctk.CTkFrame(main_frame)
            filter_frame.pack(pady=10, padx=40, fill="x")
            
            # Rótulo do filtro.
            ctk.CTkLabel(
                filter_frame,
                text="Filtrar por status:",
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(side="left", padx=(20, 10))
            
            # Variável para armazenar o valor do filtro selecionado.
            filter_var = ctk.StringVar(value="TODOS")
            
            def atualizar_listagem():
                # Função para atualizar a lista de relatórios com base no filtro.
                
                # Destrói todos os widgets da listagem anterior.
                for widget in content_frame.winfo_children():
                    widget.destroy()
                
                filtro = filter_var.get()
                relatorios_filtrados = relatorios
                
                # Filtra os relatórios de acordo com a opção selecionada.
                if filtro == "FINALIZADOS":
                    relatorios_filtrados = [r for r in relatorios if r.get('finalizado', False)]
                elif filtro == "RASCUNHOS":
                    relatorios_filtrados = [r for r in relatorios if not r.get('finalizado', False)]
                
                def safe_date_sort(relatorio):
                    # Função auxiliar para ordenação segura por data.
                    try:
                        return datetime.strptime(relatorio.get('data_criacao', '01/01/2000 00:00'), "%d/%m/%Y %H:%M")
                    except (ValueError, TypeError):
                        return datetime(2000, 1, 1) # Retorna uma data antiga se houver erro de formatação.
                
                # Ordena os relatórios filtrados pela data de criação (mais recente primeiro).
                relatorios_filtrados.sort(key=safe_date_sort, reverse=True)
                
                # Exibe mensagem se não houver relatórios após a filtragem.
                if not relatorios_filtrados:
                    empty = ctk.CTkLabel(
                        content_frame,
                        text="Nenhum relatório encontrado com este filtro.",
                        font=ctk.CTkFont(size=14),
                        text_color="gray"
                    )
                    empty.pack(pady=30)
                else:
                    # Itera sobre os relatórios filtrados para criar os itens da lista.
                    for relatorio in relatorios_filtrados:
                        rel_frame = ctk.CTkFrame(content_frame)
                        rel_frame.pack(pady=8, padx=20, fill="x")
                        
                        # Frame para as informações do relatório.
                        info_frame = ctk.CTkFrame(rel_frame, fg_color="transparent")
                        info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=12)
                        
                        # Frame para o cabeçalho (Status e Título).
                        header_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                        header_frame.pack(anchor="w", fill="x")
                        
                        # Crachá de status (Finalizado ou Rascunho).
                        if relatorio.get('finalizado', False):
                            status_badge = ctk.CTkLabel(
                                header_frame,
                                text="✓",
                                font=ctk.CTkFont(size=12, weight="bold"),
                                text_color="#2CC985", # Verde para finalizado
                                width=20
                            )
                            status_badge.pack(side="left")
                        else:
                            status_badge = ctk.CTkLabel(
                                header_frame,
                                text="⚠",
                                font=ctk.CTkFont(size=12, weight="bold"),
                                text_color="#F39C12", # Amarelo/Laranja para rascunho
                                width=20
                            )
                            status_badge.pack(side="left")
                        
                        # Rótulo do título da aula.
                        titulo_label = ctk.CTkLabel(
                            header_frame,
                            text=f"{relatorio.get('aula_titulo', 'N/A')}",
                            font=ctk.CTkFont(size=14, weight="bold"),
                            wraplength=400
                        )
                        titulo_label.pack(side="left", padx=5)
                        
                        # Informações sobre Professor, Turma e Disciplina.
                        info_text = (
                            f"Professor: {relatorio.get('professor_nome', 'N/A')} | "
                            f"Turma: {relatorio.get('turma_nome', 'N/A')} | "
                            f"Disciplina: {relatorio.get('disciplina', 'N/A')}"
                        )
                        info_label = ctk.CTkLabel(
                            info_frame,
                            text=info_text,
                            font=ctk.CTkFont(size=11),
                            text_color="gray",
                            wraplength=300

                        )
                        info_label.pack(anchor="w", pady=(3, 0))
                        
                        # Informações de data (Aula, Criação, Finalização).
                        data_info = f"Aula: {relatorio.get('aula_data', 'N/A')} | Criado: {relatorio.get('data_criacao', 'N/A')}"
                        if relatorio.get('finalizado', False):
                            data_info += f" | Finalizado: {relatorio.get('data_finalizacao', 'N/A')}"
                        
                        data_label = ctk.CTkLabel(
                            info_frame,
                            text=data_info,
                            font=ctk.CTkFont(size=10),
                            text_color="gray"
                        )
                        data_label.pack(anchor="w", pady=(2, 0))
                        
                        # Botão para visualizar detalhes do relatório.
                        view_btn = ctk.CTkButton(
                            rel_frame,
                            text="👁 Ver",
                            width=100,
                            height=35,
                            fg_color="#16A085",
                            hover_color="#138D75",
                            # Chama a função passando o relatório.
                            command=lambda r=relatorio: self.show_visualizar_relatorio_admin(r)
                        )
                        view_btn.pack(side="right", padx=10, pady=10)
            
            # Cria os botões de rádio para as opções de filtro.
            for opcao in ["TODOS", "FINALIZADOS", "RASCUNHOS"]:
                ctk.CTkRadioButton(
                    filter_frame,
                    text=opcao.capitalize(),
                    variable=filter_var,
                    value=opcao,
                    command=atualizar_listagem # Chama a função de atualização ao mudar o filtro.
                ).pack(side="left", padx=10)
            
            # Frame que irá conter a lista de relatórios.
            content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            content_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # Chama a listagem inicial.
            atualizar_listagem()
        
        # Botão para voltar.
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_admin_menu,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    def show_visualizar_relatorio_admin(self, relatorio):
        # Cria uma nova janela pop-up (Toplevel) para visualização.
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Visualizar Relatório - Admin")
        dialog.geometry("700x600")
        dialog.grab_set() # Bloqueia a interação com a janela principal.
        dialog.resizable(height=False, width=False)

        # Frame rolável para o conteúdo da janela.
        main_scroll = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título do relatório.
        title = ctk.CTkLabel(
            main_scroll,
            text="📄 Relatório de Aula",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        # Crachá de status (Finalizado ou Rascunho) com cores diferentes.
        if relatorio.get('finalizado', False):
            status_frame = ctk.CTkFrame(main_scroll, fg_color="#2CC985", corner_radius=10)
            status_text = "✓ RELATÓRIO FINALIZADO"
        else:
            status_frame = ctk.CTkFrame(main_scroll, fg_color="#F39C12", corner_radius=10)
            status_text = "⚠ RASCUNHO"
        
        status_frame.pack(pady=10)
        ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        ).pack(padx=25, pady=8)
        
        # Frame para exibir os metadados do relatório.
        info_frame = ctk.CTkFrame(main_scroll)
        info_frame.pack(pady=15, padx=40, fill="x")
        
        # Lista dos campos de metadados a serem exibidos.
        info_data = [
            ("Professor", relatorio.get('professor_nome', 'N/A')),
            ("Email do Professor", relatorio.get('professor_email', 'N/A')),
            ("Turma", relatorio.get('turma_nome', 'N/A')),
            ("Disciplina", relatorio.get('disciplina', 'N/A')),
            ("Aula", relatorio.get('aula_titulo', 'N/A')),
            ("Data da Aula", relatorio.get('aula_data', 'N/A')),
            ("Criado em", relatorio.get('data_criacao', 'N/A'))
        ]
        
        # Adiciona a data de finalização se o relatório estiver finalizado.
        if relatorio.get('finalizado', False):
            info_data.append(("Finalizado em", relatorio.get('data_finalizacao', 'N/A')))
        
        # Itera sobre os metadados para criar rótulos de exibição.
        for label, value in info_data:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=3, padx=15)
            
            # Rótulo do campo.
            ctk.CTkLabel(
                row_frame,
                text=f"{label}:",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=150,
                anchor="w"
            ).pack(side="left")
            
            # Rótulo do valor.
            ctk.CTkLabel(
                row_frame,
                text=value,
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="w"
            ).pack(side="left", padx=10)
        
        # Separador visual.
        separator = ctk.CTkFrame(main_scroll, height=2, fg_color="gray")
        separator.pack(fill="x", padx=40, pady=20)
        
        # Rótulo para o conteúdo principal.
        ctk.CTkLabel(
            main_scroll,
            text="Conteúdo do Relatório:",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(pady=(10, 5), padx=40, anchor="w")
        
        # Área de texto para o conteúdo do relatório (somente leitura).
        relatorio_text = ctk.CTkTextbox(
            main_scroll,
            width=750,
            height=300,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        relatorio_text.pack(padx=40, pady=(0, 20))
        # Insere o texto e o configura como desabilitado (somente leitura).
        relatorio_text.insert("1.0", relatorio.get('texto', ''))
        relatorio_text.configure(state="disabled")
        
        # Botão para fechar a janela de visualização.
        close_btn = ctk.CTkButton(
            dialog,
            text="Fechar",
            command=dialog.destroy,
            width=200,
            height=45,
            fg_color="gray",
            hover_color="darkgray"
        )
        close_btn.pack(pady=20)
    
    def darken_color(self, hex_color):
        # Função utilitária para escurecer uma cor hexadecimal.
        hex_color = hex_color.lstrip('#')
        # Converte a cor hexadecimal para RGB.
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        # Escurece cada componente RGB em 20% (multiplica por 0.8).
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        # Retorna o novo valor RGB formatado em hexadecimal.
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"