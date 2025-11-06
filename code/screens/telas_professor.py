import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime

class TelasProfessor:
    
    def __init__(self, app, user_email):
        self.app = app
        self.user_email = user_email
        
    def show_professor_menu(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        from backend.turmas_backend import get_user_data
        user_data = get_user_data(self.user_email)
        
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=20, pady=(20, 30))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"👨‍🏫 Bem-vindo, Prof. {user_data['nome']}!",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=f"Email: {self.user_email}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack()
        
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)
        
        buttons_data = [
            ("📚 Minhas Turmas", self.show_turmas_professor, "#3498DB"),
            ("➕ Criar Nova Turma", self.show_criar_turma, "#2CC985"),
            ("📝 Registro de Aulas", self.show_registro_aulas, "#9B59B6"),
            ("📋 Atividades", self.show_atividades_professor, "#E67E22"),
            ("📊 Notas e Frequência", self.show_notas_frequencia, "#1ABC9C"),
            ("⚙️ Editar Perfil", lambda: self.app.show_edit_screen(), "#95A5A6"),
            ("🚪 Sair", lambda: self.app.logout(), "#E74C3C")
        ]
        
        for text, command, color in buttons_data:
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                font=ctk.CTkFont(size=16, weight="bold"),
                width=400,
                height=55,
                command=command,
                fg_color=color,
                hover_color=self.darken_color(color)
            )
            btn.pack(pady=8)
    
    def show_turmas_professor(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📚 Minhas Turmas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        from backend.turmas_backend import get_turmas_professor
        turmas = get_turmas_professor(self.user_email)
        
        if not turmas:
            empty_label = ctk.CTkLabel(
                main_frame,
                text="Você ainda não possui turmas cadastradas.\nClique em 'Criar Nova Turma' para começar!",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            for turma in turmas:
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=10, padx=40, fill="x")
                
                info_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                nome_label = ctk.CTkLabel(
                    info_frame,
                    text=f"📖 {turma['nome']}",
                    font=ctk.CTkFont(size=18, weight="bold")
                )
                nome_label.pack(anchor="w")
                
                disciplina_label = ctk.CTkLabel(
                    info_frame,
                    text=f"Disciplina: {turma['disciplina']}",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                disciplina_label.pack(anchor="w", pady=2)
                
                info_label = ctk.CTkLabel(
                    info_frame,
                    text=f"Alunos: {turma['total_alunos']} | Ano: {turma['ano']}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                )
                info_label.pack(anchor="w", pady=2)
                
                buttons_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                buttons_frame.pack(side="right", padx=10, pady=10)
                
                view_btn = ctk.CTkButton(
                    buttons_frame,
                    text="Ver Detalhes",
                    width=120,
                    height=35,
                    command=lambda t=turma: self.show_detalhes_turma(t)
                )
                view_btn.pack(pady=3)
                
                edit_btn = ctk.CTkButton(
                    buttons_frame,
                    text="Editar",
                    width=120,
                    height=35,
                    fg_color="#9B59B6",
                    hover_color="#7D3C98",
                    command=lambda t=turma: self.show_editar_turma(t)
                )
                edit_btn.pack(pady=3)
        
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
        self.app.clear_window()
        
        main_frame = ctk.CTkFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="➕ Criar Nova Turma",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=10, padx=80)
        
        nome_label = ctk.CTkLabel(form_frame, text="Nome da Turma:", font=ctk.CTkFont(size=14, weight="bold"))
        nome_label.grid(row=0, column=0, pady=(20, 5), padx=(20, 10), sticky="w")
        
        nome_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: Turma A - 2024", width=400, height=40)
        nome_entry.grid(row=0, column=1, pady=(20, 5), padx=(10, 20), sticky="w")
        
        disciplina_label = ctk.CTkLabel(form_frame, text="Disciplina:", font=ctk.CTkFont(size=14, weight="bold"))
        disciplina_label.grid(row=1, column=0, pady=(15, 5), padx=(20, 10), sticky="w")
        
        disciplina_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: Matemática", width=400, height=40)
        disciplina_entry.grid(row=1, column=1, pady=(15, 5), padx=(10, 20), sticky="w")
        
        ano_label = ctk.CTkLabel(form_frame, text="Ano Letivo:", font=ctk.CTkFont(size=14, weight="bold"))
        ano_label.grid(row=2, column=0, pady=(15, 5), padx=(20, 10), sticky="w")
        
        ano_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: 2024", width=400, height=40)
        ano_entry.grid(row=2, column=1, pady=(15, 5), padx=(10, 20), sticky="w")
        
        periodo_label = ctk.CTkLabel(form_frame, text="Período:", font=ctk.CTkFont(size=14, weight="bold"))
        periodo_label.grid(row=3, column=0, pady=(15, 5), padx=(20, 10), sticky="w")
        
        periodo_var = ctk.StringVar(value="Manhã")
        periodo_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        periodo_frame.grid(row=3, column=1, pady=(15, 5), padx=(10, 20), sticky="w")
        
        periodos = ["Manhã", "Tarde", "Noite", "Integral"]
        for periodo in periodos:
            rb = ctk.CTkRadioButton(periodo_frame, text=periodo, variable=periodo_var, value=periodo)
            rb.pack(side="left", padx=10)
        
        descricao_label = ctk.CTkLabel(form_frame, text="Descrição:", font=ctk.CTkFont(size=14, weight="bold"))
        descricao_label.grid(row=4, column=0, pady=(15, 5), padx=(20, 10), sticky="nw")
        
        descricao_text = ctk.CTkTextbox(form_frame, width=400, height=100)
        descricao_text.grid(row=4, column=1, pady=(15, 20), padx=(10, 20), sticky="w")
        
        form_frame.grid_columnconfigure(0, weight=0, minsize=180)
        form_frame.grid_columnconfigure(1, weight=1)
        
        def process_criar():
            nome = nome_entry.get().strip()
            disciplina = disciplina_entry.get().strip()
            ano = ano_entry.get().strip()
            periodo = periodo_var.get()
            descricao = descricao_text.get("1.0", "end-1c").strip()
            
            if not all([nome, disciplina, ano]):
                messagebox.showerror("Erro", "Nome, Disciplina e Ano são obrigatórios!")
                return
            
            from backend.turmas_backend import criar_turma
            sucesso = criar_turma(self.user_email, nome, disciplina, ano, periodo, descricao)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Turma criada com sucesso!")
                self.show_turmas_professor()
            else:
                messagebox.showerror("Erro", "Erro ao criar turma!")
        
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
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
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="← Cancelar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_professor_menu,
            fg_color="gray",
            hover_color="darkgray"
        )
        cancel_btn.pack(side="left", padx=10)
    
    def show_detalhes_turma(self, turma):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📖 {turma['nome']}",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        info_label = ctk.CTkLabel(
            main_frame,
            text=f"{turma['disciplina']} | {turma['ano']} | {turma['periodo']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info_label.pack(pady=(0, 30))
        
        tabs = ctk.CTkTabview(main_frame, width=800, height=400)
        tabs.pack(pady=20, padx=40)
        
        tabs.add("👥 Alunos")
        tabs.add("📝 Aulas")
        tabs.add("📋 Atividades")
        
        from backend.turmas_backend import get_alunos_turma, get_aulas_turma, get_atividades_turma
        
        alunos = get_alunos_turma(turma['id'])
        for aluno in alunos:
            aluno_frame = ctk.CTkFrame(tabs.tab("👥 Alunos"))
            aluno_frame.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkLabel(
                aluno_frame,
                text=f"👤 {aluno['nome']} - {aluno['email']}",
                font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=20, pady=10)
        
        add_aluno_btn = ctk.CTkButton(
            tabs.tab("👥 Alunos"),
            text="➕ Adicionar Aluno",
            width=200,
            command=lambda: self.show_adicionar_aluno(turma)
        )
        add_aluno_btn.pack(pady=10)
        
        aulas = get_aulas_turma(turma['id'])
        for aula in aulas:
            aula_frame = ctk.CTkFrame(tabs.tab("📝 Aulas"))
            aula_frame.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkLabel(
                aula_frame,
                text=f"📅 {aula['data']} - {aula['titulo']}\n{aula['conteudo']}",
                font=ctk.CTkFont(size=13)
            ).pack(side="left", padx=20, pady=10, anchor="w")
        
        add_aula_btn = ctk.CTkButton(
            tabs.tab("📝 Aulas"),
            text="➕ Registrar Aula",
            width=200,
            command=lambda: self.show_registrar_aula(turma)
        )
        add_aula_btn.pack(pady=10)
        
        atividades = get_atividades_turma(turma['id'])
        for atividade in atividades:
            ativ_frame = ctk.CTkFrame(tabs.tab("📋 Atividades"))
            ativ_frame.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkLabel(
                ativ_frame,
                text=f"📄 {atividade['titulo']} - Prazo: {atividade['prazo']}",
                font=ctk.CTkFont(size=13)
            ).pack(side="left", padx=20, pady=10)
        
        add_ativ_btn = ctk.CTkButton(
            tabs.tab("📋 Atividades"),
            text="➕ Criar Atividade",
            width=200,
            command=lambda: self.show_criar_atividade(turma)
        )
        add_ativ_btn.pack(pady=10)
        
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_turmas_professor,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    def show_adicionar_aluno(self, turma):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Adicionar Aluno")
        dialog.geometry("500x300")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Adicionar Aluno à Turma", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=20)
        
        from backend.turmas_backend import get_alunos_disponiveis
        alunos_disponiveis = get_alunos_disponiveis(turma['id'])
        
        if not alunos_disponiveis:
            ctk.CTkLabel(dialog, text="Não há alunos disponíveis", text_color="gray").pack(pady=20)
            return
        
        selected_aluno = ctk.StringVar(value=alunos_disponiveis[0]['email'])
        
        for aluno in alunos_disponiveis:
            rb = ctk.CTkRadioButton(
                dialog,
                text=f"{aluno['nome']} - {aluno['email']}",
                variable=selected_aluno,
                value=aluno['email']
            )
            rb.pack(pady=5, padx=20, anchor="w")
        
        def add_aluno():
            from backend.turmas_backend import adicionar_aluno_turma
            sucesso = adicionar_aluno_turma(turma['id'], selected_aluno.get())
            if sucesso:
                messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
                dialog.destroy()
                self.show_detalhes_turma(turma)
            else:
                messagebox.showerror("Erro", "Erro ao adicionar aluno!")
        
        ctk.CTkButton(dialog, text="Adicionar", command=add_aluno, width=200).pack(pady=20)
    
    def show_registrar_aula(self, turma):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Registrar Aula")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Registrar Nova Aula", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=20)
        
        ctk.CTkLabel(dialog, text="Data:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=40, pady=(10, 5))
        data_entry = ctk.CTkEntry(dialog, placeholder_text="DD/MM/AAAA", width=400)
        data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        data_entry.pack(padx=40, pady=(0, 10))
        
        ctk.CTkLabel(dialog, text="Título:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=40, pady=(10, 5))
        titulo_entry = ctk.CTkEntry(dialog, placeholder_text="Ex: Introdução aos Polinômios", width=400)
        titulo_entry.pack(padx=40, pady=(0, 10))
        
        ctk.CTkLabel(dialog, text="Conteúdo:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=40, pady=(10, 5))
        conteudo_text = ctk.CTkTextbox(dialog, width=400, height=150)
        conteudo_text.pack(padx=40, pady=(0, 20))
        
        def registrar():
            data = data_entry.get().strip()
            titulo = titulo_entry.get().strip()
            conteudo = conteudo_text.get("1.0", "end-1c").strip()
            
            if not all([data, titulo, conteudo]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            from backend.turmas_backend import registrar_aula
            sucesso = registrar_aula(turma['id'], data, titulo, conteudo)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Aula registrada com sucesso!")
                dialog.destroy()
                self.show_detalhes_turma(turma)
            else:
                messagebox.showerror("Erro", "Erro ao registrar aula!")
        
        ctk.CTkButton(dialog, text="Registrar Aula", command=registrar, width=200, fg_color="#2CC985").pack(pady=10)
    
    def show_criar_atividade(self, turma):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Criar Atividade")
        dialog.geometry("600x600")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Criar Nova Atividade", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=20)
        
        ctk.CTkLabel(dialog, text="Título:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=40, pady=(10, 5))
        titulo_entry = ctk.CTkEntry(dialog, placeholder_text="Ex: Lista de Exercícios 01", width=400)
        titulo_entry.pack(padx=40, pady=(0, 10))
        
        ctk.CTkLabel(dialog, text="Descrição:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=40, pady=(10, 5))
        descricao_text = ctk.CTkTextbox(dialog, width=400, height=120)
        descricao_text.pack(padx=40, pady=(0, 10))
        
        ctk.CTkLabel(dialog, text="Prazo:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=40, pady=(10, 5))
        prazo_entry = ctk.CTkEntry(dialog, placeholder_text="DD/MM/AAAA", width=400)
        prazo_entry.pack(padx=40, pady=(0, 10))
        
        ctk.CTkLabel(dialog, text="Valor (pontos):", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=40, pady=(10, 5))
        valor_entry = ctk.CTkEntry(dialog, placeholder_text="Ex: 10", width=400)
        valor_entry.pack(padx=40, pady=(0, 10))
        
        arquivo_label = ctk.CTkLabel(dialog, text="Nenhum arquivo selecionado", text_color="gray")
        arquivo_label.pack(pady=5)
        
        arquivo_path = {"path": None}
        
        def selecionar_arquivo():
            path = filedialog.askopenfilename(title="Selecionar arquivo da atividade")
            if path:
                arquivo_path["path"] = path
                arquivo_label.configure(text=f"📎 {path.split('/')[-1]}")
        
        ctk.CTkButton(dialog, text="📎 Anexar Arquivo", command=selecionar_arquivo, width=200).pack(pady=10)
        
        def criar():
            titulo = titulo_entry.get().strip()
            descricao = descricao_text.get("1.0", "end-1c").strip()
            prazo = prazo_entry.get().strip()
            valor = valor_entry.get().strip()
            
            if not all([titulo, descricao, prazo, valor]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            from backend.turmas_backend import criar_atividade
            sucesso = criar_atividade(turma['id'], titulo, descricao, prazo, valor, arquivo_path["path"])
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Atividade criada com sucesso!")
                dialog.destroy()
                self.show_detalhes_turma(turma)
            else:
                messagebox.showerror("Erro", "Erro ao criar atividade!")
        
        ctk.CTkButton(dialog, text="Criar Atividade", command=criar, width=200, fg_color="#2CC985").pack(pady=20)
    
    def show_registro_aulas(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📝 Registro de Aulas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        from backend.turmas_backend import get_todas_aulas_professor
        aulas = get_todas_aulas_professor(self.user_email)
        
        if not aulas:
            ctk.CTkLabel(main_frame, text="Nenhuma aula registrada ainda.", text_color="gray").pack(pady=50)
        else:
            for aula in aulas:
                aula_frame = ctk.CTkFrame(main_frame)
                aula_frame.pack(pady=8, padx=40, fill="x")
                
                ctk.CTkLabel(
                    aula_frame,
                    text=f"📅 {aula['data']} | {aula['turma']}",
                    font=ctk.CTkFont(size=14, weight="bold")
                ).pack(anchor="w", padx=20, pady=(10, 5))
                
                ctk.CTkLabel(
                    aula_frame,
                    text=f"📖 {aula['titulo']}",
                    font=ctk.CTkFont(size=13)
                ).pack(anchor="w", padx=20, pady=2)
                
                ctk.CTkLabel(
                    aula_frame,
                    text=aula['conteudo'][:100] + "..." if len(aula['conteudo']) > 100 else aula['conteudo'],
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                ).pack(anchor="w", padx=20, pady=(2, 10))
        
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
    
    def show_atividades_professor(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📋 Todas as Atividades",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        from backend.turmas_backend import get_todas_atividades_professor
        atividades = get_todas_atividades_professor(self.user_email)
        
        if not atividades:
            ctk.CTkLabel(main_frame, text="Nenhuma atividade criada ainda.", text_color="gray").pack(pady=50)
        else:
            for atividade in atividades:
                ativ_frame = ctk.CTkFrame(main_frame)
                ativ_frame.pack(pady=8, padx=40, fill="x")
                
                info_frame = ctk.CTkFrame(ativ_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"📄 {atividade['titulo']}",
                    font=ctk.CTkFont(size=16, weight="bold")
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"Turma: {atividade['turma']} | Prazo: {atividade['prazo']} | Valor: {atividade['valor']} pts",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                ctk.CTkButton(
                    ativ_frame,
                    text="Ver Entregas",
                    width=120,
                    height=35,
                    command=lambda a=atividade: self.show_entregas_atividade(a)
                ).pack(side="right", padx=10, pady=10)
        
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
    
    def show_entregas_atividade(self, atividade):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📝 Entregas: {atividade['titulo']}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        from backend.turmas_backend import get_entregas_atividade
        entregas = get_entregas_atividade(atividade['id'])
        
        if not entregas:
            ctk.CTkLabel(main_frame, text="Nenhuma entrega ainda.", text_color="gray").pack(pady=50)
        else:
            for entrega in entregas:
                entrega_frame = ctk.CTkFrame(main_frame)
                entrega_frame.pack(pady=8, padx=40, fill="x")
                
                info_frame = ctk.CTkFrame(entrega_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"👤 {entrega['aluno_nome']}",
                    font=ctk.CTkFont(size=15, weight="bold")
                ).pack(anchor="w")
                
                status_color = "#2CC985" if entrega['nota'] else "#E67E22"
                status_text = f"Nota: {entrega['nota']}" if entrega['nota'] else "Aguardando correção"
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"Entregue em: {entrega['data_entrega']} | {status_text}",
                    font=ctk.CTkFont(size=12),
                    text_color=status_color
                ).pack(anchor="w", pady=2)
                
                btn_frame = ctk.CTkFrame(entrega_frame, fg_color="transparent")
                btn_frame.pack(side="right", padx=10, pady=10)
                
                ctk.CTkButton(
                    btn_frame,
                    text="Baixar",
                    width=100,
                    height=35,
                    command=lambda e=entrega: self.baixar_entrega(e)
                ).pack(pady=3)
                
                ctk.CTkButton(
                    btn_frame,
                    text="Avaliar",
                    width=100,
                    height=35,
                    fg_color="#2CC985",
                    command=lambda e=entrega: self.avaliar_entrega(e, atividade)
                ).pack(pady=3)
        
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_atividades_professor,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    def avaliar_entrega(self, entrega, atividade):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Avaliar Entrega")
        dialog.geometry("500x400")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text=f"Avaliar: {entrega['aluno_nome']}", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=20)
        
        ctk.CTkLabel(dialog, text=f"Valor da atividade: {atividade['valor']} pontos", text_color="gray").pack(pady=5)
        
        ctk.CTkLabel(dialog, text="Nota:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
        nota_entry = ctk.CTkEntry(dialog, placeholder_text=f"0 a {atividade['valor']}", width=300)
        nota_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(dialog, text="Feedback:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        feedback_text = ctk.CTkTextbox(dialog, width=400, height=150)
        feedback_text.pack(pady=(0, 20))
        
        def salvar_avaliacao():
            nota = nota_entry.get().strip()
            feedback = feedback_text.get("1.0", "end-1c").strip()
            
            if not nota:
                messagebox.showerror("Erro", "A nota é obrigatória!")
                return
            
            try:
                nota_float = float(nota)
                if nota_float < 0 or nota_float > float(atividade['valor']):
                    messagebox.showerror("Erro", f"Nota deve estar entre 0 e {atividade['valor']}!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Nota inválida!")
                return
            
            from backend.turmas_backend import avaliar_entrega
            sucesso = avaliar_entrega(entrega['id'], nota_float, feedback)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Avaliação salva com sucesso!")
                dialog.destroy()
                self.show_entregas_atividade(atividade)
            else:
                messagebox.showerror("Erro", "Erro ao salvar avaliação!")
        
        ctk.CTkButton(dialog, text="Salvar Avaliação", command=salvar_avaliacao, width=200, fg_color="#2CC985").pack(pady=10)
    
    def baixar_entrega(self, entrega):
        if entrega.get('arquivo'):
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=entrega['arquivo'],
                title="Salvar arquivo"
            )
            if save_path:
                from backend.turmas_backend import baixar_arquivo_entrega
                sucesso = baixar_arquivo_entrega(entrega['id'], save_path)
                if sucesso:
                    messagebox.showinfo("Sucesso", "Arquivo baixado com sucesso!")
                else:
                    messagebox.showerror("Erro", "Erro ao baixar arquivo!")
        else:
            messagebox.showinfo("Info", "Esta entrega não possui arquivo anexado.")
    
    def show_notas_frequencia(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📊 Notas e Frequência",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        from backend.turmas_backend import get_turmas_professor
        turmas = get_turmas_professor(self.user_email)
        
        for turma in turmas:
            turma_frame = ctk.CTkFrame(main_frame)
            turma_frame.pack(pady=10, padx=40, fill="x")
            
            ctk.CTkLabel(
                turma_frame,
                text=f"📖 {turma['nome']}",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(anchor="w", padx=20, pady=(15, 5))
            
            ctk.CTkButton(
                turma_frame,
                text="Ver Boletim da Turma",
                width=200,
                command=lambda t=turma: self.show_boletim_turma(t)
            ).pack(anchor="w", padx=20, pady=(5, 15))
        
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
    
    def show_boletim_turma(self, turma):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📊 Boletim: {turma['nome']}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        from backend.turmas_backend import get_boletim_turma
        boletim = get_boletim_turma(turma['id'])
        
        for aluno_data in boletim:
            aluno_frame = ctk.CTkFrame(main_frame)
            aluno_frame.pack(pady=8, padx=40, fill="x")
            
            ctk.CTkLabel(
                aluno_frame,
                text=f"👤 {aluno_data['nome']}",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", padx=20, pady=(10, 5))
            
            media = aluno_data['media'] if aluno_data['media'] else 0
            status = "Aprovado" if media >= 7 else "Reprovado" if media >= 0 else "Sem notas"
            status_color = "#2CC985" if media >= 7 else "#E74C3C" if media >= 0 else "gray"
            
            ctk.CTkLabel(
                aluno_frame,
                text=f"Média: {media:.1f} | Frequência: {aluno_data['frequencia']}% | Status: {status}",
                font=ctk.CTkFont(size=13),
                text_color=status_color
            ).pack(anchor="w", padx=20, pady=(2, 10))
        
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_notas_frequencia,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    def show_editar_turma(self, turma):
        messagebox.showinfo("Em desenvolvimento", "Funcionalidade de edição em desenvolvimento!")
    
    def darken_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
