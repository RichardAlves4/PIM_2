import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
from backend.turmas_backend import get_turmas_aluno, get_atividades_turma
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class TelasAluno:
    
    def __init__(self, app, user_email):
        self.app = app
        self.user_email = user_email
    
    def show_aluno_menu(self):
        self.app.clear_window()

        scroll_container = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        main_frame = ctk.CTkFrame(scroll_container, corner_radius=0)
        main_frame.pack(padx=20, pady=20, fill="x")

        from backend.turmas_backend import get_user_data
        from database.banco import users_db
        user_data = users_db.get(self.user_email, get_user_data(self.user_email))
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=20, pady=(20, 30))
        title_label = ctk.CTkLabel(header_frame, text=f"👨‍🎓 Bem-vindo, {user_data['nome']}!", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=10)
        if user_data.get('rm'):
            rm_label = ctk.CTkLabel(header_frame, text=f"RM: {user_data['rm']}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#3498DB")
            rm_label.pack(pady=5)
        subtitle_label = ctk.CTkLabel(header_frame, text=f"Email: {self.user_email}", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle_label.pack()
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)
        buttons_data = [
            ("📚 Turmas", self.show_turmas_aluno, "#3498DB"),
            ("📋 Atividades Pendentes", self.show_atividades_pendentes, "#E67E22"),
            ("✅ Atividades Concluídas", self.show_atividades_entregues, "#2CC985"),
            ("📊 Boletim Escolar", self.show_boletim_completo, "#9B59B6"),
            ("🚪 Sair", lambda: self.app.logout(), "#E74C3C")
        ]
        for text, command, color in buttons_data:
            btn = ctk.CTkButton(buttons_frame, text=text, font=ctk.CTkFont(size=16, weight="bold"), width=400, height=55, command=command, fg_color=color, hover_color=self.darken_color(color))
            btn.pack(pady=8)
    
    def show_turmas_aluno(self):
        self.app.clear_window()
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text="📚 Minhas Turmas", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=(20, 30))
        from backend.turmas_backend import get_turmas_aluno
        turmas = get_turmas_aluno(self.user_email)
        if not turmas:
            empty_label = ctk.CTkLabel(main_frame, text="Você ainda não está matriculado em nenhuma turma.\nAguarde seu professor adicioná-lo a uma turma!", font=ctk.CTkFont(size=16), text_color="gray")
            empty_label.pack(pady=50)
        else:
            for turma in turmas:
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=10, padx=40, fill="x")
                info_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                nome_label = ctk.CTkLabel(info_frame, text=f"📖 {turma['nome']}", font=ctk.CTkFont(size=18, weight="bold"))
                nome_label.pack(anchor="w")
                disciplina_label = ctk.CTkLabel(info_frame, text=f"Disciplina: {turma['disciplina']}", font=ctk.CTkFont(size=14), text_color="gray")
                disciplina_label.pack(anchor="w", pady=2)
                professor_label = ctk.CTkLabel(info_frame, text=f"Professor: {turma['professor_nome']} | {turma['periodo']}", font=ctk.CTkFont(size=12), text_color="gray")
                professor_label.pack(anchor="w", pady=2)
                view_btn = ctk.CTkButton(turma_frame, text="Ver Detalhes", width=120, height=40, command=lambda t=turma: self.show_detalhes_turma_aluno(t))
                view_btn.pack(side="right", padx=10, pady=10)
        back_btn = ctk.CTkButton(main_frame, text="← Voltar", font=ctk.CTkFont(size=16), width=200, height=50, command=self.show_aluno_menu, fg_color="gray", hover_color="darkgray")
        back_btn.pack(pady=30)
    
    def show_detalhes_turma_aluno(self, turma):
        self.app.clear_window()
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text=f"📖 {turma['nome']}", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=(20, 10))
        info_label = ctk.CTkLabel(main_frame, text=f"{turma['disciplina']} | Prof. {turma['professor_nome']} | {turma['periodo']}", font=ctk.CTkFont(size=14), text_color="gray")
        info_label.pack(pady=(0, 30))
        tabs = ctk.CTkTabview(main_frame, width=800, height=400)
        tabs.pack(pady=20, padx=40)
        tabs.add("📝 Aulas Ministradas")
        tabs.add("📋 Atividades")
        tabs.add("📊 Minhas Notas")
        from backend.turmas_backend import get_aulas_turma, get_atividades_turma_aluno, get_notas_aluno_turma
        aulas = get_aulas_turma(turma['id'])
        if not aulas:
            ctk.CTkLabel(tabs.tab("📝 Aulas Ministradas"), text="Nenhuma aula registrada ainda.", text_color="gray").pack(pady=20)
        else:
            for aula in aulas:
                aula_frame = ctk.CTkFrame(tabs.tab("📝 Aulas Ministradas"))
                aula_frame.pack(pady=5, padx=10, fill="x")
                ctk.CTkLabel(aula_frame, text=f"📅 {aula['data']} - {aula['titulo']}", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
                ctk.CTkLabel(aula_frame, text=aula['conteudo'], font=ctk.CTkFont(size=12), text_color="gray", wraplength=700, justify="left").pack(anchor="w", padx=20, pady=(2, 10))
        atividades = get_atividades_turma_aluno(turma['id'], self.user_email)
        if not atividades:
            ctk.CTkLabel(tabs.tab("📋 Atividades"), text="Nenhuma atividade disponível.", text_color="gray").pack(pady=20)
        else:
            for atividade in atividades:
                ativ_frame = ctk.CTkFrame(tabs.tab("📋 Atividades"))
                ativ_frame.pack(pady=5, padx=10, fill="x")
                info_frame = ctk.CTkFrame(ativ_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=10)
                status_icon = "✅" if atividade['entregue'] else "⏰"
                ctk.CTkLabel(info_frame, text=f"{status_icon} {atividade['titulo']}", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
                ctk.CTkLabel(info_frame, text=f"Prazo: {atividade['data_entrega']} | Valor: {atividade['valor']} pontos", font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w", pady=2)
                if atividade['entregue']:
                    if atividade.get('nota'):
                        ctk.CTkLabel(info_frame, text=f"Nota: {atividade['nota']}/{atividade['valor']}", font=ctk.CTkFont(size=12, weight="bold"), text_color="#2CC985").pack(anchor="w", pady=2)
                    else:
                        ctk.CTkLabel(info_frame, text="Aguardando correção", font=ctk.CTkFont(size=12), text_color="#E67E22").pack(anchor="w", pady=2)
                    ctk.CTkButton(ativ_frame, text="Ver Entrega", width=100, height=30, command=lambda a=atividade: self.show_ver_entrega(a)).pack(side="right", padx=5, pady=5)
                else:
                    ctk.CTkButton(ativ_frame, text="Entregar", width=100, height=30, fg_color="#2CC985", hover_color="#25A066", command=lambda a=atividade: self.show_entregar_atividade(a)).pack(side="right", padx=5, pady=5)
        notas = get_notas_aluno_turma(turma['id'], self.user_email)
        if not notas:
            ctk.CTkLabel(tabs.tab("📊 Minhas Notas"), text="Nenhuma nota disponível ainda.", text_color="gray").pack(pady=20)
        else:
            media = sum([nota['nota'] for nota in notas]) / sum([nota['valor'] for nota in notas]) * 10 if notas else 0
            media_label = ctk.CTkLabel(tabs.tab("📊 Minhas Notas"), text=f"📊 Média: {media:.2f}", font=ctk.CTkFont(size=18, weight="bold"), text_color="#2CC985" if media >= 7 else "#E74C3C")
            media_label.pack(pady=20)
            for nota in notas:
                nota_frame = ctk.CTkFrame(tabs.tab("📊 Minhas Notas"))
                nota_frame.pack(pady=5, padx=10, fill="x")
                ctk.CTkLabel(nota_frame, text=f"📝 {nota['atividade']}: {nota['nota']}/{nota['valor']}", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20, pady=10)
        back_btn = ctk.CTkButton(main_frame, text="← Voltar", font=ctk.CTkFont(size=16), width=200, height=50, command=self.show_turmas_aluno, fg_color="gray", hover_color="darkgray")
        back_btn.pack(pady=30)
    
    def show_entregar_atividade(self, atividade):
        self.app.clear_window()
        
        # ADICIONAR SCROLLABLE FRAME
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(main_frame, text=f"📤 Entregar: {atividade['titulo']}", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 10))
        info_label = ctk.CTkLabel(main_frame, text=f"Prazo: {atividade['data_entrega']} | Valor: {atividade['valor']} pontos", font=ctk.CTkFont(size=14), text_color="gray")
        info_label.pack(pady=(0, 20))
        desc_frame = ctk.CTkFrame(main_frame)
        desc_frame.pack(pady=10, padx=50, fill="both", expand=True)
        ctk.CTkLabel(desc_frame, text="Descrição da Atividade:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        desc_text = ctk.CTkTextbox(desc_frame, height=100, state="normal")
        desc_text.pack(pady=5, padx=20, fill="x")
        desc_text.insert("1.0", atividade['descricao'])
        desc_text.configure(state="disabled")
        ctk.CTkLabel(desc_frame, text="Sua Resposta:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        resposta_text = ctk.CTkTextbox(desc_frame, height=150)
        resposta_text.pack(pady=5, padx=20, fill="both", expand=True)
        file_label = ctk.CTkLabel(desc_frame, text="Nenhum arquivo selecionado", font=ctk.CTkFont(size=12), text_color="gray")
        file_label.pack(pady=10)
        selected_file = {"path": None}
        def select_file():
            filepath = filedialog.askopenfilename(title="Selecionar Arquivo", filetypes=[("Todos os arquivos", "*.*"), ("PDFs", "*.pdf"), ("Documentos", "*.doc;*.docx"), ("Imagens", "*.png;*.jpg;*.jpeg")])
            if filepath:
                selected_file["path"] = filepath
                file_label.configure(text=f"Arquivo: {filepath.split('/')[-1]}")
        file_btn = ctk.CTkButton(desc_frame, text="📎 Anexar Arquivo (Opcional)", width=200, command=select_file)
        file_btn.pack(pady=10)
        def process_entrega():
            resposta = resposta_text.get("1.0", "end-1c").strip()
            if not resposta and not selected_file["path"]:
                messagebox.showerror("Erro", "Você precisa escrever uma resposta ou anexar um arquivo!")
                return
            from backend.turmas_backend import entregar_atividade
            sucesso, mensagem = entregar_atividade(atividade['id'], self.user_email, selected_file["path"], resposta)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.show_atividades_pendentes()
            else:
                messagebox.showerror("Erro", mensagem)
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        submit_btn = ctk.CTkButton(buttons_frame, text="✓ Entregar", font=ctk.CTkFont(size=16, weight="bold"), width=190, height=50, command=process_entrega, fg_color="#2CC985", hover_color="#25A066")
        submit_btn.pack(side="left", padx=10)
        cancel_btn = ctk.CTkButton(buttons_frame, text="← Cancelar", font=ctk.CTkFont(size=16), width=190, height=50, command=self.show_atividades_pendentes, fg_color="gray", hover_color="darkgray")
        cancel_btn.pack(side="left", padx=10)
    
    def show_ver_entrega(self, atividade):
        self.app.clear_window()
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text=f"📄 {atividade['titulo']}", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 10))
        info_label = ctk.CTkLabel(main_frame, text=f"Entregue em: {atividade['data_entrega']}", font=ctk.CTkFont(size=14), text_color="gray")
        info_label.pack(pady=(0, 20))
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(pady=10, padx=50, fill="both", expand=True)
        ctk.CTkLabel(content_frame, text="Sua Resposta:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        resposta_text = ctk.CTkTextbox(content_frame, height=150, state="normal")
        resposta_text.pack(pady=5, padx=20, fill="both", expand=True)
        resposta_text.insert("1.0", atividade.get('comentario', 'Nenhuma resposta escrita'))
        resposta_text.configure(state="disabled")
        if atividade.get('arquivo'):
            ctk.CTkLabel(content_frame, text=f"📎 Arquivo anexado: {atividade.get('arquivo_nome', 'arquivo')}", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=10)
        if atividade.get('nota'):
            nota_frame = ctk.CTkFrame(content_frame, fg_color="#2CC985")
            nota_frame.pack(pady=20, padx=20, fill="x")
            ctk.CTkLabel(nota_frame, text=f"⭐ Nota: {atividade['nota']}/{atividade['valor']}", font=ctk.CTkFont(size=18, weight="bold"), text_color="white").pack(pady=15)
            if atividade.get('feedback'):
                ctk.CTkLabel(content_frame, text="Feedback do Professor:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
                feedback_text = ctk.CTkTextbox(content_frame, height=100, state="normal")
                feedback_text.pack(pady=5, padx=20, fill="x")
                feedback_text.insert("1.0", atividade['feedback'])
                feedback_text.configure(state="disabled")
        else:
            status_frame = ctk.CTkFrame(content_frame, fg_color="#E67E22")
            status_frame.pack(pady=20, padx=20, fill="x")
            ctk.CTkLabel(status_frame, text="⏳ Aguardando Correção", font=ctk.CTkFont(size=16, weight="bold"), text_color="white").pack(pady=15)
        back_btn = ctk.CTkButton(main_frame, text="← Voltar", font=ctk.CTkFont(size=16), width=200, height=50, command=self.show_atividades_entregues, fg_color="gray", hover_color="darkgray")
        back_btn.pack(pady=30)
    
    def show_atividades_pendentes(self):
        self.app.clear_window()
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text="📋 Atividades Pendentes", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=(20, 30))

        turmas = get_turmas_aluno(self.user_email)
        from backend.turmas_backend import carregar_json, ENTREGAS_FILE
        entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})

        atividades = []
        for turma in turmas:
            atividades_turma = get_atividades_turma(turma['id'])
            for atividade in atividades_turma:
                ja_entregou = False
                for entrega in entregas.values():
                    if (entrega.get('atividade_id') == atividade['id'] and 
                        entrega.get('aluno_email') == self.user_email):
                        ja_entregou = True
                        break
                
                if not ja_entregou:
                    ativ_copy = atividade.copy()
                    ativ_copy['turma_nome'] = turma['nome']
                    ativ_copy['disciplina'] = turma['disciplina']
                    atividades.append(ativ_copy)
        if not atividades:
            empty_label = ctk.CTkLabel(main_frame, text="Parabéns! Você não possui atividades pendentes. 🎉", font=ctk.CTkFont(size=16), text_color="gray")
            empty_label.pack(pady=50)
        else:
            for atividade in atividades:
                ativ_frame = ctk.CTkFrame(main_frame)
                ativ_frame.pack(pady=10, padx=40, fill="x")
                info_frame = ctk.CTkFrame(ativ_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                ctk.CTkLabel(info_frame, text=f"⏰ {atividade['titulo']}", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
                ctk.CTkLabel(info_frame, text=f"Turma: {atividade.get('turma_nome', 'N/A')} | Prazo: {atividade['data_entrega']}", font=ctk.CTkFont(size=13), text_color="gray").pack(anchor="w", pady=2)
                ctk.CTkLabel(info_frame, text=f"Valor: {atividade['valor']} pontos", font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w", pady=2)
                ctk.CTkButton(ativ_frame, text="Entregar", width=120, height=35, fg_color="#2CC985", hover_color="#25A066", command=lambda a=atividade: self.show_entregar_atividade(a)).pack(side="right", padx=10, pady=10)
        back_btn = ctk.CTkButton(main_frame, text="← Voltar", font=ctk.CTkFont(size=16), width=200, height=50, command=self.show_aluno_menu, fg_color="gray", hover_color="darkgray")
        back_btn.pack(pady=30)
    
    def show_atividades_entregues(self):
        self.app.clear_window()
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text="✅ Atividades Concluídas", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=(20, 30))
        from backend.turmas_backend import get_atividades_entregues_aluno
        atividades = get_atividades_entregues_aluno(self.user_email)
        if not atividades:
            empty_label = ctk.CTkLabel(main_frame, text="Você ainda não entregou nenhuma atividade.", font=ctk.CTkFont(size=16), text_color="gray")
            empty_label.pack(pady=50)
        else:
            for atividade in atividades:
                ativ_frame = ctk.CTkFrame(main_frame)
                ativ_frame.pack(pady=10, padx=40, fill="x")
                info_frame = ctk.CTkFrame(ativ_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                ctk.CTkLabel(info_frame, text=f"✅ {atividade['titulo']}", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
                ctk.CTkLabel(info_frame, text=f"Turma: {atividade['turma']} | Entregue em: {atividade['data_entrega']}", font=ctk.CTkFont(size=13), text_color="gray").pack(anchor="w", pady=2)
                if atividade.get('nota'):
                    ctk.CTkLabel(info_frame, text=f"Nota: {atividade['nota']}/{atividade['valor']}", font=ctk.CTkFont(size=13, weight="bold"), text_color="#2CC985").pack(anchor="w", pady=2)
                else:
                    ctk.CTkLabel(info_frame, text="Aguardando correção", font=ctk.CTkFont(size=12), text_color="#E67E22").pack(anchor="w", pady=2)
                ctk.CTkButton(ativ_frame, text="Ver Detalhes", width=120, height=35, command=lambda a=atividade: self.show_ver_entrega(a)).pack(side="right", padx=10, pady=10)
        back_btn = ctk.CTkButton(main_frame, text="← Voltar", font=ctk.CTkFont(size=16), width=200, height=50, command=self.show_aluno_menu, fg_color="gray", hover_color="darkgray")
        back_btn.pack(pady=30)
    
    def show_boletim_completo(self):
        self.app.clear_window()
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(main_frame, text="📊 Boletim Escolar", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=(20, 30))
        from backend.turmas_backend import get_boletim_aluno
        from database.banco import users_db
        user_data = users_db.get(self.user_email, {})
        boletim = get_boletim_aluno(self.user_email)
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(pady=10, padx=40, fill="x")
        ctk.CTkLabel(info_frame, text=f"👨‍🎓 Aluno: {user_data.get('nome', 'N/A')}", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(info_frame, text=f"📧 Email: {self.user_email}", font=ctk.CTkFont(size=14), text_color="gray").pack(anchor="w", padx=20, pady=2)
        if user_data.get('rm'):
            ctk.CTkLabel(info_frame, text=f"🎫 RM: {user_data['rm']}", font=ctk.CTkFont(size=14), text_color="gray").pack(anchor="w", padx=20, pady=(2, 15))
        if not boletim:
            ctk.CTkLabel(main_frame, text="Você ainda não possui notas registradas.", font=ctk.CTkFont(size=16), text_color="gray").pack(pady=50)
        else:
            turmas_com_media = [t for t in boletim if t.get('media')]
            if turmas_com_media:
                media_geral = sum([turma['media'] for turma in turmas_com_media]) / len(turmas_com_media)
            else:
                media_geral = 0
            resumo_frame = ctk.CTkFrame(main_frame)
            resumo_frame.pack(pady=10, padx=40, fill="x")
            ctk.CTkLabel(resumo_frame, text=f"📊 Média Geral: {media_geral:.2f}", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2CC985" if media_geral >= 7 else "#E74C3C").pack(pady=20)
            for turma_data in boletim:
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=10, padx=40, fill="x")
                ctk.CTkLabel(turma_frame, text=f"📖 {turma_data['turma']}", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
                ctk.CTkLabel(turma_frame, text=f"Disciplina: {turma_data['disciplina']} | Professor: {turma_data['professor']}", font=ctk.CTkFont(size=13), text_color="gray").pack(anchor="w", padx=20, pady=2)
                media = turma_data['media'] if turma_data['media'] else 0
                status = "Aprovado ✓" if media >= 7 else "Reprovado ✗" if media > 0 else "Sem notas"
                status_color = "#2CC985" if media >= 7 else "#E74C3C" if media > 0 else "gray"
                ctk.CTkLabel(turma_frame, text=f"Média: {media:.2f} | Frequência: {turma_data['frequencia']}% | Status: {status}", font=ctk.CTkFont(size=14, weight="bold"), text_color=status_color).pack(anchor="w", padx=20, pady=(5, 10))
                if turma_data['notas']:
                    notas_header = ctk.CTkLabel(turma_frame, text="Notas por atividade:", font=ctk.CTkFont(size=13, weight="bold"))
                    notas_header.pack(anchor="w", padx=20, pady=(5, 5))
                    for nota in turma_data['notas']:
                        nota_line = ctk.CTkLabel(turma_frame, text=f"  • {nota['atividade']}: {nota['nota']}/{nota['valor']}", font=ctk.CTkFont(size=12), text_color="gray")
                        nota_line.pack(anchor="w", padx=40, pady=2)
                turma_frame.pack_configure(pady=(10, 15))
            if REPORTLAB_AVAILABLE:
                export_btn = ctk.CTkButton(main_frame, text="📥 Exportar Boletim (PDF)", font=ctk.CTkFont(size=16, weight="bold"), width=250, height=50, command=lambda: self.exportar_boletim_pdf(user_data, boletim), fg_color="#3498DB", hover_color="#2874A6")
                export_btn.pack(pady=20)
        back_btn = ctk.CTkButton(main_frame, text="← Voltar", font=ctk.CTkFont(size=16), width=200, height=50, command=self.show_aluno_menu, fg_color="gray", hover_color="darkgray")
        back_btn.pack(pady=30)
    
    def exportar_boletim_pdf(self, user_data, boletim):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialfile=f"Boletim_{user_data.get('rm', 'aluno')}.pdf")
            if not filename:
                return
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#3498DB'), spaceAfter=30, alignment=1)
            story.append(Paragraph("📊 BOLETIM ESCOLAR", title_style))
            story.append(Spacer(1, 0.5*cm))
            info_data = [["Aluno:", user_data.get('nome', 'N/A')], ["RM:", user_data.get('rm', 'N/A')], ["Email:", user_data.get('email', 'N/A')], ["Data:", datetime.now().strftime("%d/%m/%Y")]]
            info_table = Table(info_data, colWidths=[4*cm, 12*cm])
            info_table.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 10), ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10), ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey), ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1'))]))
            story.append(info_table)
            story.append(Spacer(1, 1*cm))
            if boletim:
                media_geral = sum([t['media'] for t in boletim if t['media']]) / len([t for t in boletim if t['media']])
                resumo_data = [["MÉDIA GERAL", f"{media_geral:.2f}"]]
                resumo_table = Table(resumo_data, colWidths=[12*cm, 4*cm])
                resumo_table.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 14), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2CC985' if media_geral >= 7 else '#E74C3C')), ('TEXTCOLOR', (0, 0), (-1, -1), colors.white), ('GRID', (0, 0), (-1, -1), 1, colors.white)]))
                story.append(resumo_table)
                story.append(Spacer(1, 0.7*cm))
                for turma_data in boletim:
                    story.append(Paragraph(f"<b>{turma_data['turma']}</b>", styles['Heading2']))
                    story.append(Spacer(1, 0.3*cm))
                    turma_info = [[f"Disciplina: {turma_data['disciplina']}", f"Professor: {turma_data['professor']}"]]
                    turma_table = Table(turma_info, colWidths=[8*cm, 8*cm])
                    turma_table.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 9), ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
                    story.append(turma_table)
                    story.append(Spacer(1, 0.3*cm))
                    media = turma_data['media'] if turma_data['media'] else 0
                    status = "Aprovado" if media >= 7 else "Reprovado" if media > 0 else "Sem notas"
                    desempenho_data = [["Média", "Frequência", "Status"], [f"{media:.2f}", f"{turma_data['frequencia']}%", status]]
                    desempenho_table = Table(desempenho_data, colWidths=[5*cm, 5*cm, 6*cm])
                    desempenho_table.setStyle(TableStyle([('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10), ('FONT', (0, 1), (-1, -1), 'Helvetica', 10), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), ('BACKGROUND', (2, 1), (2, 1), colors.HexColor('#2CC985' if media >= 7 else '#E74C3C')), ('TEXTCOLOR', (2, 1), (2, 1), colors.white if media != 0 else colors.black)]))
                    story.append(desempenho_table)
                    if turma_data['notas']:
                        story.append(Spacer(1, 0.3*cm))
                        notas_data = [["Atividade", "Nota", "Valor"]]
                        for nota in turma_data['notas']:
                            notas_data.append([nota['atividade'], str(nota['nota']), str(nota['valor'])])
                        notas_table = Table(notas_data, colWidths=[10*cm, 3*cm, 3*cm])
                        notas_table.setStyle(TableStyle([('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9), ('FONT', (0, 1), (-1, -1), 'Helvetica', 8), ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('ALIGN', (1, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ECF0F1'))]))
                        story.append(notas_table)
                    story.append(Spacer(1, 0.7*cm))
            doc.build(story)
            messagebox.showinfo("Sucesso", f"Boletim exportado com sucesso!\n{filename}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar boletim:\n{str(e)}")
    
    def darken_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"