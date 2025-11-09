import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import os
from screens.tela_registro_aulas import TelaRegistroAulas

class TelasProfessor:
    
    def __init__(self, app, user_email):
        self.app = app
        self.user_email = user_email
        
    def show_professor_menu(self):
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
        if not aulas:
            ctk.CTkLabel(tabs.tab("📝 Aulas"), text="Nenhuma aula registrada", text_color="gray").pack(pady=20)
        else:
            for aula in aulas:
                aula_frame = ctk.CTkFrame(tabs.tab("📝 Aulas"))
                aula_frame.pack(pady=5, padx=10, fill="x")
                
                ctk.CTkLabel(
                    aula_frame,
                    text=f"📅 {aula['data']} - {aula['titulo']}",
                    font=ctk.CTkFont(size=13, weight="bold")
                ).pack(anchor="w", padx=20, pady=(10, 5))
                
                ctk.CTkLabel(
                    aula_frame,
                    text=aula['conteudo'][:100] + "..." if len(aula['conteudo']) > 100 else aula['conteudo'],
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                ).pack(anchor="w", padx=20, pady=(0, 10))
        
        atividades = get_atividades_turma(turma['id'])
        if not atividades:
            ctk.CTkLabel(tabs.tab("📋 Atividades"), text="Nenhuma atividade criada", text_color="gray").pack(pady=20)
        else:
            for atividade in atividades:
                ativ_frame = ctk.CTkFrame(tabs.tab("📋 Atividades"))
                ativ_frame.pack(pady=5, padx=10, fill="x")
                
                ctk.CTkLabel(
                    ativ_frame,
                    text=f"📄 {atividade['titulo']} - Entrega: {atividade['data_entrega']} - Valor: {atividade['valor']} pts",
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
        dialog.geometry("550x500")
        dialog.grab_set()
        
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
    
    def show_registro_aulas(self):
        tela_aulas = TelaRegistroAulas(self.app, self.user_email)
        tela_aulas.show()
    
    def show_atividades_professor(self):
        """Mostra todas as atividades do professor com informação de entregas"""
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📋 Minhas Atividades",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # NOVA FUNÇÃO: Obtém atividades com informações de entregas
        from backend.turmas_backend import get_atividades_com_entregas
        atividades = get_atividades_com_entregas(self.user_email)
        
        if not atividades:
            ctk.CTkLabel(main_frame, text="Nenhuma atividade criada ainda.", text_color="gray").pack(pady=50)
        else:
            for atividade in atividades:
                ativ_frame = ctk.CTkFrame(main_frame)
                ativ_frame.pack(pady=8, padx=40, fill="x")
                
                info_frame = ctk.CTkFrame(ativ_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                # Título da atividade
                ctk.CTkLabel(
                    info_frame,
                    text=f"📄 {atividade['titulo']}",
                    font=ctk.CTkFont(size=16, weight="bold")
                ).pack(anchor="w")
                
                # Informações da turma
                ctk.CTkLabel(
                    info_frame,
                    text=f"Turma: {atividade['turma_nome']} - {atividade['disciplina']}",
                    font=ctk.CTkFont(size=13),
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                # Informações da atividade
                ctk.CTkLabel(
                    info_frame,
                    text=f"Entrega: {atividade['data_entrega']} | Valor: {atividade['valor']} pts",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                # STATUS DAS ENTREGAS - INFORMAÇÃO CRUCIAL
                total_alunos = atividade['total_alunos']
                entregas = atividade['total_entregas']
                corrigidas = atividade['entregas_corrigidas']
                pendentes = atividade['entregas_pendentes']
                nao_entregaram = total_alunos - entregas
                
                # Texto de status com cores
                if entregas == 0:
                    status_text = f"⚠️  Nenhuma entrega ainda ({total_alunos} alunos na turma)"
                    status_color = "#E74C3C"
                elif pendentes > 0:
                    status_text = f"📝 {entregas}/{total_alunos} entregas | {pendentes} aguardando correção | {corrigidas} corrigidas"
                    status_color = "#E67E22"
                else:
                    status_text = f"✅ {entregas}/{total_alunos} entregas | Todas corrigidas"
                    status_color = "#2CC985"
                
                ctk.CTkLabel(
                    info_frame,
                    text=status_text,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=status_color
                ).pack(anchor="w", pady=5)
                
                # Botão para ver entregas
                ctk.CTkButton(
                    ativ_frame,
                    text="Ver Entregas",
                    width=120,
                    height=35,
                    command=lambda a=atividade: self.show_entregas_atividade(a)
                ).pack(side="right", padx=10, pady=10)
        
        # Botão para criar nova atividade
        create_btn = ctk.CTkButton(
            main_frame,
            text="➕ Criar Nova Atividade",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=250,
            height=50,
            command=lambda: self.show_criar_atividade(),
            fg_color="#2CC985",
            hover_color="#25A066"
        )
        create_btn.pack(pady=20)
        
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
        """Mostra todas as entregas de uma atividade com status detalhado"""
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📝 Entregas: {atividade['titulo']}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        info_label = ctk.CTkLabel(
            main_frame,
            text=f"Turma: {atividade['turma_nome']} | Valor: {atividade['valor']} pontos | Entrega: {atividade['data_entrega']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info_label.pack(pady=(0, 20))
        
        # USAR NOVA FUNÇÃO PARA OBTER DETALHES COMPLETOS
        from backend.turmas_backend import get_detalhes_atividade_professor
        detalhes = get_detalhes_atividade_professor(atividade['id'])
        
        if not detalhes:
            ctk.CTkLabel(main_frame, text="Erro ao carregar detalhes da atividade.", text_color="red").pack(pady=50)
            return
        
        # Resumo de entregas
        resumo_frame = ctk.CTkFrame(main_frame)
        resumo_frame.pack(pady=10, padx=40, fill="x")
        
        ctk.CTkLabel(
            resumo_frame,
            text=f"📊 Status: {detalhes['total_entregas']}/{detalhes['total_alunos']} entregas | {detalhes['total_corrigidas']} corrigidas | {detalhes['total_pendentes']} pendentes",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=15)
        
        # Tabs para organizar
        tabs = ctk.CTkTabview(main_frame, width=900, height=400)
        tabs.pack(pady=20, padx=40)
        
        tabs.add("✅ Entregas Recebidas")
        tabs.add("⚠️ Não Entregaram")
        
        # TAB 1: Entregas recebidas
        entregas = detalhes['entregas']
        if not entregas:
            ctk.CTkLabel(tabs.tab("✅ Entregas Recebidas"), text="Nenhuma entrega ainda.", text_color="gray").pack(pady=20)
        else:
            for entrega in entregas:
                entrega_frame = ctk.CTkFrame(tabs.tab("✅ Entregas Recebidas"))
                entrega_frame.pack(pady=8, padx=10, fill="x")
                
                info_frame = ctk.CTkFrame(entrega_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                # Nome e RM do aluno
                ctk.CTkLabel(
                    info_frame,
                    text=f"👤 {entrega['aluno_nome']} (RM: {entrega['aluno_rm']})",
                    font=ctk.CTkFont(size=15, weight="bold")
                ).pack(anchor="w")
                
                # Status da correção
                if entrega.get('nota') is not None:
                    status_text = f"✅ Nota: {entrega['nota']:.1f}/{atividade['valor']}"
                    status_color = "#2CC985"
                else:
                    status_text = "⏳ Aguardando Correção"
                    status_color = "#E67E22"
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"Entregue em: {entrega['data_entrega']} | Status: {status_text}",
                    font=ctk.CTkFont(size=12),
                    text_color=status_color
                ).pack(anchor="w", pady=2)
                
                # Botões de ação
                btn_frame = ctk.CTkFrame(entrega_frame, fg_color="transparent")
                btn_frame.pack(side="right", padx=10, pady=10)
                
                if entrega.get('arquivo'):
                    ctk.CTkButton(
                        btn_frame,
                        text="📥 Baixar",
                        width=100,
                        height=35,
                        command=lambda e=entrega: self.baixar_entrega(e)
                    ).pack(pady=3)
                
                btn_text = "✏️ Reavалiar" if entrega.get('nota') is not None else "✓ Avaliar"
                ctk.CTkButton(
                    btn_frame,
                    text=btn_text,
                    width=100,
                    height=35,
                    fg_color="#2CC985",
                    command=lambda e=entrega: self.avaliar_entrega(e, atividade)
                ).pack(pady=3)
        
        # TAB 2: Alunos que não entregaram
        nao_entregaram = detalhes['alunos_nao_entregaram']
        if not nao_entregaram:
            ctk.CTkLabel(
                tabs.tab("⚠️ Não Entregaram"), 
                text="✅ Todos os alunos já entregaram!", 
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#2CC985"
            ).pack(pady=20)
        else:
            for aluno in nao_entregaram:
                aluno_frame = ctk.CTkFrame(tabs.tab("⚠️ Não Entregaram"))
                aluno_frame.pack(pady=5, padx=10, fill="x")
                
                ctk.CTkLabel(
                    aluno_frame,
                    text=f"⚠️ {aluno['nome']} (RM: {aluno['rm']}) - {aluno['email']}",
                    font=ctk.CTkFont(size=14),
                    text_color="#E74C3C"
                ).pack(anchor="w", padx=20, pady=10)
        
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
        """Modal COM SCROLL para avaliar uma entrega e ver o que foi entregue"""
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Avaliar Entrega")
        dialog.geometry("700x700")  # Maior para caber tudo com scroll
        dialog.grab_set()
        
        # ===== SCROLLABLE FRAME PRINCIPAL =====
        main_scroll = ctk.CTkScrollableFrame(dialog, width=650, height=630)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title = ctk.CTkLabel(
            main_scroll,
            text=f"📝 Avaliar Entrega",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 5))
        
        # Informações do aluno
        aluno_label = ctk.CTkLabel(
            main_scroll,
            text=f"👤 {entrega['aluno_nome']} (RM: {entrega['aluno_rm']})",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        aluno_label.pack(pady=(0, 20))
        
        # Frame de informações gerais
        info_frame = ctk.CTkFrame(main_scroll)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            info_frame,
            text=f"📄 Atividade: {atividade['titulo']}",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            info_frame,
            text=f"Valor da atividade: {atividade['valor']} pontos",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w", padx=15, pady=(0, 5))
        
        ctk.CTkLabel(
            info_frame,
            text=f"📅 Entregue em: {entrega['data_entrega']}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        # ===== VISUALIZAÇÃO DO QUE FOI ENTREGUE =====
        entrega_frame = ctk.CTkFrame(main_scroll)
        entrega_frame.pack(pady=15, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(
            entrega_frame,
            text="📋 Resposta do Aluno:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        # Textbox para mostrar a resposta (somente leitura)
        resposta_text = ctk.CTkTextbox(
            entrega_frame,
            width=600,
            height=180,
            wrap="word"
        )
        resposta_text.pack(padx=15, pady=(0, 15))
        
        # Inserir resposta do aluno
        comentario = entrega.get('comentario', '')
        if comentario:
            resposta_text.insert("1.0", comentario)
        else:
            resposta_text.insert("1.0", "Sem resposta escrita.")
        resposta_text.configure(state="disabled")  # Somente leitura
        
        # Arquivo anexado
        if entrega.get('arquivo'):
            arquivo_label = ctk.CTkLabel(
                entrega_frame,
                text=f"📎 Arquivo anexado: {entrega.get('arquivo_nome', 'arquivo')}",
                font=ctk.CTkFont(size=12),
                text_color="#3498DB"
            )
            arquivo_label.pack(anchor="w", padx=15, pady=(0, 10))
            
            ctk.CTkButton(
                entrega_frame,
                text="📥 Baixar Arquivo",
                width=150,
                height=35,
                command=lambda: self.baixar_entrega(entrega)
            ).pack(anchor="w", padx=15, pady=(0, 15))
        else:
            ctk.CTkLabel(
                entrega_frame,
                text="📎 Nenhum arquivo anexado",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(anchor="w", padx=15, pady=(0, 15))
        
        # ===== FORMULÁRIO DE AVALIAÇÃO =====
        avaliacao_frame = ctk.CTkFrame(main_scroll)
        avaliacao_frame.pack(pady=15, padx=20, fill="x")
        
        # Campo de nota
        ctk.CTkLabel(
            avaliacao_frame,
            text="✏️ Nota:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        nota_entry = ctk.CTkEntry(
            avaliacao_frame,
            placeholder_text=f"0 a {atividade['valor']}",
            width=300,
            height=40
        )
        
        # Preencher nota existente se houver
        if entrega.get('nota') is not None:
            nota_entry.insert(0, str(entrega['nota']))
        
        nota_entry.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Campo de feedback
        ctk.CTkLabel(
            avaliacao_frame,
            text="💬 Feedback para o aluno:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        feedback_text = ctk.CTkTextbox(
            avaliacao_frame,
            width=600,
            height=120
        )
        
        # Preencher feedback existente se houver
        if entrega.get('feedback'):
            feedback_text.insert("1.0", entrega['feedback'])
        
        feedback_text.pack(padx=15, pady=(0, 20))
        
        # Função para salvar avaliação
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
                messagebox.showerror("Erro", "Nota inválida! Use apenas números.")
                return
            
            from backend.turmas_backend import avaliar_entrega
            sucesso = avaliar_entrega(entrega['id'], nota_float, feedback)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Avaliação salva com sucesso!")
                dialog.destroy()
                self.show_entregas_atividade(atividade)
            else:
                messagebox.showerror("Erro", "Erro ao salvar avaliação!")
        
        # Botão de salvar
        ctk.CTkButton(
            main_scroll,
            text="💾 Salvar Avaliação",
            command=salvar_avaliacao,
            width=250,
            height=50,
            fg_color="#2CC985",
            hover_color="#25A066",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=25)
    
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
        
        ctk.CTkButton(
            dialog, 
            text="💾 Salvar Avaliação", 
            command=salvar_avaliacao, 
            width=200, 
            fg_color="#2CC985"
        ).pack(pady=10)
    
    def baixar_entrega(self, entrega):
        """Baixa o arquivo da entrega"""
        if entrega.get('arquivo'):
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=os.path.basename(entrega['arquivo']),
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
        """Mostra o boletim completo da turma com status de aprovação"""
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
            
            # Nome e RM
            ctk.CTkLabel(
                aluno_frame,
                text=f"👤 {aluno_data['nome']} (RM: {aluno_data['rm']})",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", padx=20, pady=(10, 5))
            
            # Média, frequência e status
            media = aluno_data['media'] if aluno_data['media'] else 0
            frequencia = aluno_data['frequencia']
            status = aluno_data.get('status', 'Sem notas')
            
            # Cores baseadas no status
            if status == 'Aprovado':
                status_color = "#2CC985"
                status_icon = "✅"
            elif 'Reprovado' in status:
                status_color = "#E74C3C"
                status_icon = "❌"
            else:
                status_color = "gray"
                status_icon = "⏳"
            
            ctk.CTkLabel(
                aluno_frame,
                text=f"Média: {media:.2f} | Frequência: {frequencia:.1f}% | {status_icon} {status}",
                font=ctk.CTkFont(size=13, weight="bold"),
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
    
    def show_criar_atividade(self, turma=None):
        """Modal para criar uma nova atividade"""
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Criar Nova Atividade")
        dialog.geometry("750x650")
        dialog.grab_set()
        
        main_scroll = ctk.CTkScrollableFrame(dialog, width=700, height=580)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(
            main_scroll,
            text="➕ Criar Nova Atividade",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        form_frame = ctk.CTkFrame(main_scroll)
        form_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Seleção de turma
        ctk.CTkLabel(
            form_frame,
            text="Turma:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        from backend.turmas_backend import get_turmas_professor
        turmas = get_turmas_professor(self.user_email)
        
        turma_var = ctk.StringVar()
        turma_options = [f"{t['nome']} - {t['disciplina']}" for t in turmas]
        turma_map = {f"{t['nome']} - {t['disciplina']}": t for t in turmas}
        
        if turma:
            turma_var.set(f"{turma['nome']} - {turma['disciplina']}")
        elif turmas:
            turma_var.set(turma_options[0])
        
        turma_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=turma_var,
            values=turma_options,
            width=600,
            height=40
        )
        turma_menu.pack(padx=20, pady=(0, 15))
        
        # Título
        ctk.CTkLabel(
            form_frame,
            text="Título da Atividade:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        titulo_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Trabalho sobre Funções Quadráticas",
            width=600,
            height=40
        )
        titulo_entry.pack(padx=20, pady=(0, 15))
        
        # Descrição
        ctk.CTkLabel(
            form_frame,
            text="Descrição:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        descricao_text = ctk.CTkTextbox(
            form_frame,
            width=600,
            height=120
        )
        descricao_text.pack(padx=20, pady=(0, 15))
        
        # Data de entrega
        ctk.CTkLabel(
            form_frame,
            text="Data de Entrega:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        from datetime import timedelta
        data_sugerida = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
        
        data_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="DD/MM/AAAA",
            width=600,
            height=40
        )
        data_entry.insert(0, data_sugerida)
        data_entry.pack(padx=20, pady=(0, 15))
        
        # Valor (pontuação)
        ctk.CTkLabel(
            form_frame,
            text="Valor (pontos):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        valor_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: 10",
            width=600,
            height=40
        )
        valor_entry.pack(padx=20, pady=(0, 15))
        
        # Arquivo opcional
        arquivo_path = None
        arquivo_label = ctk.CTkLabel(
            form_frame,
            text="Nenhum arquivo selecionado",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        
        def selecionar_arquivo():
            nonlocal arquivo_path
            path = filedialog.askopenfilename(
                title="Selecionar arquivo",
                filetypes=[
                    ("Todos os arquivos", "*.*"),
                    ("PDF", "*.pdf"),
                    ("Word", "*.docx"),
                    ("Imagens", "*.png *.jpg *.jpeg")
                ]
            )
            if path:
                arquivo_path = path
                arquivo_label.configure(text=f"Arquivo: {os.path.basename(path)}")
        
        ctk.CTkButton(
            form_frame,
            text="📎 Anexar Arquivo (opcional)",
            command=selecionar_arquivo,
            width=200,
            height=40,
            fg_color="#95A5A6",
            hover_color="#7F8C8D"
        ).pack(pady=(10, 5))
        
        arquivo_label.pack(pady=(0, 15))
        
        # Função para salvar
        def salvar_atividade():
            turma_selecionada = turma_map.get(turma_var.get())
            if not turma_selecionada:
                messagebox.showerror("Erro", "Selecione uma turma!")
                return
            
            titulo = titulo_entry.get().strip()
            descricao = descricao_text.get("1.0", "end-1c").strip()
            data_entrega = data_entry.get().strip()
            valor = valor_entry.get().strip()
            
            if not all([titulo, descricao, data_entrega, valor]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            try:
                valor_float = float(valor)
                if valor_float <= 0:
                    messagebox.showerror("Erro", "O valor deve ser maior que zero!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
                return
            
            from backend.turmas_backend import criar_atividade
            atividade_id = criar_atividade(
                turma_selecionada['id'],
                titulo,
                descricao,
                data_entrega,
                valor_float,
                arquivo_path
            )
            
            if atividade_id:
                messagebox.showinfo("Sucesso", "Atividade criada com sucesso!")
                dialog.destroy()
                self.show_atividades_professor()
            else:
                messagebox.showerror("Erro", "Erro ao criar atividade!")
        
        # Botão de criar
        ctk.CTkButton(
            main_scroll,
            text="✓ Criar Atividade",
            command=salvar_atividade,
            width=200,
            height=45,
            fg_color="#2CC985",
            hover_color="#25A066"
        ).pack(pady=20)
    
    def darken_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"