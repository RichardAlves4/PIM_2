import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class TelasAdmin:
    
    def __init__(self, app, user_email):
        self.app = app
        self.user_email = user_email
    
    def show_admin_menu(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
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
            ("📊 Relatórios Gerais", self.show_relatorios_gerais, "#2CC985"),
            ("📈 Estatísticas do Sistema", self.show_estatisticas, "#E67E22"),
            ("🗑️ Limpeza de Dados", self.show_limpeza_dados, "#E74C3C"),
            ("⚙️ Editar Perfil", lambda: self.app.show_edit_screen(), "#95A5A6"),
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
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="👥 Gerenciar Usuários",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        filter_frame = ctk.CTkFrame(main_frame)
        filter_frame.pack(pady=10, padx=40, fill="x")
        
        filter_var = ctk.StringVar(value="TODOS")
        
        ctk.CTkLabel(filter_frame, text="Filtrar por tipo:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=20)
        
        for option in ["TODOS", "ADMIN", "INSTRUCTOR", "USER"]:
            rb = ctk.CTkRadioButton(
                filter_frame,
                text=option,
                variable=filter_var,
                value=option,
                command=lambda: self.show_gerenciar_usuarios()
            )
            rb.pack(side="left", padx=10)
        
        from backend.turmas_backend import get_todos_usuarios
        usuarios = get_todos_usuarios(filter_var.get())
        
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(pady=10, padx=40, fill="x")
        
        total = len(usuarios)
        admins = len([u for u in usuarios if u['role'] == 'ADMIN'])
        professores = len([u for u in usuarios if u['role'] == 'INSTRUCTOR'])
        alunos = len([u for u in usuarios if u['role'] == 'USER'])
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Total: {total} | Admins: {admins} | Professores: {professores} | Alunos: {alunos}",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=15)
        
        for usuario in usuarios:
            user_frame = ctk.CTkFrame(main_frame)
            user_frame.pack(pady=8, padx=40, fill="x")
            
            info_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
            
            icon = "👨‍💼" if usuario['role'] == 'ADMIN' else "👨‍🏫" if usuario['role'] == 'INSTRUCTOR' else "👨‍🎓"
            role_text = "Administrador" if usuario['role'] == 'ADMIN' else "Professor" if usuario['role'] == 'INSTRUCTOR' else "Aluno"
            
            ctk.CTkLabel(
                info_frame,
                text=f"{icon} {usuario['nome']}",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=f"Email: {usuario['email']} | Tipo: {role_text} | Idade: {usuario['idade']}",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(anchor="w", pady=2)
            
            btn_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
            btn_frame.pack(side="right", padx=10, pady=5)
            
            ctk.CTkButton(
                btn_frame,
                text="Ver Detalhes",
                width=110,
                height=35,
                command=lambda u=usuario: self.show_detalhes_usuario(u)
            ).pack(side="left", padx=3)
            
            ctk.CTkButton(
                btn_frame,
                text="Editar",
                width=90,
                height=35,
                fg_color="#9B59B6",
                hover_color="#7D3C98",
                command=lambda u=usuario: self.show_editar_usuario(u)
            ).pack(side="left", padx=3)
            
            if usuario['email'] != self.user_email:
                ctk.CTkButton(
                    btn_frame,
                    text="Excluir",
                    width=90,
                    height=35,
                    fg_color="#E74C3C",
                    hover_color="#C0392B",
                    command=lambda u=usuario: self.confirmar_excluir_usuario(u)
                ).pack(side="left", padx=3)
        
        add_btn = ctk.CTkButton(
            main_frame,
            text="➕ Adicionar Novo Usuário",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=300,
            height=50,
            command=self.show_adicionar_usuario,
            fg_color="#2CC985",
            hover_color="#25A066"
        )
        add_btn.pack(pady=20)
        
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
        back_btn.pack(pady=10)
    
    def show_detalhes_usuario(self, usuario):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Detalhes do Usuário")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        title = ctk.CTkLabel(
            dialog,
            text=f"Detalhes: {usuario['nome']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        info_frame = ctk.CTkFrame(dialog)
        info_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        from backend.turmas_backend import get_detalhes_completos_usuario
        detalhes = get_detalhes_completos_usuario(usuario['email'])
        
        dados = [
            ("Nome:", usuario['nome']),
            ("Email:", usuario['email']),
            ("Idade:", str(usuario['idade'])),
            ("Tipo:", "Administrador" if usuario['role'] == 'ADMIN' else "Professor" if usuario['role'] == 'INSTRUCTOR' else "Aluno"),
            ("Data de Cadastro:", detalhes.get('data_cadastro', 'N/A')),
        ]
        
        if usuario['role'] == 'INSTRUCTOR':
            dados.append(("Turmas Lecionando:", str(detalhes.get('total_turmas', 0))))
            dados.append(("Total de Alunos:", str(detalhes.get('total_alunos', 0))))
            dados.append(("Atividades Criadas:", str(detalhes.get('total_atividades', 0))))
        elif usuario['role'] == 'USER':
            dados.append(("Turmas Matriculado:", str(detalhes.get('total_turmas', 0))))
            dados.append(("Atividades Entregues:", str(detalhes.get('atividades_entregues', 0))))
            dados.append(("Média Geral:", f"{detalhes.get('media_geral', 0):.2f}"))
        
        for label, valor in dados:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(pady=8, padx=20, fill="x")
            
            ctk.CTkLabel(
                row_frame,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                width=180,
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
            fg_color="gray"
        ).pack(pady=20)
    
    def show_editar_usuario(self, usuario):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Editar Usuário")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text=f"Editar: {usuario['nome']}", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=20)
        
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(form_frame, text="Nome:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        nome_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        nome_entry.insert(0, usuario['nome'])
        nome_entry.pack(padx=20, pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="Idade:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        idade_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        idade_entry.insert(0, str(usuario['idade']))
        idade_entry.pack(padx=20, pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="Tipo de Usuário:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        role_var = ctk.StringVar(value=usuario['role'])
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.pack(anchor="w", padx=20, pady=(0, 15))
        
        roles = [("👨‍💼 Admin", "ADMIN"), ("👨‍🏫 Professor", "INSTRUCTOR"), ("👨‍🎓 Aluno", "USER")]
        for text, value in roles:
            rb = ctk.CTkRadioButton(role_frame, text=text, variable=role_var, value=value)
            rb.pack(side="left", padx=10)
        
        def salvar_edicao():
            novo_nome = nome_entry.get().strip()
            nova_idade = idade_entry.get().strip()
            novo_role = role_var.get()
            
            if not novo_nome or not nova_idade:
                messagebox.showerror("Erro", "Nome e idade são obrigatórios!")
                return
            
            try:
                idade_int = int(nova_idade)
                if idade_int < 7 or idade_int > 100:
                    messagebox.showerror("Erro", "Idade deve estar entre 7 e 100!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Idade inválida!")
                return
            
            from backend.turmas_backend import editar_usuario
            sucesso = editar_usuario(usuario['email'], novo_nome, idade_int, novo_role)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário editado com sucesso!")
                dialog.destroy()
                self.show_gerenciar_usuarios()
            else:
                messagebox.showerror("Erro", "Erro ao editar usuário!")
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(
            btn_frame,
            text="Salvar",
            command=salvar_edicao,
            width=180,
            fg_color="#2CC985"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=dialog.destroy,
            width=180,
            fg_color="gray"
        ).pack(side="left", padx=10)
    
    def confirmar_excluir_usuario(self, usuario):
        result = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o usuário:\n\n{usuario['nome']}\n{usuario['email']}\n\nEsta ação é IRREVERSÍVEL!",
            icon='warning'
        )
        
        if result:
            from backend.turmas_backend import excluir_usuario
            sucesso = excluir_usuario(usuario['email'])
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                self.show_gerenciar_usuarios()
            else:
                messagebox.showerror("Erro", "Erro ao excluir usuário!")
    
    def show_adicionar_usuario(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Adicionar Usuário")
        dialog.geometry("600x600")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Adicionar Novo Usuário", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=20)
        
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(form_frame, text="Nome:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        nome_entry = ctk.CTkEntry(form_frame, placeholder_text="Nome completo", width=400, height=40)
        nome_entry.pack(padx=20, pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="Email:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="email@exemplo.com", width=400, height=40)
        email_entry.pack(padx=20, pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="Idade:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        idade_entry = ctk.CTkEntry(form_frame, placeholder_text="Idade (7-100)", width=400, height=40)
        idade_entry.pack(padx=20, pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="Senha:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        senha_entry = ctk.CTkEntry(form_frame, placeholder_text="Senha", width=400, height=40, show="*")
        senha_entry.pack(padx=20, pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="Tipo de Usuário:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        role_var = ctk.StringVar(value="USER")
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.pack(anchor="w", padx=20, pady=(0, 20))
        
        roles = [("👨‍💼 Admin", "ADMIN"), ("👨‍🏫 Professor", "INSTRUCTOR"), ("👨‍🎓 Aluno", "USER")]
        for text, value in roles:
            rb = ctk.CTkRadioButton(role_frame, text=text, variable=role_var, value=value)
            rb.pack(side="left", padx=10)
        
        def adicionar():
            nome = nome_entry.get().strip()
            email = email_entry.get().strip()
            idade = idade_entry.get().strip()
            senha = senha_entry.get()
            role = role_var.get()
            
            if not all([nome, email, idade, senha]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            try:
                idade_int = int(idade)
                if idade_int < 7 or idade_int > 100:
                    messagebox.showerror("Erro", "Idade deve estar entre 7 e 100!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Idade inválida!")
                return
            
            from backend.turmas_backend import adicionar_usuario
            sucesso = adicionar_usuario(nome, email, idade_int, senha, role)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
                dialog.destroy()
                self.show_gerenciar_usuarios()
            else:
                messagebox.showerror("Erro", "Erro ao adicionar usuário! Email pode já estar cadastrado.")
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Adicionar",
            command=adicionar,
            width=180,
            fg_color="#2CC985"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=dialog.destroy,
            width=180,
            fg_color="gray"
        ).pack(side="left", padx=10)
    
    def show_gerenciar_turmas(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📚 Gerenciar Turmas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        from backend.turmas_backend import get_todas_turmas
        turmas = get_todas_turmas()
        
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(pady=10, padx=40, fill="x")
        
        total_turmas = len(turmas)
        total_alunos = sum([t['total_alunos'] for t in turmas])
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Total de Turmas: {total_turmas} | Total de Alunos Matriculados: {total_alunos}",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=15)
        
        if not turmas:
            ctk.CTkLabel(main_frame, text="Nenhuma turma cadastrada no sistema.", text_color="gray").pack(pady=50)
        else:
            for turma in turmas:
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=8, padx=40, fill="x")
                
                info_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"📖 {turma['nome']}",
                    font=ctk.CTkFont(size=16, weight="bold")
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"Disciplina: {turma['disciplina']} | Prof: {turma['professor_nome']}",
                    font=ctk.CTkFont(size=13),
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"Alunos: {turma['total_alunos']} | Ano: {turma['ano']} | {turma['periodo']}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                btn_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                btn_frame.pack(side="right", padx=10, pady=5)
                
                ctk.CTkButton(
                    btn_frame,
                    text="Ver Detalhes",
                    width=110,
                    height=35,
                    command=lambda t=turma: self.show_detalhes_turma_admin(t)
                ).pack(pady=3)
                
                ctk.CTkButton(
                    btn_frame,
                    text="Excluir",
                    width=110,
                    height=35,
                    fg_color="#E74C3C",
                    hover_color="#C0392B",
                    command=lambda t=turma: self.confirmar_excluir_turma(t)
                ).pack(pady=3)
        
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
    
    def show_detalhes_turma_admin(self, turma):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Detalhes da Turma")
        dialog.geometry("700x600")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text=f"📖 {turma['nome']}", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        from backend.turmas_backend import get_detalhes_completos_turma
        detalhes = get_detalhes_completos_turma(turma['id'])
        
        info_frame = ctk.CTkFrame(dialog)
        info_frame.pack(pady=10, padx=40, fill="x")
        
        dados = [
            ("Disciplina:", turma['disciplina']),
            ("Professor:", turma['professor_nome']),
            ("Ano Letivo:", turma['ano']),
            ("Período:", turma['periodo']),
            ("Total de Alunos:", str(turma['total_alunos'])),
            ("Aulas Registradas:", str(detalhes.get('total_aulas', 0))),
            ("Atividades Criadas:", str(detalhes.get('total_atividades', 0))),
        ]
        
        for label, valor in dados:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(pady=5, padx=20, fill="x")
            
            ctk.CTkLabel(row_frame, text=label, font=ctk.CTkFont(size=13, weight="bold"), width=180, anchor="w").pack(side="left")
            ctk.CTkLabel(row_frame, text=valor, font=ctk.CTkFont(size=13), anchor="w").pack(side="left")
        
        if detalhes.get('descricao'):
            ctk.CTkLabel(dialog, text="Descrição:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=60, pady=(20, 5))
            desc_text = ctk.CTkTextbox(dialog, width=580, height=150)
            desc_text.insert("1.0", detalhes['descricao'])
            desc_text.configure(state="disabled")
            desc_text.pack(padx=60, pady=(0, 20))
        
        ctk.CTkButton(dialog, text="Fechar", command=dialog.destroy, width=150, fg_color="gray").pack(pady=20)
    
    def confirmar_excluir_turma(self, turma):
        result = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a turma:\n\n{turma['nome']}\n{turma['disciplina']}\n\nTodos os dados relacionados (aulas, atividades, notas) serão perdidos!\n\nEsta ação é IRREVERSÍVEL!",
            icon='warning'
        )
        
        if result:
            from backend.turmas_backend import excluir_turma
            sucesso = excluir_turma(turma['id'])
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Turma excluída com sucesso!")
                self.show_gerenciar_turmas()
            else:
                messagebox.showerror("Erro", "Erro ao excluir turma!")
    
    def show_relatorios_gerais(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📊 Relatórios Gerais do Sistema",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        from backend.turmas_backend import get_relatorio_geral
        relatorio = get_relatorio_geral()
        
        sections = [
            ("👥 Usuários", [
                ("Total de Usuários:", str(relatorio['total_usuarios'])),
                ("Administradores:", str(relatorio['total_admins'])),
                ("Professores:", str(relatorio['total_professores'])),
                ("Alunos:", str(relatorio['total_alunos'])),
            ]),
            ("📚 Turmas", [
                ("Total de Turmas:", str(relatorio['total_turmas'])),
                ("Alunos Matriculados:", str(relatorio['total_matriculas'])),
                ("Média de Alunos/Turma:", f"{relatorio['media_alunos_turma']:.1f}"),
            ]),
            ("📝 Atividades", [
                ("Total de Atividades:", str(relatorio['total_atividades'])),
                ("Atividades Entregues:", str(relatorio['total_entregas'])),
                ("Taxa de Entrega:", f"{relatorio['taxa_entrega']:.1f}%"),
                ("Atividades Corrigidas:", str(relatorio['total_corrigidas'])),
            ]),
            ("📊 Desempenho", [
                ("Média Geral do Sistema:", f"{relatorio['media_geral_sistema']:.2f}"),
                ("Taxa de Aprovação:", f"{relatorio['taxa_aprovacao']:.1f}%"),
            ]),
        ]
        
        for section_title, items in sections:
            section_frame = ctk.CTkFrame(main_frame)
            section_frame.pack(pady=15, padx=40, fill="x")
            
            ctk.CTkLabel(
                section_frame,
                text=section_title,
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(anchor="w", padx=20, pady=(15, 10))
            
            for label, valor in items:
                row_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
                row_frame.pack(pady=5, padx=40, fill="x")
                
                ctk.CTkLabel(
                    row_frame,
                    text=label,
                    font=ctk.CTkFont(size=14),
                    width=250,
                    anchor="w"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    row_frame,
                    text=valor,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    anchor="w"
                ).pack(side="left")
            
            section_frame.pack_configure(pady=(15, 5))
        
        export_btn = ctk.CTkButton(
            main_frame,
            text="📄 Exportar Relatório",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=300,
            height=50,
            command=lambda: self.exportar_relatorio(relatorio),
            fg_color="#2CC985"
        )
        export_btn.pack(pady=30)
        
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
        back_btn.pack(pady=10)
    
    def exportar_relatorio(self, relatorio):
        from tkinter import filedialog
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de Texto", "*.txt"), ("Todos os arquivos", "*.*")],
            initialfile=f"relatorio_sistema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if save_path:
            from backend.turmas_backend import exportar_relatorio_txt
            sucesso = exportar_relatorio_txt(relatorio, save_path)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao exportar relatório!")
    
    def show_estatisticas(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📈 Estatísticas do Sistema",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        from backend.turmas_backend import get_estatisticas_detalhadas
        stats = get_estatisticas_detalhadas()
        
        ctk.CTkLabel(
            main_frame,
            text="🏆 Top 5 Alunos com Melhores Médias",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 15))
        
        top_alunos_frame = ctk.CTkFrame(main_frame)
        top_alunos_frame.pack(pady=10, padx=40, fill="x")
        
        for i, aluno in enumerate(stats['top_alunos'], 1):
            aluno_frame = ctk.CTkFrame(top_alunos_frame, fg_color="transparent")
            aluno_frame.pack(pady=5, padx=20, fill="x")
            
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🎖️"
            
            ctk.CTkLabel(
                aluno_frame,
                text=f"{medal} {i}º - {aluno['nome']} | Média: {aluno['media']:.2f}",
                font=ctk.CTkFont(size=14),
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            main_frame,
            text="👨‍🏫 Professores Mais Ativos",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 15))
        
        prof_frame = ctk.CTkFrame(main_frame)
        prof_frame.pack(pady=10, padx=40, fill="x")
        
        for prof in stats['professores_ativos']:
            p_frame = ctk.CTkFrame(prof_frame, fg_color="transparent")
            p_frame.pack(pady=5, padx=20, fill="x")
            
            ctk.CTkLabel(
                p_frame,
                text=f"👨‍🏫 {prof['nome']} | Turmas: {prof['turmas']} | Atividades: {prof['atividades']}",
                font=ctk.CTkFont(size=14),
                anchor="w"
            ).pack(side="left")
        
        ctk.CTkLabel(
            main_frame,
            text="📚 Turmas com Melhor Desempenho",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 15))
        
        turmas_frame = ctk.CTkFrame(main_frame)
        turmas_frame.pack(pady=10, padx=40, fill="x")
        
        for turma in stats['melhores_turmas']:
            t_frame = ctk.CTkFrame(turmas_frame, fg_color="transparent")
            t_frame.pack(pady=5, padx=20, fill="x")
            
            ctk.CTkLabel(
                t_frame,
                text=f"📖 {turma['nome']} | Média: {turma['media']:.2f} | Taxa de Aprovação: {turma['taxa_aprovacao']:.1f}%",
                font=ctk.CTkFont(size=14),
                anchor="w"
            ).pack(side="left")
        
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
    
    def show_limpeza_dados(self):
        self.app.clear_window()
        
        main_frame = ctk.CTkFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="🗑️ Limpeza de Dados",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(30, 20))
        
        warning_label = ctk.CTkLabel(
            main_frame,
            text="⚠️ ATENÇÃO: Essas operações são IRREVERSÍVEIS! ⚠️",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#E74C3C"
        )
        warning_label.pack(pady=(10, 40))
        
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)
        
        operations = [
            ("Limpar Turmas Antigas", "Excluir turmas de anos anteriores", lambda: self.limpar_turmas_antigas()),
            ("Remover Atividades Antigas", "Excluir atividades com mais de 1 ano", lambda: self.limpar_atividades_antigas()),
            ("Arquivar Usuários Inativos", "Remover usuários sem atividade há mais de 1 ano", lambda: self.arquivar_inativos()),
        ]
        
        for titulo, descricao, comando in operations:
            op_frame = ctk.CTkFrame(buttons_frame)
            op_frame.pack(pady=15, padx=40, fill="x")
            
            ctk.CTkLabel(
                op_frame,
                text=titulo,
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", padx=20, pady=(15, 5))
            
            ctk.CTkLabel(
                op_frame,
                text=descricao,
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(anchor="w", padx=20, pady=(0, 10))
            
            ctk.CTkButton(
                op_frame,
                text="Executar",
                width=150,
                height=40,
                command=comando,
                fg_color="#E74C3C",
                hover_color="#C0392B"
            ).pack(anchor="e", padx=20, pady=(0, 15))
        
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
        back_btn.pack(side="bottom", pady=30)
    
    def limpar_turmas_antigas(self):
        result = messagebox.askyesno(
            "Confirmar Limpeza",
            "Deseja realmente excluir todas as turmas de anos anteriores?\n\nEsta ação não pode ser desfeita!",
            icon='warning'
        )
        
        if result:
            from backend.turmas_backend import limpar_turmas_antigas
            total = limpar_turmas_antigas()
            messagebox.showinfo("Concluído", f"{total} turma(s) antiga(s) foram removidas.")
    
    def limpar_atividades_antigas(self):
        result = messagebox.askyesno(
            "Confirmar Limpeza",
            "Deseja realmente excluir todas as atividades com mais de 1 ano?\n\nEsta ação não pode ser desfeita!",
            icon='warning'
        )
        
        if result:
            from backend.turmas_backend import limpar_atividades_antigas
            total = limpar_atividades_antigas()
            messagebox.showinfo("Concluído", f"{total} atividade(s) antiga(s) foram removidas.")
    
    def arquivar_inativos(self):
        result = messagebox.askyesno(
            "Confirmar Arquivamento",
            "Deseja realmente arquivar usuários inativos há mais de 1 ano?\n\nEsta ação não pode ser desfeita!",
            icon='warning'
        )
        
        if result:
            from backend.turmas_backend import arquivar_usuarios_inativos
            total = arquivar_usuarios_inativos()
            messagebox.showinfo("Concluído", f"{total} usuário(s) inativo(s) foram arquivados.")
    
    def darken_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
