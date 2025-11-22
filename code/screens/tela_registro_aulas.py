import customtkinter as ctk 
from tkinter import messagebox, filedialog 
from datetime import datetime 

class TelaRegistroAulas:
    
    def __init__(self, app, user_email):
        # O construtor da classe.
        self.app = app # Armazena a instância da janela principal do aplicativo para manipular a exibição de telas.
        self.user_email = user_email # Armazena o e-mail do professor logado, essencial para buscar as turmas corretas no backend.
    
    def limitar_caracteres(self, var, limite):
        # Define uma função de callback para limitar o número de caracteres em um campo de entrada.
        def callback(*args):
            conteudo = var.get() # Obtém o conteúdo atual da variável de string associada ao campo.
            if len(conteudo) > limite:
                
                var.set(conteudo[:limite]) # Trunca o conteúdo para o limite máximo e o define novamente.
        return callback # Retorna a função de callback para ser ligada ao evento de escrita do StringVar.

    def show_registro_aulas(self):
        # Exibe a tela principal de registro de aulas, listando as turmas.
        self.app.clear_window() # Limpa o conteúdo atual da janela principal.
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0) # Cria um frame rolável para conter todo o conteúdo da tela.
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📝 Registro de Aulas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        
        new_btn = ctk.CTkButton(
            main_frame,
            text="➕ Registrar Nova Aula",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=300,
            height=50,
            command=self.show_nova_aula, # Comando para abrir a tela de registro de nova aula (sem turma pré-selecionada).
            fg_color="#2CC985",
            hover_color="#25A066"
        )
        new_btn.pack(pady=20)
        
        from backend.turmas_backend import get_turmas_professor # Importa a função do backend para obter as turmas do professor.
        turmas = get_turmas_professor(self.user_email) # Obtém a lista de turmas.
        
        if not turmas:
            # Exibe uma mensagem se não houver turmas cadastradas.
            empty_label = ctk.CTkLabel(
                main_frame,
                text="Você ainda não possui turmas cadastradas.",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            # Itera sobre cada turma para criar um widget de exibição.
            for turma in turmas:
                turma_frame = ctk.CTkFrame(main_frame) # Frame para a turma individual.
                turma_frame.pack(pady=10, padx=40, fill="x")
                
                info_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"📖 {turma['nome']}", # Exibe o nome da turma.
                    font=ctk.CTkFont(size=18, weight="bold")
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"Disciplina: {turma['disciplina']} | Período: {turma['periodo']}", # Exibe disciplina e período.
                    font=ctk.CTkFont(size=13),
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                from backend.turmas_backend import get_aulas_turma # Importa a função para obter aulas.
                aulas = get_aulas_turma(turma['id']) # Obtém as aulas registradas para a turma.
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"Total de aulas: {len(aulas)}", # Exibe a contagem de aulas.
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
                    command=lambda t=turma: self.show_aulas_turma(t) # Botão para navegar para a lista de aulas da turma.
                ).pack(pady=3)
                
                ctk.CTkButton(
                    buttons_frame,
                    text="➕ Nova Aula",
                    width=120,
                    height=35,
                    fg_color="#2CC985",
                    hover_color="#25A066",
                    command=lambda t=turma: self.show_nova_aula(t) # Botão para abrir o formulário de nova aula, pré-selecionando esta turma.
                ).pack(pady=3)
        
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.voltar_menu, # Comando para retornar ao menu principal (presumido).
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    def show_nova_aula(self, turma=None):
        # Exibe a janela de diálogo para registrar uma nova aula.
        dialog = ctk.CTkToplevel(self.app) # Cria uma nova janela pop-up (nível superior).
        dialog.title("Registrar Nova Aula")
        dialog.geometry("700x600")
        dialog.grab_set() # Torna a janela modal (bloqueia interações com a janela principal).
        dialog.resizable(height=False, width=False)

        form_frame = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            form_frame,
            text="📝 Registrar Nova Aula",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        ctk.CTkLabel(
            form_frame,
            text="Turma:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        from backend.turmas_backend import get_turmas_professor # Importa função (necessário para o OptionMenu).
        turmas = get_turmas_professor(self.user_email) # Obtém a lista de turmas.
        
        turma_var = ctk.StringVar()
        turma_options = [f"{t['nome']} - {t['disciplina']}" for t in turmas]
        turma_map = {f"{t['nome']} - {t['disciplina']}": t for t in turmas} # Mapeia a string de exibição para o objeto da turma.
        
        if turma:
            turma_var.set(f"{turma['nome']} - {turma['disciplina']}") # Pré-seleciona a turma se um objeto 'turma' foi passado.
        elif turmas:
            turma_var.set(turma_options[0]) # Caso contrário, seleciona a primeira turma disponível.
        
        turma_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=turma_var,
            values=turma_options,
            width=600,
            height=40
        )
        turma_menu.pack(padx=20, pady=(0, 15))
        
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
        data_entry.insert(0, datetime.now().strftime("%d/%m/%Y")) # Insere a data atual no formato dia/mês/ano.
        data_entry.pack(padx=20, pady=(0, 15))
        
        limite_titulo = 46
        titulo_var = ctk.StringVar() # Variável de controle para o limite de caracteres do título.

        ctk.CTkLabel(
            form_frame,
            text="Título da Aula:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        titulo_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Introdução à Álgebra Linear",
            width=600,
            height=40,
            textvariable=titulo_var
        )
        titulo_entry.pack(padx=20, pady=(0, 15))
        titulo_var.trace_add("write", self.limitar_caracteres(titulo_var, limite_titulo)) # Liga o callback de limite de caracteres à variável.
        
        ctk.CTkLabel(
            form_frame,
            text="Conteúdo da Aula(máximo 1000 caracteres):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        conteudo_text = ctk.CTkTextbox(
            form_frame,
            width=600,
            height=150,
            wrap="word",
        )
        conteudo_text.pack(padx=20, pady=(0, 15))
        
        limite_texto_curto = 65
        observacoes_var = ctk.StringVar() # Variável de controle para o limite de caracteres das observações.

        ctk.CTkLabel(
            form_frame,
            text="Observações (opcional):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        observacoes_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Prova na próxima aula",
            width=600,
            height=40,
            textvariable=observacoes_var
        )
        observacoes_entry.pack(padx=20, pady=(0, 15))
        observacoes_var.trace_add("write", self.limitar_caracteres(observacoes_var, limite_texto_curto)) # Liga o callback de limite de caracteres à variável.
        
        def salvar_aula():
            # Lógica para coletar os dados do formulário e salvar a aula.
            turma_selecionada = turma_map.get(turma_var.get()) # Obtém o objeto turma a partir da string selecionada.

            if not turma_selecionada:
                messagebox.showerror("Erro", "Selecione uma turma!")
                return
            
            limite_texto = 1000 # Redefine o limite do conteúdo (apenas para referência na validação).
            
            data = data_entry.get().strip()
            titulo = titulo_var.get().strip().title() # Obtém o título e aplica capitalização (título).
            conteudo = conteudo_text.get("1.0", "end-1c").strip() # Obtém o conteúdo do Textbox (removendo a última nova linha).
            observacoes = observacoes_var.get().strip()
            
            if not all([data, titulo, conteudo]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            if len(conteudo) > limite_texto:
                messagebox.showerror("Erro", f"O conteúdo não pode ter mais de {limite_texto} caracteres.")
                return 
            
            from backend.turmas_backend import registrar_aula # Importa a função do backend para registrar a aula.
            aula_id = registrar_aula(
                turma_selecionada['id'],
                data,
                titulo,
                conteudo,
                observacoes
            )
            
            if aula_id:
                # Pergunta se o usuário deseja iniciar a chamada após o registro.
                fazer_chamada = messagebox.askyesno(
                    "Aula Registrada",
                    "Aula registrada com sucesso!\n\nDeseja fazer a chamada agora?",
                    icon='question'
                )
                
                dialog.destroy() # Fecha a janela de registro.
                
                if fazer_chamada:
                    self.show_chamada(aula_id, turma_selecionada) # Chama a tela de chamada.
                else:
                    messagebox.showinfo("Sucesso", "Aula registrada com sucesso!")
                    self.show_registro_aulas() # Atualiza a tela principal.
            else:
                messagebox.showerror("Erro", "Erro ao registrar aula!")
        
        ctk.CTkButton(
            form_frame,
            text="✓ Salvar Aula",
            command=salvar_aula, # Liga a função de salvar ao botão.
            width=200,
            height=45,
            fg_color="#2CC985",
            hover_color="#25A066"
        ).pack(pady=20)

        back_btn = ctk.CTkButton(
            dialog,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.voltar_menu, # Comando para fechar o diálogo e voltar ao menu (presumido).
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    def show_aulas_turma(self, turma):
        # Exibe a lista detalhada de aulas para uma turma específica.
        
        self.app.clear_window() # Limpa o conteúdo da janela principal.
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📝 Aulas: {turma['nome']}", # Título específico da turma.
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
        
        from backend.turmas_backend import get_aulas_turma # Importa função.
        aulas = get_aulas_turma(turma['id']) # Obtém a lista de aulas da turma.
        
        if not aulas:
            # Mensagem se não houver aulas.
            empty_label = ctk.CTkLabel(
                main_frame,
                text="Nenhuma aula registrada ainda.",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            # Itera sobre as aulas para exibir os detalhes.
            for aula in aulas:
                aula_frame = ctk.CTkFrame(main_frame)
                aula_frame.pack(pady=10, padx=40, fill="x")
                
                info_frame = ctk.CTkFrame(aula_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"📅 {aula['data']} - {aula['titulo']}",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    wraplength=400
                ).pack(anchor="w")
                
                conteudo_aula = ctk.CTkTextbox(
                    info_frame,
                    font=ctk.CTkFont(size=13),
                    text_color="gray",
                    wrap="word",
                    height=120,
                    
                )
                conteudo_aula.pack(anchor="w", pady=(5, 2),fill="x", expand=True)
                conteudo_aula.insert("0.0", aula['conteudo']) # Insere o conteúdo da aula.
                conteudo_aula.configure(state="disabled") # Desabilita a edição.
                
                if aula.get('observacoes'):
                    # Exibe observações, se existirem.
                    ctk.CTkLabel(
                        info_frame,
                        text=f"Obs: {aula['observacoes']}",
                        font=ctk.CTkFont(size=12),
                        text_color="#E67E22",
                        wraplength=400
                    ).pack(anchor="w", pady=2)
                
                
                from backend.turmas_backend import get_frequencia_aula # Importa função.
                frequencia = get_frequencia_aula(aula['id']) # Verifica se a chamada (frequência) foi registrada.
                
                if frequencia:
                    # Exibe o resumo da chamada se estiver registrada.
                    total_alunos = len(frequencia)
                    presentes = sum(1 for p in frequencia.values() if p)
                    ctk.CTkLabel(
                        info_frame,
                        text=f"✓ Chamada feita: {presentes}/{total_alunos} presentes",
                        font=ctk.CTkFont(size=12),
                        text_color="#2CC985"
                    ).pack(anchor="w", pady=2)
                else:
                    # Exibe um aviso se a chamada não foi feita.
                    ctk.CTkLabel(
                        info_frame,
                        text="⚠ Chamada não realizada",
                        font=ctk.CTkFont(size=12),
                        text_color="#E74C3C"
                    ).pack(anchor="w", pady=2)
                
                buttons_frame = ctk.CTkFrame(aula_frame, fg_color="transparent")
                buttons_frame.pack(side="right", padx=10, pady=10)
                
                if not frequencia:
                    # Botão para fazer a chamada se ainda não foi registrada.
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
                    # Botão para ver a chamada se já foi registrada.
                    ctk.CTkButton(
                        buttons_frame,
                        text="Ver Chamada",
                        width=130,
                        height=35,
                        command=lambda a=aula, t=turma: self.show_ver_chamada(a, t) # Presumida função para visualizar os detalhes da chamada.
                    ).pack(pady=3)
                
                ctk.CTkButton(
                    buttons_frame,
                    text="Editar",
                    width=130,
                    height=35,
                    fg_color="#9B59B6",
                    hover_color="#7D3C98",
                    command=lambda a=aula: self.show_editar_aula(a, turma) # Presumida função para editar os detalhes da aula.
                ).pack(pady=3)
        
        
        new_btn = ctk.CTkButton(
            main_frame,
            text="➕ Registrar Nova Aula",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=300,
            height=50,
            command=lambda: self.show_nova_aula(turma), # Botão para registrar nova aula, mantendo a turma pré-selecionada.
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
            command=self.show_registro_aulas, # Volta para a tela de listagem de turmas.
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=10)
    
    def show_chamada(self, aula_id, turma):
        # Exibe a janela de diálogo para registrar a frequência (chamada) dos alunos.
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Fazer Chamada")
        dialog.geometry("700x600")
        dialog.grab_set() # Torna a janela modal.
        dialog.resizable(height=False, width=False)
        
        scroll_frame = ctk.CTkScrollableFrame(dialog, width=550, height=450)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            scroll_frame,
            text=f"✓ Chamada - {turma['nome']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        from backend.turmas_backend import get_alunos_turma # Importa função.
        alunos = get_alunos_turma(turma['id']) # Obtém a lista de alunos da turma.
        
        if not alunos:
            # Mensagem se não houver alunos matriculados.
            ctk.CTkLabel(
                scroll_frame,
                text="Nenhum aluno matriculado nesta turma.",
                text_color="gray"
            ).pack(pady=20)
            return
        
        presencas = {} # Dicionário para armazenar a presença (email do aluno como chave, BooleanVar como valor).
        
        for aluno in alunos:
            # Itera sobre os alunos para criar um widget de frequência para cada um.
            aluno_frame = ctk.CTkFrame(scroll_frame)
            aluno_frame.pack(pady=5, padx=10, fill="x")
            
            info_frame = ctk.CTkFrame(aluno_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text=aluno['nome'], # Exibe o nome do aluno.
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            ).pack(anchor="w")
            
            if aluno.get('rm'):
                ctk.CTkLabel(
                    info_frame,
                    text=f"RM: {aluno['rm']}", # Exibe o RM (Registro de Matrícula), se existir.
                    font=ctk.CTkFont(size=12),
                    text_color="gray",
                    anchor="w"
                ).pack(anchor="w")
            
            
            presenca_var = ctk.BooleanVar(value=True) # Variável de controle booleana, True por padrão (presente).
            presencas[aluno['email']] = presenca_var # Associa a variável de controle ao e-mail do aluno.
            
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
            # Lógica para salvar a frequência de todos os alunos.
            presencas_dict = {email: var.get() for email, var in presencas.items()} # Converte os BooleanVar em um dicionário de booleanos (True/False).
            
            from backend.turmas_backend import registrar_chamada # Importa função.
            sucesso = registrar_chamada(aula_id, presencas_dict) # Registra a chamada no backend.
            
            if sucesso:
                # Exibe o resumo e fecha a janela.
                presentes = sum(1 for p in presencas_dict.values() if p)
                total = len(presencas_dict)
                messagebox.showinfo(
                    "Sucesso",
                    f"Chamada registrada com sucesso!\n\nPresentes: {presentes}/{total}"
                )
                dialog.destroy()
                self.show_registro_aulas() # Retorna à lista de turmas/aulas atualizada.
            else:
                messagebox.showerror("Erro", "Erro ao registrar chamada!")
        
        ctk.CTkButton(
            scroll_frame,
            text="✓ Salvar Chamada",
            command=salvar_chamada, # Liga a função de salvar ao botão.
            width=200,
            height=45,
            fg_color="#2CC985",
            hover_color="#25A066"
        ).pack(pady=20)

        ctk.CTkButton(
            dialog,
            text="Fechar",
            command=dialog.destroy, # Comando para fechar a janela de diálogo (modal).
            width=200,
            height=45,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(pady=20)
    
    def show_ver_chamada(self, aula, turma):
        #  Método para exibir os detalhes da frequência (chamada) de uma aula específica.
        dialog = ctk.CTkToplevel(self.app) # Cria uma nova janela de nível superior (modal).
        dialog.title("Visualizar Chamada")
        dialog.geometry("700x600")
        dialog.grab_set() # Torna a janela modal.
        dialog.resizable(height=False, width=False)

        form_frame = ctk.CTkScrollableFrame(dialog, corner_radius=0) # Frame rolável para o conteúdo.
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            form_frame,
            text=f"📋 Chamada - {aula['titulo']}", # Exibe o título da aula.
            font=ctk.CTkFont(size=20, weight="bold"),
            wraplength=500
        )
        title.pack(pady=20)
        
        ctk.CTkLabel(
            form_frame,
            text=f"Data: {aula['data']}", # Exibe a data da aula.
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
        from backend.turmas_backend import get_frequencia_aula, get_alunos_turma # Importa funções de acesso ao backend.
        frequencia = get_frequencia_aula(aula['id']) # Obtém o registro de frequência da aula.
        alunos = get_alunos_turma(turma['id']) # Obtém a lista de alunos da turma.
        total = len(alunos)
        presentes = sum(1 for p in frequencia.values() if p) # Calcula o número de presentes.
        ausentes = total - presentes # Calcula o número de ausentes.
        percentual = (presentes / total * 100) if total > 0 else 0 # Calcula o percentual de frequência.
        
        ctk.CTkLabel(
            form_frame,
            text=f"Presentes: {presentes} | Ausentes: {ausentes} | Total: {total}", # Exibe o resumo estatístico.
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(
            form_frame,
            text=f"Frequência: {percentual:.1f}%", # Exibe a porcentagem.
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2CC985" if percentual >= 75 else "#E74C3C" # Cor condicional (verde para alta frequência, vermelho para baixa).
        ).pack(pady=5)
        
        for aluno in alunos:
            # Itera sobre os alunos para exibir o status individual.
            presente = frequencia.get(aluno['email'], False) # Pega o status do aluno (True/False).
            
            aluno_frame = ctk.CTkFrame(form_frame)
            aluno_frame.pack(pady=5, padx=10, fill="x")
            
            info_frame = ctk.CTkFrame(aluno_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text=aluno['nome'], # Exibe o nome do aluno.
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            ).pack(anchor="w")
            
            if aluno.get('rm'):
                ctk.CTkLabel(
                    info_frame,
                    text=f"RM: {aluno['rm']}", # Exibe o RM, se disponível.
                    font=ctk.CTkFont(size=12),
                    text_color="gray",
                    anchor="w"
                ).pack(anchor="w")
            
            status_label = ctk.CTkLabel(
                aluno_frame,
                text="✓ Presente" if presente else "✗ Ausente", # Exibe o status formatado.
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#2CC985" if presente else "#E74C3C" # Cor para status (verde/vermelho).
            )
            status_label.pack(side="right", padx=15, pady=10)
        
        ctk.CTkButton(
            form_frame,
            text="✏️ Editar Chamada",
            # Comando: fecha a janela atual (Visualizar) e abre a janela de edição.
            command=lambda: (dialog.destroy(), self.show_editar_chamada(aula['id'], turma)), 
            width=200,
            height=45,
            fg_color="#9B59B6", # Cor roxa (edição).
            hover_color="#7D3C98",
        ).pack(pady=10)

        ctk.CTkButton(
            dialog,
            text="Fechar",
            command=dialog.destroy, # Botão para fechar o modal.
            width=200,
            height=45,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(pady=20)
    
    def show_editar_aula(self, aula, turma):
        #  Método para exibir e permitir a edição dos detalhes de uma aula.
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Editar Aula")
        dialog.geometry("700x600")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)

        form_frame = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            form_frame,
            text="✏️ Editar Aula", # Título da edição.
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        # Exibição da turma (não editável).
        ctk.CTkLabel(
            form_frame,
            text="Turma:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        ctk.CTkLabel(
            form_frame,
            text=f"{turma['nome']} - {turma['disciplina']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Campo de entrada para a Data (pré-preenchido).
        ctk.CTkLabel(
            form_frame,
            text="Data da Aula:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        data_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="DD/MM/AAAA",
            width=600,
            height=40
        )
        data_entry.insert(0, aula['data']) # Insere o valor atual da data.
        data_entry.pack(padx=20, pady=(0, 15))
        
        limite_titulo = 46
        titulo_var = ctk.StringVar(value=aula['titulo']) # StringVar inicializada com o título atual.
        
        # Campo de entrada para o Título (com limite de caracteres).
        ctk.CTkLabel(
            form_frame,
            text="Título da Aula:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        titulo_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Introdução à Álgebra Linear",
            width=600,
            height=40,
            textvariable=titulo_var
        )
        titulo_entry.pack(padx=20, pady=(0, 15))
        titulo_var.trace_add("write", self.limitar_caracteres(titulo_var, limite_titulo)) # Aplica o limite.
        
        # Campo de entrada para o Conteúdo (Textbox, pré-preenchido).
        ctk.CTkLabel(
            form_frame,
            text="Conteúdo da Aula (máximo 1000 caracteres):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        conteudo_text = ctk.CTkTextbox(
            form_frame,
            width=600,
            height=150,
            wrap="word",
        )
        conteudo_text.insert("0.0", aula['conteudo']) # Insere o conteúdo atual.
        conteudo_text.pack(padx=20, pady=(0, 15))
        
        limite_texto_curto = 65
        observacoes_var = ctk.StringVar(value=aula.get('observacoes', '')) # StringVar inicializada com observações atuais.
        
        # Campo de entrada para Observações (com limite de caracteres).
        ctk.CTkLabel(
            form_frame,
            text="Observações (opcional):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        observacoes_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Prova na próxima aula",
            width=600,
            height=40,
            textvariable=observacoes_var
        )
        observacoes_entry.pack(padx=20, pady=(0, 15))
        observacoes_var.trace_add("write", self.limitar_caracteres(observacoes_var, limite_texto_curto)) # Aplica o limite.
        
        def salvar_edicao():
            # Função para coletar os dados e salvar as alterações no backend.
            limite_texto = 1000
            
            data = data_entry.get().strip()
            titulo = titulo_var.get().strip().title()
            conteudo = conteudo_text.get("1.0", "end-1c").strip()
            observacoes = observacoes_var.get().strip()
            
            if not all([data, titulo, conteudo]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            if len(conteudo) > limite_texto:
                messagebox.showerror("Erro", f"O conteúdo não pode ter mais de {limite_texto} caracteres.")
                return
            
            from backend.turmas_backend import editar_aula # Importa função de edição.
            sucesso = editar_aula( # Chama o backend.
                aula['id'],
                data,
                titulo,
                conteudo,
                observacoes
            )
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Aula atualizada com sucesso!")
                dialog.destroy()
                self.show_aulas_turma(turma) # Recarrega a tela de aulas da turma.
            else:
                messagebox.showerror("Erro", "Erro ao atualizar aula!")
        
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        ctk.CTkButton(
            buttons_frame,
            text="✓ Salvar Alterações",
            command=salvar_edicao, # Botão para salvar.
            width=200,
            height=45,
            fg_color="#2CC985",
            hover_color="#25A066"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="✗ Cancelar",
            command=dialog.destroy, # Botão para cancelar a edição e fechar o modal.
            width=200,
            height=45,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(side="left", padx=10)

    def show_editar_chamada(self, aula_id, turma):
        #  Método para exibir e permitir a edição de uma chamada já registrada.
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Editar Chamada")
        dialog.geometry("700x600")
        dialog.grab_set() 
        dialog.resizable(height=False, width=False)
        
        scroll_frame = ctk.CTkScrollableFrame(dialog, width=550, height=450)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            scroll_frame,
            text=f"✏️ Editar Chamada - {turma['nome']}", # Título da edição de chamada.
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)

        from backend.turmas_backend import get_alunos_turma, get_frequencia_aula, registrar_chamada # Importa funções.

        frequencia_atual = get_frequencia_aula(aula_id) # Obtém o registro de frequência atual.
        alunos = get_alunos_turma(turma['id'])
        
        if not alunos:
            # Mensagem de erro caso não haja alunos na turma.
            ctk.CTkLabel(
                scroll_frame,
                text="Nenhum aluno matriculado nesta turma.",
                text_color="gray"
            ).pack(pady=20)
            return
        
        presencas = {}
        
        for aluno in alunos:
            # Loop para criar o switch de presença/ausência para cada aluno.
            status_inicial = frequencia_atual.get(aluno['email'], False) # Define o estado inicial do switch (False se não encontrado).
            
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
            
            presenca_var = ctk.BooleanVar(value=status_inicial)
            presencas[aluno['email']] = presenca_var # Mapeia o email do aluno à variável de controle do switch.
            
            switch = ctk.CTkSwitch(
                aluno_frame,
                text="Presente",
                variable=presenca_var,
                onvalue=True,
                offvalue=False,
                progress_color="#2CC985"
            )
            switch.pack(side="right", padx=15, pady=10)
        
        def salvar_edicao_chamada():
            # Função para coletar os novos status de presença e salvar no backend.
            presencas_dict = {email: var.get() for email, var in presencas.items()}
            sucesso = registrar_chamada(aula_id, presencas_dict) # Usa a mesma função de registro para atualizar/sobrescrever.
            
            if sucesso:
                presentes = sum(1 for p in presencas_dict.values() if p)
                total = len(presencas_dict)
                messagebox.showinfo(
                    "Sucesso",
                    f"Chamada atualizada com sucesso!\n\nPresentes: {presentes}/{total}"
                )
                dialog.destroy()
                self.show_registro_aulas() # Retorna à tela inicial de registro de aulas (que lista as turmas).
            else:
                messagebox.showerror("Erro", "Erro ao atualizar chamada!")
        
        ctk.CTkButton(
            scroll_frame,
            text="✓ Salvar Edições",
            command=salvar_edicao_chamada, # Botão para salvar as edições.
            width=200,
            height=45,
            fg_color="#3B8EDC", # Cor azul para salvar edição.
            hover_color="#36719F"
        ).pack(pady=20)

        ctk.CTkButton(
            dialog,
            text="Fechar",
            command=dialog.destroy, # Botão para fechar o modal.
            width=200,
            height=45,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(pady=20)
    
    def voltar_menu(self):
        #  Método para retornar ao menu principal do professor.
        
        from screens.telas_professor import TelasProfessor # Importa a classe de navegação.
        telas = TelasProfessor(self.app, self.user_email) # Cria uma instância da classe de telas.
        telas.show_professor_menu() # Chama o método para exibir o menu.