import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime


class TelasAdmin:
    
    def __init__(self, app, user_email):
        self.app = app
        self.user_email = user_email
        
    def show_editar_turma(self, turma):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title(f"Editar Turma: {turma['nome']}")
        dialog.geometry("700x750")  # Aumentei a altura
        dialog.grab_set()
        dialog.resizable(height=False, width=False)

        main_frame = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            main_frame,
            text=f"✏️ Editar Turma: {turma['nome']}",
            font=ctk.CTkFont(size=24, weight="bold"),
            wraplength=400
        )
        title_label.pack(pady=(20, 30))
        
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=10, padx=80, fill="x")
        
        # 1. Nome
        nome_label = ctk.CTkLabel(form_frame, text="Nome da Turma:", font=ctk.CTkFont(size=14, weight="bold"))
        nome_label.pack(pady=(20, 5), padx=20, anchor="w")
        nome_entry = ctk.CTkEntry(form_frame, height=40)
        nome_entry.insert(0, turma.get('nome', ''))
        nome_entry.pack(pady=(0, 15), padx=20, fill="x")
        
        # 2. Disciplina
        disciplina_label = ctk.CTkLabel(form_frame, text="Disciplina:", font=ctk.CTkFont(size=14, weight="bold"))
        disciplina_label.pack(pady=(15, 5), padx=20, anchor="w")
        disciplina_entry = ctk.CTkEntry(form_frame, height=40)
        disciplina_entry.insert(0, turma.get('disciplina', ''))
        disciplina_entry.pack(pady=(0, 15), padx=20, fill="x")
        
        # 3. Ano
        ano_label = ctk.CTkLabel(form_frame, text="Ano Letivo:", font=ctk.CTkFont(size=14, weight="bold"))
        ano_label.pack(pady=(15, 5), padx=20, anchor="w")
        ano_entry = ctk.CTkEntry(form_frame, height=40)
        ano_entry.insert(0, turma.get('ano', ''))
        ano_entry.pack(pady=(0, 15), padx=20, fill="x")
        
        # 4. Período (RadioButton)
        periodo_label = ctk.CTkLabel(form_frame, text="Período:", font=ctk.CTkFont(size=14, weight="bold"))
        periodo_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        periodo_var = ctk.StringVar(value=turma.get('periodo', 'Manhã'))
        periodo_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        periodo_frame.pack(pady=(0, 15), padx=20, anchor="w")
        
        periodos = ["Manhã", "Tarde", "Noite", "Integral"]
        for periodo in periodos:
            rb = ctk.CTkRadioButton(periodo_frame, text=periodo, variable=periodo_var, value=periodo)
            rb.pack(side="left", padx=5)
        
        # 5. PROFESSOR (EDITÁVEL!) 🎯
        prof_label = ctk.CTkLabel(form_frame, text="Professor:", font=ctk.CTkFont(size=14, weight="bold"))
        prof_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        from backend.turmas_backend import get_professores_disponiveis
        professores = get_professores_disponiveis()
        
        if not professores:
            ctk.CTkLabel(
                form_frame,
                text="⚠️ Nenhum professor cadastrado no sistema",
                text_color="#E74C3C"
            ).pack(pady=(0, 15), padx=20, anchor="w")
            professor_var = None
        else:
            professor_options = [f"{p['nome']} ({p['email']})" for p in professores]
            professor_map = {f"{p['nome']} ({p['email']})": p['email'] for p in professores}
            
            # Selecionar o professor atual
            professor_atual = f"{turma.get('professor_nome', 'N/A')} ({turma.get('professor_email', 'N/A')})"
            if professor_atual not in professor_options:
                professor_atual = professor_options[0] if professor_options else None
            
            professor_var = ctk.StringVar(value=professor_atual)
            
            professor_menu = ctk.CTkOptionMenu(
                form_frame,
                variable=professor_var,
                values=professor_options,
                width=600,
                height=40
            )
            professor_menu.pack(pady=(0, 15), padx=20)

        # 6. Descrição
        descricao_label = ctk.CTkLabel(form_frame, text="Descrição:", font=ctk.CTkFont(size=14, weight="bold"))
        descricao_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        descricao_text = ctk.CTkTextbox(form_frame, height=100)
        descricao_text.insert("0.0", turma.get('descricao', ''))
        descricao_text.pack(pady=(0, 20), padx=20, fill="x")
        
        def salvar_edicao():
            nome = nome_entry.get().strip()
            disciplina = disciplina_entry.get().strip()
            ano = ano_entry.get().strip()
            periodo = periodo_var.get()
            descricao = descricao_text.get("1.0", "end-1c").strip()
            
            if not all([nome, disciplina, ano]):
                messagebox.showerror("Erro", "Nome, Disciplina e Ano são obrigatórios!")
                return
            
            from backend.turmas_backend import editar_turma, atribuir_professor_turma, get_detalhes_completos_turma
            
            # 1. Editar dados básicos da turma
            sucesso = editar_turma(turma['id'], nome, disciplina, ano, periodo, descricao)
            
            if not sucesso:
                messagebox.showerror("Erro", "Erro ao salvar edição da turma.")
                return
            
            # 2. Atribuir/trocar professor (se houver professores disponíveis)
            if professor_var and professores:
                professor_email = professor_map.get(professor_var.get())
                if professor_email:
                    sucesso_prof, msg_prof = atribuir_professor_turma(turma['id'], professor_email)
                    if not sucesso_prof:
                        messagebox.showwarning("Aviso", f"Turma editada, mas: {msg_prof}")
            
            messagebox.showinfo("Sucesso", "Turma atualizada com sucesso!")
            dialog.destroy()
            
            turma_atualizada = get_detalhes_completos_turma(turma['id'])
            self.show_detalhes_turma(turma_atualizada)
        
        button_wrapper_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_wrapper_frame.pack(pady=(10, 20))

        create_btn = ctk.CTkButton(
            button_wrapper_frame,
            text="✓ Salvar Alterações",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=50,
            command=salvar_edicao,
            fg_color="#3B8EDC",
            hover_color="#36719F"
        )
        create_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_wrapper_frame,
            text="← Cancelar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=dialog.destroy,
            fg_color="gray",
            hover_color="darkgray"
        )
        cancel_btn.pack(side="left", padx=10)
        
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

        scroll_container = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        main_frame = ctk.CTkFrame(scroll_container, corner_radius=0)
        main_frame.pack(padx=20, pady=20, fill="x")
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="➕ Criar Nova Turma",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Adicionar ANTES dos campos de nome, após o form_frame:

        # Seleção de Professor
        prof_label = ctk.CTkLabel(form_frame, text="Professor Responsável:", font=ctk.CTkFont(size=14, weight="bold"))
        prof_label.pack(pady=(20, 5), padx=20, anchor="w")

        from backend.turmas_backend import get_professores_disponiveis
        professores = get_professores_disponiveis()

        if not professores:
            ctk.CTkLabel(
                form_frame,
                text="⚠️ Cadastre professores antes de criar turmas!",
                text_color="#E74C3C"
            ).pack(pady=(0, 15), padx=20, anchor="w")
            professor_var = None
        else:
            professor_options = [f"{p['nome']} ({p['email']})" for p in professores]
            professor_map = {f"{p['nome']} ({p['email']})": p['email'] for p in professores}
            
            professor_var = ctk.StringVar(value=professor_options[0])
            
            professor_menu = ctk.CTkOptionMenu(
                form_frame,
                variable=professor_var,
                values=professor_options,
                width=600,
                height=40
            )
            professor_menu.pack(pady=(0, 15), padx=20)

        # ... resto dos campos (nome, disciplina, etc)
        
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=10, padx=80, fill="x") 
        
        nome_label = ctk.CTkLabel(form_frame, text="Nome da Turma:", font=ctk.CTkFont(size=14, weight="bold"))
        nome_label.pack(pady=(20, 5), padx=20, anchor="w") 
        
        nome_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: Turma A - 2024", height=40)
        nome_entry.pack(pady=(0, 15), padx=20, fill="x") 
        
        disciplina_label = ctk.CTkLabel(form_frame, text="Disciplina:", font=ctk.CTkFont(size=14, weight="bold"))
        disciplina_label.pack(pady=(15, 5), padx=20, anchor="w") 
        
        disciplina_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: Matemática", height=40)
        disciplina_entry.pack(pady=(0, 15), padx=20, fill="x") 
        
        ano_label = ctk.CTkLabel(form_frame, text="Ano Letivo:", font=ctk.CTkFont(size=14, weight="bold"))
        ano_label.pack(pady=(15, 5), padx=20, anchor="w") 
        
        ano_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: 2024", height=40)
        ano_entry.pack(pady=(0, 15), padx=20, fill="x") 
        
        periodo_label = ctk.CTkLabel(form_frame, text="Período:", font=ctk.CTkFont(size=14, weight="bold"))
        periodo_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        periodo_var = ctk.StringVar(value="Manhã")
        periodo_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        
        periodo_frame.pack(pady=(0, 15), padx=20, anchor="w") 
        
        periodos = ["Manhã", "Tarde", "Noite", "Integral"]
        for periodo in periodos:
            rb = ctk.CTkRadioButton(periodo_frame, text=periodo, variable=periodo_var, value=periodo)
            rb.pack(side="left", padx=5) 
        
        descricao_label = ctk.CTkLabel(form_frame, text="Descrição:", font=ctk.CTkFont(size=14, weight="bold"))
        descricao_label.pack(pady=(15, 5), padx=20, anchor="w") 
        
        descricao_text = ctk.CTkTextbox(form_frame, height=100)
        descricao_text.pack(pady=(0, 20), padx=20, fill="x")
        
        def process_criar():
            nome = nome_entry.get().strip()
            disciplina = disciplina_entry.get().strip()
            ano = ano_entry.get().strip()
            periodo = periodo_var.get()
            descricao = descricao_text.get("1.0", "end-1c").strip()
            
            if not all([nome, disciplina, ano]):
                messagebox.showerror("Erro", "Nome, Disciplina e Ano são obrigatórios!")
                return
            
            if not professor_var or not professores:
                messagebox.showerror("Erro", "Selecione um professor!")
                return
            
            professor_email = professor_map.get(professor_var.get())
            
            from backend.turmas_backend import criar_turma, get_turma_por_id
            turma_id = criar_turma(professor_email, nome, disciplina, ano, periodo, descricao)
            
            if turma_id:
                messagebox.showinfo("Sucesso", "Turma criada com sucesso!")
                turma = get_turma_por_id(turma_id)
                if turma:
                    self.show_detalhes_turma_criada(turma)
                else:
                    self.show_admin_menu()
            else:
                messagebox.showerror("Erro", "Erro ao criar turma!")
        
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(pady=20) 
        
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
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_admin_menu,
            fg_color="gray",
            hover_color="darkgray"
        )
        cancel_btn.pack(side="left", padx=10)
    
    def show_detalhes_turma_criada(self, turma):
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
        
        from backend.turmas_backend import get_alunos_turma
        alunos = get_alunos_turma(turma['id'])
        
        alunos_frame = ctk.CTkFrame(main_frame)
        alunos_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(
            alunos_frame,
            text="👥 Alunos Matriculados",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15)
        
        if not alunos:
            ctk.CTkLabel(
                alunos_frame,
                text="Nenhum aluno matriculado ainda.",
                text_color="gray"
            ).pack(pady=20)
        else:
            for aluno in alunos:
                aluno_frame = ctk.CTkFrame(alunos_frame)
                aluno_frame.pack(pady=5, padx=10, fill="x")
                
                ctk.CTkLabel(
                    aluno_frame,
                    text=f"👤 {aluno['nome']} - {aluno['email']}",
                    font=ctk.CTkFont(size=14)
                ).pack(side="left", padx=20, pady=10)
        
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
        
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar ao Menu",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_admin_menu,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    def show_adicionar_aluno_criada(self, turma):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Adicionar Aluno")
        dialog.geometry("550x500")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)
        
        main_scroll = ctk.CTkScrollableFrame(dialog, width=500, height=420)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(
            main_scroll,
            text="Adicionar Aluno à Turma",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=20)
        
        from backend.turmas_backend import get_alunos_disponiveis
        alunos_disponiveis = get_alunos_disponiveis(turma['id'])
        
        if not alunos_disponiveis:
            ctk.CTkLabel(
                main_scroll,
                text="Não há alunos disponíveis",
                text_color="gray"
            ).pack(pady=20)
            return
        
        selected_aluno = ctk.StringVar(value=alunos_disponiveis[0]['email'])
        
        for aluno in alunos_disponiveis:
            rb = ctk.CTkRadioButton(
                main_scroll,
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
                self.show_detalhes_turma_criada(turma)
            else:
                messagebox.showerror("Erro", "Erro ao adicionar aluno!")
        
        ctk.CTkButton(
            main_scroll,
            text="Adicionar",
            command=add_aluno,
            width=200,
            fg_color="#2CC985"
        ).pack(pady=20)
    
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
        if not aulas:
            ctk.CTkLabel(tabs.tab("📝 Aulas"), text="Nenhuma aula registrada", text_color="gray").pack(pady=20)
        else:
            for aula in aulas:
                aula_frame = ctk.CTkFrame(tabs.tab("📝 Aulas"))
                aula_frame.pack(pady=5, padx=10, fill="x")
                
                ctk.CTkLabel(
                    aula_frame,
                    text=f"📅 {aula['data']} - {aula['titulo']}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    wraplength=550
                ).pack(anchor="w", padx=20, pady=(10, 5))
                
                conteudo_aula = ctk.CTkTextbox(
                    aula_frame,
                    font=ctk.CTkFont(size=13),
                    text_color="gray",
                    wrap="word",
                    height=120,
                    
                )
                conteudo_aula.pack(anchor="w", pady=(5, 2), fill="x", expand=True)
                conteudo_aula.insert("0.0", aula['conteudo'])
                conteudo_aula.configure(state="disabled")
        
        atividades = get_atividades_turma(turma['id'])
        if not atividades:
            ctk.CTkLabel(tabs.tab("📋 Atividades"), text="Nenhuma atividade criada", text_color="gray").pack(pady=20)
        else:
            for atividade in atividades:
                ativ_frame = ctk.CTkFrame(tabs.tab("📋 Atividades"))
                ativ_frame.pack(pady=5, padx=10, fill="x")
                
                ctk.CTkLabel(
                    ativ_frame,
                    text=f"📄 {atividade['titulo']} | Criado em: {atividade['data_criacao']} | Entrega: {atividade['data_entrega']} | Valor: {atividade['valor']} pts",
                    font=ctk.CTkFont(size=13),
                    wraplength=500
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
            command=self.show_admin_menu,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    def show_adicionar_aluno(self, turma):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Adicionar Aluno")
        dialog.geometry("550x500")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)
        
        main_scroll = ctk.CTkScrollableFrame(dialog, width=500, height=420)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(
            main_scroll,
            text="Adicionar Aluno à Turma",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=20)
        
        from backend.turmas_backend import get_alunos_disponiveis
        alunos_disponiveis = get_alunos_disponiveis(turma['id'])
        
        if not alunos_disponiveis:
            ctk.CTkLabel(
                main_scroll,
                text="Não há alunos disponíveis",
                text_color="gray"
            ).pack(pady=20)
            return
        
        selected_aluno = ctk.StringVar(value=alunos_disponiveis[0]['email'])
        
        for aluno in alunos_disponiveis:
            rb = ctk.CTkRadioButton(
                main_scroll,
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
        
        ctk.CTkButton(
            main_scroll,
            text="Adicionar",
            command=add_aluno,
            width=200,
            fg_color="#2CC985"
        ).pack(pady=20)
    
    def show_admin_menu(self):
        self.app.clear_window()
        
        scroll_container = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        main_frame = ctk.CTkFrame(scroll_container, corner_radius=0)
        main_frame.pack(padx=20, pady=20, fill="x")
        
        from backend.turmas_backend import get_user_data
        user_data = get_user_data(self.user_email)
        
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=20, pady=(20, 30))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"👨‍💼 Painel do Administrador",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=f"Bem-vindo, {user_data['nome']} | {self.user_email}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack()
        
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)
        
        buttons_data = [
            ("👥 Gerenciar Usuários", self.show_gerenciar_usuarios, "#3498DB"),
            ("📚 Gerenciar Turmas", self.show_gerenciar_turmas, "#9B59B6"),
            ("➕ Criar Turmas", self.show_criar_turma, "#E74C3C"),
            ("📄 Relatórios de Aulas", self.show_relatorios_aulas_admin, "#16A085"),
            ("📊 Relatórios Gerais", self.show_relatorios_gerais, "#2CC985"),
            ("📈 Estatísticas do Sistema", self.show_estatisticas, "#E67E22"),
            ("🗑️ Limpeza de Dados", self.show_limpeza_dados, "#E74C3C"),
            ("🚪 Sair", lambda: self.app.logout(), "#34495E")
        ]
        
        for text, command, color in buttons_data:
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                font=ctk.CTkFont(size=16, weight="bold"),
                width=450,
                height=55,
                command=command,
                fg_color=color,
                hover_color=self.darken_color(color)
            )
            btn.pack(pady=8)
    
    def show_gerenciar_usuarios(self):
        if not hasattr(self, 'filter_var'):
            self.filter_var = ctk.StringVar(value="TODOS")
        
        if not hasattr(self, 'search_var'):
            self.search_var = ctk.StringVar(value="")

        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="👥 Gerenciar Usuários",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 20))

        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(pady=10, padx=40, fill="x")
        
        search_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        search_frame.pack(pady=(5, 10), padx=5, fill="x")
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por nome ou email...",
            width=500,
            textvariable=self.search_var
        )
        search_entry.pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            width=80,
            command=self.show_gerenciar_usuarios
        ).pack(side="left", padx=10)
        
        filter_frame = ctk.CTkFrame(main_frame)
        filter_frame.pack(pady=10, padx=40, fill="x")
        
        ctk.CTkLabel(
            filter_frame, 
            text="Filtrar:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=15, pady=10)
        
        for option in ["TODOS", "ADMIN", "INSTRUCTOR", "USER"]:
            rb = ctk.CTkRadioButton(
                filter_frame,
                text=option,
                variable=self.filter_var,
                value=option,
                command=lambda: self.show_gerenciar_usuarios()
            )
            rb.pack(side="left", padx=10)
        
        from backend.turmas_backend import get_todos_usuarios

        search_term = self.search_var.get() if self.search_var.get() else None

        usuarios = get_todos_usuarios(self.filter_var.get(), search_term=search_term)
        
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(pady=10, padx=40, fill="x")
        
        total = len(usuarios)
        admins = len([u for u in usuarios if u['role'] == 'ADMIN'])
        professores = len([u for u in usuarios if u['role'] == 'INSTRUCTOR'])
        alunos = len([u for u in usuarios if u['role'] == 'USER'])
        
        ctk.CTkLabel(
            stats_frame,
            text=f"📊 Total: {total} | 👨‍💼 Admins: {admins} | 👨‍🏫 Profs: {professores} | 👨‍🎓 Alunos: {alunos}",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=12)
        
        if not usuarios:
            ctk.CTkLabel(
                main_frame, 
                text="Nenhum usuário encontrado.", 
                text_color="gray"
            ).pack(pady=30)
        else:
            for usuario in usuarios:
                user_frame = ctk.CTkFrame(main_frame)
                user_frame.pack(pady=5, padx=40, fill="x")
                
                info_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
                
                icon = "👨‍💼" if usuario['role'] == 'ADMIN' else "👨‍🏫" if usuario['role'] == 'INSTRUCTOR' else "👨‍🎓"
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"{icon} {usuario['nome']}",
                    font=ctk.CTkFont(size=15, weight="bold")
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"{usuario['email']}",
                    font=ctk.CTkFont(size=11),
                    text_color="gray"
                ).pack(anchor="w")
                
                btn_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
                btn_frame.pack(side="right", padx=8)
                
                
                ctk.CTkButton(
                    btn_frame,
                    text="👁️",
                    width=45,
                    height=32,
                    anchor="center",
                    command=lambda u=usuario: self.show_detalhes_usuario(u)
                ).pack(side="left", padx=2)
                
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
        
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(pady=20)
        
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
    
    def show_detalhes_usuario(self, usuario):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Detalhes do Usuário")
        dialog.geometry("700x500")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)

        main = ctk.CTkFrame(dialog, corner_radius=0)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            main,
            text=f"👤 {usuario['nome']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        info_frame = ctk.CTkFrame(main)
        info_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        from backend.turmas_backend import get_detalhes_completos_usuario
        detalhes = get_detalhes_completos_usuario(usuario['email'])
        
        role_map = {
            'ADMIN': 'Administrador',
            'INSTRUCTOR': 'Professor',
            'USER': 'Aluno'
        }
        
        dados = [
            ("📧 Email:", usuario['email']),

            ("👤 Tipo:", role_map.get(usuario['role'], usuario['role'])),
        ]
        
        if usuario['role'] == 'INSTRUCTOR':
            dados.extend([
                ("📚 Turmas:", str(detalhes.get('total_turmas', 0))),
                ("👥 Total Alunos:", str(detalhes.get('total_alunos', 0))),
                ("📝 Atividades:", str(detalhes.get('total_atividades', 0))),
            ])
        elif usuario['role'] == 'USER':
            dados.extend([
                ("📚 Matriculado em:", f"{detalhes.get('total_turmas', 0)} turma(s)"),
                ("📅 dia da matricula:", detalhes.get('data_matricula', 'N/A')),
                ("✅ Entregas:", str(detalhes.get('atividades_entregues', 0))),
                ("📊 Média:", f"{detalhes.get('media_geral', 0):.2f}"),
            ])
        
        for label, valor in dados:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(pady=6, padx=15, fill="x")
            
            ctk.CTkLabel(
                row_frame,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                width=150,
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                row_frame,
                text=valor,
                font=ctk.CTkFont(size=14),
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(
            dialog,
            text="Fechar",
            command=dialog.destroy,
            width=150,
            height=40,
            fg_color="gray"
        ).pack(pady=20)
    
    def show_editar_usuario(self, usuario):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Editar Usuário")
        dialog.geometry("700x500")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)

        main_scroll = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            main_scroll, 
            text=f"✏️ Editar: {usuario['nome']}", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        form_frame = ctk.CTkFrame(main_scroll)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(
            form_frame, 
            text="Nome:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 3))
        
        nome_entry = ctk.CTkEntry(form_frame, width=450, height=38)
        nome_entry.insert(0, usuario['nome'])
        nome_entry.pack(padx=15, pady=(0, 10))
        
        ctk.CTkLabel(
            form_frame, 
            text="Tipo:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 3))
        
        role_var = ctk.StringVar(value=usuario['role'])
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.pack(anchor="w", padx=15, pady=(0, 15))
        
        roles = [("👨‍💼 Admin", "ADMIN"), ("👨‍🏫 Prof", "INSTRUCTOR"), ("👨‍🎓 Aluno", "USER")]
        for text, value in roles:
            rb = ctk.CTkRadioButton(role_frame, text=text, variable=role_var, value=value)
            rb.pack(side="left", padx=8)
        
        ctk.CTkLabel(
            form_frame, 
            text="Nova Senha (deixe vazio para não alterar):", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 3))
        nova_senha_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Nova Senha", 
            width=450, 
            height=38, 
            show="*"
        )
        nova_senha_entry.pack(padx=15, pady=(0, 10))

        ctk.CTkLabel(
            form_frame, 
            text="Repetir Senha:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 3))
        repetir_senha_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Repita a Nova Senha", 
            width=450, 
            height=38, 
            show="*"
        )
        repetir_senha_entry.pack(padx=15, pady=(0, 10))
        
        
        def salvar_edicao():
            novo_nome = nome_entry.get().strip().title()
            novo_role = role_var.get()
            nova_senha = nova_senha_entry.get().strip()
            repetir_senha = repetir_senha_entry.get().strip()

            senha_criptografada = None

            if nova_senha != repetir_senha:
                messagebox.showerror("Erro de Senha", "As novas senhas não coincidem!")
                return
            
            if nova_senha != "":
                if len(nova_senha) < 6:
                    messagebox.showerror("Erro de Senha", "A nova senha deve ter pelo menos 6 caracteres.")
                    return
            
                from infra import security as infra
                senha_criptografada = infra.criptografar_senha(nova_senha)
            
            if not novo_nome:
                messagebox.showerror("Erro", "O campo nome é obrigatório!")
                return
            
            from backend.turmas_backend import editar_usuario
            sucesso = editar_usuario(usuario['email'], novo_nome, novo_role, senha_criptografada)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário editado!")

                from database import banco
                banco.carregar_usuarios()

                dialog.destroy()
                self.show_gerenciar_usuarios()
            else:
                messagebox.showerror("Erro", "Erro ao editar!")
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar",
            command=salvar_edicao,
            width=160,
            height=42,
            fg_color="#2CC985"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=dialog.destroy,
            width=160,
            height=42,
            fg_color="gray"
        ).pack(side="left", padx=5)
    
    def confirmar_excluir_usuario(self, usuario):
        result = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Excluir usuário?\n\n{usuario['nome']}\n{usuario['email']}\n\n⚠️ IRREVERSÍVEL!",
            icon='warning'
        )
        
        if result:
            from backend.turmas_backend import excluir_usuario
            sucesso = excluir_usuario(usuario['email'])
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário excluído!")
                self.show_gerenciar_usuarios()
            else:
                messagebox.showerror("Erro", "Erro ao excluir!")
    
    def show_adicionar_usuario(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Adicionar Usuário")
        dialog.geometry("550x600")
        dialog.grab_set()
        
        main_scroll = ctk.CTkScrollableFrame(dialog, width=500, height=530)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(
            main_scroll, 
            text="➕ Novo Usuário", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        form_frame = ctk.CTkFrame(main_scroll)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
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
        
        ctk.CTkLabel(
            form_frame, 
            text="Tipo:", 
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 3))
        
        role_var = ctk.StringVar(value="USER")
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.pack(anchor="w", padx=15, pady=(0, 15))
        
        roles = [("👨‍💼 Admin", "ADMIN"), ("👨‍🏫 Prof", "INSTRUCTOR"), ("👨‍🎓 Aluno", "USER")]
        for text, value in roles:
            rb = ctk.CTkRadioButton(role_frame, text=text, variable=role_var, value=value)
            rb.pack(side="left", padx=8)
        
        def adicionar():
            nome = nome_entry.get().strip()
            email = email_entry.get().strip()
            senha = senha_entry.get()
            role = role_var.get()
            
            if not all([nome, email, senha]):
                messagebox.showerror("Erro", "Todos os campos obrigatórios!")
                return
            
            from backend.turmas_backend import adicionar_usuario
            sucesso = adicionar_usuario(nome, email, senha, role)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário adicionado!")
                dialog.destroy()
                self.show_gerenciar_usuarios()
            else:
                messagebox.showerror("Erro", "Email já existe!")
        
        btn_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="➕ Adicionar",
            command=adicionar,
            width=160,
            height=42,
            fg_color="#2CC985"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=dialog.destroy,
            width=160,
            height=42,
            fg_color="gray"
        ).pack(side="left", padx=5)
    
    def show_gerenciar_turmas(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📚 Gerenciar Turmas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 20))
        
        from backend.turmas_backend import get_todas_turmas
        turmas = get_todas_turmas()
        
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(pady=10, padx=40, fill="x")
        
        total_turmas = len(turmas)
        total_alunos = sum([t['total_alunos'] for t in turmas])
        
        ctk.CTkLabel(
            stats_frame,
            text=f"📊 {total_turmas} turma(s) | {total_alunos} aluno(s) matriculado(s)",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=12)
        
        if not turmas:
            ctk.CTkLabel(
                main_frame, 
                text="Nenhuma turma cadastrada.", 
                text_color="gray"
            ).pack(pady=30)
        else:
            for turma in turmas:
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=5, padx=40, fill="x")
                
                info_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"📖 {turma['nome']}",
                    font=ctk.CTkFont(size=15, weight="bold")
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"{turma['disciplina']} | {turma['professor_nome']} | {turma['total_alunos']} alunos",
                    font=ctk.CTkFont(size=11),
                    text_color="gray"
                ).pack(anchor="w")
                
                btn_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                btn_frame.pack(side="right", padx=8)
                
                ctk.CTkButton(
                    btn_frame,
                    text="👁️",
                    width=45,
                    height=32,
                    command=lambda t=turma: self.show_detalhes_turma_admin(t)
                ).pack(side="left", padx=2)
                
                ctk.CTkButton(
                    btn_frame,
                    text="✏",
                    width=45,
                    height=32,
                    fg_color="#E74C3C",
                    hover_color="#C0392B",
                    command=lambda t=turma: self.show_editar_turma(t)
                ).pack(side="left", padx=2)
                
                ctk.CTkButton(
                    btn_frame,
                    text="🗑️",
                    width=45,
                    height=32,
                    fg_color="#E74C3C",
                    hover_color="#C0392B",
                    command=lambda t=turma: self.confirmar_excluir_turma(t)
                ).pack(side="left", padx=2)
        
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
    
    def show_detalhes_turma_admin(self, turma):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Detalhes da Turma")
        dialog.geometry("700x600")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)

        main_scroll = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            main_scroll, 
            text=f"📖 {turma['nome']}", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        from backend.turmas_backend import get_detalhes_completos_turma
        detalhes = get_detalhes_completos_turma(turma['id'])
        
        info_frame = ctk.CTkFrame(main_scroll)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        dados = [
            ("📚 Disciplina:", turma['disciplina']),
            ("👨‍🏫 Professor:", turma['professor_nome']),
            ("📅 Ano:", turma['ano']),
            ("🕐 Período:", turma['periodo']),
            ("👥 Alunos:", str(turma['total_alunos'])),
            ("📝 Aulas:", str(detalhes.get('total_aulas', 0))),
            ("📋 Atividades:", str(detalhes.get('total_atividades', 0))),
        ]
        
        for label, valor in dados:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(pady=6, padx=15, fill="x")
            
            ctk.CTkLabel(
                row_frame, 
                text=label, 
                font=ctk.CTkFont(size=13, weight="bold"), 
                width=140, 
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                row_frame, 
                text=valor, 
                font=ctk.CTkFont(size=13), 
                anchor="w"
            ).pack(side="left")
        
        if detalhes.get('descricao'):
            ctk.CTkLabel(
                main_scroll, 
                text="📄 Descrição:", 
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(anchor="w", padx=35, pady=(15, 5))

        desc_text = ctk.CTkTextbox(
            main_scroll,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="gray",
            wrap="word",
            width=500,
                    
        )
        desc_text.pack(anchor="w", pady=(15, 5),fill="x", expand=True)
        desc_text.insert("1.0", detalhes['descricao'])
        desc_text.configure(state="disabled")
        
        ctk.CTkButton(
            dialog, 
            text="Fechar", 
            command=dialog.destroy, 
            width=150,
            height=40,
            fg_color="gray"
        ).pack(pady=15)
    
    def confirmar_excluir_turma(self, turma):
        result = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Excluir turma?\n\n{turma['nome']}\n{turma['disciplina']}\n\n⚠️ TODOS os dados (aulas, atividades, notas) serão perdidos!\n\nIRREVERSÍVEL!",
            icon='warning'
        )
        
        if result:
            from backend.turmas_backend import excluir_turma
            sucesso = excluir_turma(turma['id'])
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Turma excluída!")
                self.show_gerenciar_turmas()
            else:
                messagebox.showerror("Erro", "Erro ao excluir!")
    
    def show_relatorios_gerais(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📊 Relatórios do Sistema",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 25))
        
        from backend.turmas_backend import get_relatorio_geral
        relatorio = get_relatorio_geral()
        
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
        
        for section_title, items in sections:
            section_frame = ctk.CTkFrame(main_frame)
            section_frame.pack(pady=8, padx=40, fill="x")
            
            ctk.CTkLabel(
                section_frame,
                text=section_title,
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", padx=15, pady=(12, 8))
            
            for label, valor in items:
                row_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
                row_frame.pack(pady=4, padx=30, fill="x")
                
                ctk.CTkLabel(
                    row_frame,
                    text=label,
                    font=ctk.CTkFont(size=13),
                    width=180,
                    anchor="w"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    row_frame,
                    text=valor,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    anchor="w"
                ).pack(side="left")
            
            ctk.CTkLabel(section_frame, text="").pack(pady=6)
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="📄 Exportar",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=150,
            height=45,
            command=lambda: self.exportar_relatorio(relatorio),
            fg_color="#2CC985"
        ).pack(side="left", padx=5)
        
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
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")],
            initialfile=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if save_path:
            from backend.turmas_backend import exportar_relatorio_txt
            sucesso = exportar_relatorio_txt(relatorio, save_path)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Relatório exportado!")
            else:
                messagebox.showerror("Erro", "Erro ao exportar!")
    
    def show_estatisticas(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📈 Estatísticas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 25))
        
        from backend.turmas_backend import get_estatisticas_detalhadas
        stats = get_estatisticas_detalhadas()
        
        ctk.CTkLabel(
            main_frame,
            text="🏆 Top 5 Alunos",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))
        
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.pack(pady=8, padx=40, fill="x")
        
        if stats['top_alunos']:
            for i, aluno in enumerate(stats['top_alunos'], 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🎖️"
                
                ctk.CTkLabel(
                    top_frame,
                    text=f"{medal} {i}º - {aluno['nome']} | {aluno['media']:.2f}",
                    font=ctk.CTkFont(size=13),
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=4)
        else:
            ctk.CTkLabel(
                top_frame,
                text="Nenhum dado disponível",
                text_color="gray"
            ).pack(pady=10)
        
        ctk.CTkLabel(
            main_frame,
            text="👨‍🏫 Professores Ativos",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))
        
        prof_frame = ctk.CTkFrame(main_frame)
        prof_frame.pack(pady=8, padx=40, fill="x")
        
        if stats['professores_ativos']:
            for prof in stats['professores_ativos']:
                ctk.CTkLabel(
                    prof_frame,
                    text=f"👨‍🏫 {prof['nome']} | {prof['turmas']} turma(s) | {prof['atividades']} atividade(s)",
                    font=ctk.CTkFont(size=13),
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=4)
        else:
            ctk.CTkLabel(
                prof_frame,
                text="Nenhum dado disponível",
                text_color="gray"
            ).pack(pady=10)
        
        ctk.CTkLabel(
            main_frame,
            text="📚 Melhores Turmas",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))
        
        turmas_frame = ctk.CTkFrame(main_frame)
        turmas_frame.pack(pady=8, padx=40, fill="x")
        
        if stats['melhores_turmas']:
            for turma in stats['melhores_turmas']:
                ctk.CTkLabel(
                    turmas_frame,
                    text=f"📖 {turma['nome']} | Média: {turma['media']:.2f} | Aprovação: {turma['taxa_aprovacao']:.1f}%",
                    font=ctk.CTkFont(size=13),
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=4)
        else:
            ctk.CTkLabel(
                turmas_frame,
                text="Nenhum dado disponível",
                text_color="gray"
            ).pack(pady=10)
        
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
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="🗑️ Limpeza de Dados",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 15))
        
        warning_label = ctk.CTkLabel(
            main_frame,
            text="⚠️ ATENÇÃO: OPERAÇÕES IRREVERSÍVEIS! ⚠️",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#E74C3C"
        )
        warning_label.pack(pady=(10, 25))
        
        operations = [
            ("Limpar Turmas Antigas", "Excluir turmas de anos anteriores", lambda: self.limpar_turmas_antigas()),
            ("Remover Atividades Antigas", "Excluir atividades com +1 ano", lambda: self.limpar_atividades_antigas()),
            ("Arquivar Inativos", "Remover usuários inativos (+1 ano)", lambda: self.arquivar_inativos()),
        ]
        
        for titulo, descricao, comando in operations:
            op_frame = ctk.CTkFrame(main_frame)
            op_frame.pack(pady=8, padx=40, fill="x")
            
            info_frame = ctk.CTkFrame(op_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=12)
            
            ctk.CTkLabel(
                info_frame,
                text=titulo,
                font=ctk.CTkFont(size=15, weight="bold")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=descricao,
                font=ctk.CTkFont(size=11),
                text_color="gray"
            ).pack(anchor="w", pady=(2, 0))
            
            ctk.CTkButton(
                op_frame,
                text="Executar",
                width=100,
                height=36,
                command=comando,
                fg_color="#E74C3C",
                hover_color="#C0392B"
            ).pack(side="right", padx=15, pady=12)
        
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
        result = messagebox.askyesno(
            "Confirmar",
            "Excluir turmas de anos anteriores?\n\n⚠️ IRREVERSÍVEL!",
            icon='warning'
        )
        
        if result:
            from backend.turmas_backend import limpar_turmas_antigas
            total = limpar_turmas_antigas()
            messagebox.showinfo("Concluído", f"{total} turma(s) removida(s).")
    
    def limpar_atividades_antigas(self):
        result = messagebox.askyesno(
            "Confirmar",
            "Excluir atividades com +1 ano?\n\n⚠️ IRREVERSÍVEL!",
            icon='warning'
        )
        
        if result:
            from backend.turmas_backend import limpar_atividades_antigas
            total = limpar_atividades_antigas()
            messagebox.showinfo("Concluído", f"{total} atividade(s) removida(s).")
    
    def arquivar_inativos(self):
        result = messagebox.askyesno(
            "Confirmar",
            "Arquivar inativos (+1 ano)?\n\n⚠️ IRREVERSÍVEL!",
            icon='warning'
        )
        
        if result:
            from backend.turmas_backend import arquivar_usuarios_inativos
            total = arquivar_usuarios_inativos()
            messagebox.showinfo("Concluído", f"{total} usuário(s) arquivado(s).")
    
    def show_relatorios_aulas_admin(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📄 Relatórios de Aulas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Visualize todos os relatórios de aulas registrados pelos professores",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 30))
        
        from backend.turmas_backend import get_todos_relatorios
        relatorios = get_todos_relatorios()
        
        if not relatorios:
            empty_label = ctk.CTkLabel(
                main_frame,
                text="Nenhum relatório registrado no sistema ainda.",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            filter_frame = ctk.CTkFrame(main_frame)
            filter_frame.pack(pady=10, padx=40, fill="x")
            
            ctk.CTkLabel(
                filter_frame,
                text="Filtrar por status:",
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(side="left", padx=(20, 10))
            
            filter_var = ctk.StringVar(value="TODOS")
            
            def atualizar_listagem():
                for widget in content_frame.winfo_children():
                    widget.destroy()
                
                filtro = filter_var.get()
                relatorios_filtrados = relatorios
                
                if filtro == "FINALIZADOS":
                    relatorios_filtrados = [r for r in relatorios if r.get('finalizado', False)]
                elif filtro == "RASCUNHOS":
                    relatorios_filtrados = [r for r in relatorios if not r.get('finalizado', False)]
                
                def safe_date_sort(relatorio):
                    try:
                        return datetime.strptime(relatorio.get('data_criacao', '01/01/2000 00:00'), "%d/%m/%Y %H:%M")
                    except (ValueError, TypeError):
                        return datetime(2000, 1, 1)
                
                relatorios_filtrados.sort(key=safe_date_sort, reverse=True)
                
                if not relatorios_filtrados:
                    empty = ctk.CTkLabel(
                        content_frame,
                        text="Nenhum relatório encontrado com este filtro.",
                        font=ctk.CTkFont(size=14),
                        text_color="gray"
                    )
                    empty.pack(pady=30)
                else:
                    for relatorio in relatorios_filtrados:
                        rel_frame = ctk.CTkFrame(content_frame)
                        rel_frame.pack(pady=8, padx=20, fill="x")
                        
                        info_frame = ctk.CTkFrame(rel_frame, fg_color="transparent")
                        info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=12)
                        
                        header_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                        header_frame.pack(anchor="w", fill="x")
                        
                        if relatorio.get('finalizado', False):
                            status_badge = ctk.CTkLabel(
                                header_frame,
                                text="✓",
                                font=ctk.CTkFont(size=12, weight="bold"),
                                text_color="#2CC985",
                                width=20
                            )
                            status_badge.pack(side="left")
                        else:
                            status_badge = ctk.CTkLabel(
                                header_frame,
                                text="⚠",
                                font=ctk.CTkFont(size=12, weight="bold"),
                                text_color="#F39C12",
                                width=20
                            )
                            status_badge.pack(side="left")
                        
                        titulo_label = ctk.CTkLabel(
                            header_frame,
                            text=f"{relatorio.get('aula_titulo', 'N/A')}",
                            font=ctk.CTkFont(size=14, weight="bold"),
                            wraplength=400
                        )
                        titulo_label.pack(side="left", padx=5)
                        
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
                        
                        view_btn = ctk.CTkButton(
                            rel_frame,
                            text="👁 Ver",
                            width=100,
                            height=35,
                            fg_color="#16A085",
                            hover_color="#138D75",
                            command=lambda r=relatorio: self.show_visualizar_relatorio_admin(r)
                        )
                        view_btn.pack(side="right", padx=10, pady=10)
            
            for opcao in ["TODOS", "FINALIZADOS", "RASCUNHOS"]:
                ctk.CTkRadioButton(
                    filter_frame,
                    text=opcao.capitalize(),
                    variable=filter_var,
                    value=opcao,
                    command=atualizar_listagem
                ).pack(side="left", padx=10)
            
            content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            content_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            atualizar_listagem()
        
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
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Visualizar Relatório - Admin")
        dialog.geometry("700x600")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)

        main_scroll = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            main_scroll,
            text="📄 Relatório de Aula",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
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
        
        info_frame = ctk.CTkFrame(main_scroll)
        info_frame.pack(pady=15, padx=40, fill="x")
        
        info_data = [
            ("Professor", relatorio.get('professor_nome', 'N/A')),
            ("Email do Professor", relatorio.get('professor_email', 'N/A')),
            ("Turma", relatorio.get('turma_nome', 'N/A')),
            ("Disciplina", relatorio.get('disciplina', 'N/A')),
            ("Aula", relatorio.get('aula_titulo', 'N/A')),
            ("Data da Aula", relatorio.get('aula_data', 'N/A')),
            ("Criado em", relatorio.get('data_criacao', 'N/A'))
        ]
        
        if relatorio.get('finalizado', False):
            info_data.append(("Finalizado em", relatorio.get('data_finalizacao', 'N/A')))
        
        for label, value in info_data:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=3, padx=15)
            
            ctk.CTkLabel(
                row_frame,
                text=f"{label}:",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=150,
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                row_frame,
                text=value,
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="w"
            ).pack(side="left", padx=10)
        
        separator = ctk.CTkFrame(main_scroll, height=2, fg_color="gray")
        separator.pack(fill="x", padx=40, pady=20)
        
        ctk.CTkLabel(
            main_scroll,
            text="Conteúdo do Relatório:",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(pady=(10, 5), padx=40, anchor="w")
        
        relatorio_text = ctk.CTkTextbox(
            main_scroll,
            width=750,
            height=300,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        relatorio_text.pack(padx=40, pady=(0, 20))
        relatorio_text.insert("1.0", relatorio.get('texto', ''))
        relatorio_text.configure(state="disabled")
        
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
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"