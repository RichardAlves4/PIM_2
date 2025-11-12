import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime

class TelaRegistroAulas:
    """Tela para registro de aulas ministradas"""
    
    def __init__(self, app, user_email):
        self.app = app
        self.user_email = user_email
    
    def show_registro_aulas(self):
        """Exibe a tela principal de registro de aulas"""
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📝 Registro de Aulas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Botão para registrar nova aula
        new_btn = ctk.CTkButton(
            main_frame,
            text="➕ Registrar Nova Aula",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=300,
            height=50,
            command=self.show_nova_aula,
            fg_color="#2CC985",
            hover_color="#25A066"
        )
        new_btn.pack(pady=20)
        
        # Listar turmas do professor
        from backend.turmas_backend import get_turmas_professor
        turmas = get_turmas_professor(self.user_email)
        
        if not turmas:
            empty_label = ctk.CTkLabel(
                main_frame,
                text="Você ainda não possui turmas cadastradas.",
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
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"📖 {turma['nome']}",
                    font=ctk.CTkFont(size=18, weight="bold")
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"Disciplina: {turma['disciplina']} | Período: {turma['periodo']}",
                    font=ctk.CTkFont(size=13),
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                # Contar aulas
                from backend.turmas_backend import get_aulas_turma
                aulas = get_aulas_turma(turma['id'])
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"Total de aulas: {len(aulas)}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                buttons_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                buttons_frame.pack(side="right", padx=10, pady=10)
                
                ctk.CTkButton(
                    buttons_frame,
                    text="Ver Aulas",
                    width=120,
                    height=35,
                    command=lambda t=turma: self.show_aulas_turma(t)
                ).pack(pady=3)
                
                ctk.CTkButton(
                    buttons_frame,
                    text="➕ Nova Aula",
                    width=120,
                    height=35,
                    fg_color="#2CC985",
                    hover_color="#25A066",
                    command=lambda t=turma: self.show_nova_aula(t)
                ).pack(pady=3)
        
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.voltar_menu,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    def show_nova_aula(self, turma=None):
        """Modal para registrar uma nova aula"""
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Registrar Nova Aula")
        dialog.geometry("700x600")
        dialog.grab_set()
        
        title = ctk.CTkLabel(
            dialog,
            text="📝 Registrar Nova Aula",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        form_frame = ctk.CTkFrame(dialog)
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
        
        # Data da aula
        ctk.CTkLabel(
            form_frame,
            text="Data da Aula:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        data_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text=datetime.now().strftime("%d/%m/%Y"),
            width=600,
            height=40
        )
        data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        data_entry.pack(padx=20, pady=(0, 15))
        
        # Título da aula
        ctk.CTkLabel(
            form_frame,
            text="Título da Aula:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        titulo_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Introdução à Álgebra Linear",
            width=600,
            height=40
        )
        titulo_entry.pack(padx=20, pady=(0, 15))
        
        # Conteúdo/descrição
        ctk.CTkLabel(
            form_frame,
            text="Conteúdo da Aula:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        conteudo_text = ctk.CTkTextbox(
            form_frame,
            width=600,
            height=150
        )
        conteudo_text.pack(padx=20, pady=(0, 15))
        
        # Observações
        ctk.CTkLabel(
            form_frame,
            text="Observações (opcional):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        observacoes_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Prova na próxima aula",
            width=600,
            height=40
        )
        observacoes_entry.pack(padx=20, pady=(0, 15))
        
        def salvar_aula():
            turma_selecionada = turma_map.get(turma_var.get())
            if not turma_selecionada:
                messagebox.showerror("Erro", "Selecione uma turma!")
                return
            
            data = data_entry.get().strip()
            titulo = titulo_entry.get().strip()
            conteudo = conteudo_text.get("1.0", "end-1c").strip()
            observacoes = observacoes_entry.get().strip()
            
            if not all([data, titulo, conteudo]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            from backend.turmas_backend import registrar_aula
            aula_id = registrar_aula(
                turma_selecionada['id'],
                titulo,
                conteudo,
                data,
                observacoes
            )
            
            if aula_id:
                # Perguntar se deseja fazer chamada agora
                fazer_chamada = messagebox.askyesno(
                    "Aula Registrada",
                    "Aula registrada com sucesso!\n\nDeseja fazer a chamada agora?",
                    icon='question'
                )
                
                dialog.destroy()
                
                if fazer_chamada:
                    self.show_chamada(aula_id, turma_selecionada)
                else:
                    messagebox.showinfo("Sucesso", "Aula registrada com sucesso!")
                    self.show_registro_aulas()
            else:
                messagebox.showerror("Erro", "Erro ao registrar aula!")
        
        ctk.CTkButton(
            dialog,
            text="✓ Salvar Aula",
            command=salvar_aula,
            width=200,
            height=45,
            fg_color="#2CC985",
            hover_color="#25A066"
        ).pack(pady=20)
    
    def show_aulas_turma(self, turma):
        """Exibe todas as aulas de uma turma"""
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📝 Aulas: {turma['nome']}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text=f"{turma['disciplina']} | {turma['periodo']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 30))
        
        from backend.turmas_backend import get_aulas_turma
        aulas = get_aulas_turma(turma['id'])
        
        if not aulas:
            empty_label = ctk.CTkLabel(
                main_frame,
                text="Nenhuma aula registrada ainda.",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            for aula in aulas:
                aula_frame = ctk.CTkFrame(main_frame)
                aula_frame.pack(pady=10, padx=40, fill="x")
                
                info_frame = ctk.CTkFrame(aula_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"📅 {aula['data']} - {aula['titulo']}",
                    font=ctk.CTkFont(size=16, weight="bold")
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=aula['conteudo'][:100] + "..." if len(aula['conteudo']) > 100 else aula['conteudo'],
                    font=ctk.CTkFont(size=13),
                    text_color="gray",
                    wraplength=600,
                    justify="left"
                ).pack(anchor="w", pady=(5, 2))
                
                if aula.get('observacoes'):
                    ctk.CTkLabel(
                        info_frame,
                        text=f"Obs: {aula['observacoes']}",
                        font=ctk.CTkFont(size=12),
                        text_color="#E67E22"
                    ).pack(anchor="w", pady=2)
                
                # Verificar se tem chamada
                from backend.turmas_backend import get_frequencia_aula
                frequencia = get_frequencia_aula(aula['id'])
                
                if frequencia:
                    total_alunos = len(frequencia)
                    presentes = sum(1 for p in frequencia.values() if p)
                    ctk.CTkLabel(
                        info_frame,
                        text=f"✓ Chamada feita: {presentes}/{total_alunos} presentes",
                        font=ctk.CTkFont(size=12),
                        text_color="#2CC985"
                    ).pack(anchor="w", pady=2)
                else:
                    ctk.CTkLabel(
                        info_frame,
                        text="⚠ Chamada não realizada",
                        font=ctk.CTkFont(size=12),
                        text_color="#E74C3C"
                    ).pack(anchor="w", pady=2)
                
                buttons_frame = ctk.CTkFrame(aula_frame, fg_color="transparent")
                buttons_frame.pack(side="right", padx=10, pady=10)
                
                if not frequencia:
                    ctk.CTkButton(
                        buttons_frame,
                        text="✓ Fazer Chamada",
                        width=130,
                        height=35,
                        fg_color="#2CC985",
                        hover_color="#25A066",
                        command=lambda a=aula, t=turma: self.show_chamada(a['id'], t)
                    ).pack(pady=3)
                else:
                    ctk.CTkButton(
                        buttons_frame,
                        text="Ver Chamada",
                        width=130,
                        height=35,
                        command=lambda a=aula, t=turma: self.show_ver_chamada(a, t)
                    ).pack(pady=3)
                
                ctk.CTkButton(
                    buttons_frame,
                    text="Editar",
                    width=130,
                    height=35,
                    fg_color="#9B59B6",
                    hover_color="#7D3C98",
                    command=lambda a=aula: self.show_editar_aula(a, turma)
                ).pack(pady=3)
        
        # Botão para nova aula
        new_btn = ctk.CTkButton(
            main_frame,
            text="➕ Registrar Nova Aula",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=300,
            height=50,
            command=lambda: self.show_nova_aula(turma),
            fg_color="#2CC985",
            hover_color="#25A066"
        )
        new_btn.pack(pady=20)
        
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_registro_aulas,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=10)
    
    def show_chamada(self, aula_id, turma):
        """Tela para fazer chamada"""
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Fazer Chamada")
        dialog.geometry("600x700")
        dialog.grab_set()
        
        title = ctk.CTkLabel(
            dialog,
            text=f"✓ Chamada - {turma['nome']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        # Frame scrollable para lista de alunos
        scroll_frame = ctk.CTkScrollableFrame(dialog, width=550, height=500)
        scroll_frame.pack(pady=10, padx=20)
        
        from backend.turmas_backend import get_alunos_turma
        alunos = get_alunos_turma(turma['id'])
        
        if not alunos:
            ctk.CTkLabel(
                scroll_frame,
                text="Nenhum aluno matriculado nesta turma.",
                text_color="gray"
            ).pack(pady=20)
            return
        
        presencas = {}
        
        for aluno in alunos:
            aluno_frame = ctk.CTkFrame(scroll_frame)
            aluno_frame.pack(pady=5, padx=10, fill="x")
            
            info_frame = ctk.CTkFrame(aluno_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text=aluno['nome'],
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            ).pack(anchor="w")
            
            if aluno.get('rm'):
                ctk.CTkLabel(
                    info_frame,
                    text=f"RM: {aluno['rm']}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray",
                    anchor="w"
                ).pack(anchor="w")
            
            # Switch para presente/ausente
            presenca_var = ctk.BooleanVar(value=True)
            presencas[aluno['email']] = presenca_var
            
            switch = ctk.CTkSwitch(
                aluno_frame,
                text="Presente",
                variable=presenca_var,
                onvalue=True,
                offvalue=False,
                progress_color="#2CC985"
            )
            switch.pack(side="right", padx=15, pady=10)
        
        def salvar_chamada():
            presencas_dict = {email: var.get() for email, var in presencas.items()}
            
            from backend.turmas_backend import registrar_chamada
            sucesso = registrar_chamada(aula_id, presencas_dict)
            
            if sucesso:
                presentes = sum(1 for p in presencas_dict.values() if p)
                total = len(presencas_dict)
                messagebox.showinfo(
                    "Sucesso",
                    f"Chamada registrada com sucesso!\n\nPresentes: {presentes}/{total}"
                )
                dialog.destroy()
                self.show_registro_aulas()
            else:
                messagebox.showerror("Erro", "Erro ao registrar chamada!")
        
        ctk.CTkButton(
            dialog,
            text="✓ Salvar Chamada",
            command=salvar_chamada,
            width=200,
            height=45,
            fg_color="#2CC985",
            hover_color="#25A066"
        ).pack(pady=20)
    
    def show_ver_chamada(self, aula, turma):
        """Visualiza a chamada de uma aula"""
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Visualizar Chamada")
        dialog.geometry("600x700")
        dialog.grab_set()
        
        title = ctk.CTkLabel(
            dialog,
            text=f"📋 Chamada - {aula['titulo']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        ctk.CTkLabel(
            dialog,
            text=f"Data: {aula['data']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
        from backend.turmas_backend import get_frequencia_aula, get_alunos_turma
        frequencia = get_frequencia_aula(aula['id'])
        alunos = get_alunos_turma(turma['id'])
        
        # Estatísticas
        total = len(alunos)
        presentes = sum(1 for p in frequencia.values() if p)
        ausentes = total - presentes
        percentual = (presentes / total * 100) if total > 0 else 0
        
        stats_frame = ctk.CTkFrame(dialog)
        stats_frame.pack(pady=20, padx=40, fill="x")
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Presentes: {presentes} | Ausentes: {ausentes} | Total: {total}",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Frequência: {percentual:.1f}%",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2CC985" if percentual >= 75 else "#E74C3C"
        ).pack(pady=5)
        
        # Lista de alunos
        scroll_frame = ctk.CTkScrollableFrame(dialog, width=550, height=400)
        scroll_frame.pack(pady=10, padx=20)
        
        for aluno in alunos:
            presente = frequencia.get(aluno['email'], False)
            
            aluno_frame = ctk.CTkFrame(scroll_frame)
            aluno_frame.pack(pady=5, padx=10, fill="x")
            
            info_frame = ctk.CTkFrame(aluno_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text=aluno['nome'],
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            ).pack(anchor="w")
            
            if aluno.get('rm'):
                ctk.CTkLabel(
                    info_frame,
                    text=f"RM: {aluno['rm']}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray",
                    anchor="w"
                ).pack(anchor="w")
            
            status_label = ctk.CTkLabel(
                aluno_frame,
                text="✓ Presente" if presente else "✗ Ausente",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#2CC985" if presente else "#E74C3C"
            )
            status_label.pack(side="right", padx=15, pady=10)
        
        ctk.CTkButton(
            dialog,
            text="Fechar",
            command=dialog.destroy,
            width=200,
            height=45,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(pady=20)
    
    def show_editar_aula(self, aula, turma):
        """Modal para editar aula"""
        messagebox.showinfo("Em desenvolvimento", "Funcionalidade de edição de aula em desenvolvimento!")
    
    def voltar_menu(self):
        """Volta para o menu do professor"""
        from screens.telas_professor import TelasProfessor
        telas = TelasProfessor(self.app, self.user_email)
        telas.show_professor_menu()