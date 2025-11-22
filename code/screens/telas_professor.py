import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import os
from screens.tela_registro_aulas import TelaRegistroAulas

class TelasProfessor:
    
    # Método construtor da classe
    def __init__(self, app, user_email):
        self.app = app
        self.user_email = user_email
    # Método para escutar e limitar o número de caracteres em um widget de entrada
    def limitar_caracteres(self, var, limite):
        # Define a função de callback que será chamada em cada alteração da variável
        def callback(*args):
            conteudo = var.get()

            # Se o conteúdo exceder o limite, ele é truncado
            if len(conteudo) > limite:
                var.set(conteudo[:limite])
        # Retorna a função de callback para ser vinculada (e.g., com .trace_add)
        return callback
    
    # Método principal que exibe o menu inicial do professor
    def show_professor_menu(self):
        # Limpa todos os widgets existentes na janela principal da aplicação
        self.app.clear_window()

        # Cria um frame com barra de rolagem para acomodar o conteúdo
        scroll_container = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Frame principal dentro do container de rolagem
        main_frame = ctk.CTkFrame(scroll_container, corner_radius=0)
        main_frame.pack(padx=20, pady=20, fill="x")
        
        # Importa uma função para acessar os dados do usuário
        from backend.turmas_backend import get_user_data
        
        # Tenta obter os dados do usuário do banco de dados
        user_data = get_user_data(self.user_email)
        
        # Cabeçalho de Boas-Vindas
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=20, pady=(20, 30))
        
        # Rótulo de título com o nome do professor
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"👨‍🏫 Bem-vindo, Prof. {user_data['nome']}!",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Rótulo para o email do professor
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=f"Email: {self.user_email}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack()
        
        # Frame para adicionar os botões
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)
        
        # Lista de tuplas: (Texto do Botão, Comando de Função, Cor)
        buttons_data = [
            ("📚 Minhas Turmas", self.show_turmas_professor, "#3498DB"),
            ("📝 Registro de Aulas", self.show_registro_aulas, "#9B59B6"),
            ("📄 Relatórios de Aulas", self.show_relatorios_aulas, "#16A085"),
            ("📋 Atividades", self.show_atividades_professor, "#E67E22"),
            ("📊 Notas e Frequência", self.show_notas_frequencia, "#1ABC9C"),
            ("🚪 Sair", lambda: self.app.logout(), "#E74C3C")
        ]
        
        # Cria e empacota os botões dinamicamente
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

    # Método para exibir a lista de turmas em que o aluno está matriculado
    def show_turmas_professor(self):
        self.app.clear_window()
        
        #cria um frame de colagem principal para exbir o conteúdo do método
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        #Título da tela
        title_label = ctk.CTkLabel(
            main_frame,
            text="📚 Minhas Turmas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Importa a função para visualisar as turmas do professor
        from backend.turmas_backend import get_turmas_professor
        turmas = get_turmas_professor(self.user_email)
        
        # Verifica se alguma turma foi encontrada (caso sim: constroi a leta, caso: retorna uma mensagem)
        if not turmas:
            empty_label = ctk.CTkLabel(
                main_frame,
                text="Você ainda não possui turmas atribuídas.\nContate o administrador para receber turmas!",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            for turma in turmas:
                #Cria uma frame para exibir as turmas 
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=10, padx=40, fill="x")
                
                #Cria uma frame filha dentro de turma_frame
                info_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                #Exibe nome da turma
                nome_label = ctk.CTkLabel(
                    info_frame,
                    text=f"📖 {turma['nome']}",
                    font=ctk.CTkFont(size=18, weight="bold")
                )
                nome_label.pack(anchor="w")
                
                #Exibe disciplina da turma
                disciplina_label = ctk.CTkLabel(
                    info_frame,
                    text=f"Disciplina: {turma['disciplina']}",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                disciplina_label.pack(anchor="w", pady=2)
                
                #Exibe quantidade de alunos e ano atual da turma
                info_label = ctk.CTkLabel(
                    info_frame,
                    text=f"Alunos: {turma['total_alunos']} | Ano: {turma['ano']}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                )
                info_label.pack(anchor="w", pady=2)
                
                #Cria um frame para exbir botões
                buttons_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                buttons_frame.pack(side="right", padx=10, pady=10)
                
                #cria um botão para ver os detalhes da turma
                view_btn = ctk.CTkButton(
                    buttons_frame,
                    text="Ver Detalhes",
                    width=120,
                    height=35,
                    command=lambda t=turma: self.show_detalhes_turma(t)
                )
                view_btn.pack(pady=3)
        
        #Cria um botão na main frame da tela para voltar a tela anterior
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
    
    #Método para exbir os detalhes de uma turma
    def show_detalhes_turma(self, turma):
        # Limpa os widgets da tela
        self.app.clear_window()
        
        #Frame principal
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titulo com o nome da turma
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📖 {turma['nome']}",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Label com exibindo disciplina, ano e periodo da turma
        info_label = ctk.CTkLabel(
            main_frame,
            text=f"{turma['disciplina']} | {turma['ano']} | {turma['periodo']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info_label.pack(pady=(0, 30))
        
        #Cria uma tabView
        tabs = ctk.CTkTabview(main_frame, width=800, height=400)
        tabs.pack(pady=20, padx=40)
        
        #Adiciona a tabs alunos, aulas e atividades
        tabs.add("👥 Alunos")
        tabs.add("📝 Aulas")
        tabs.add("📋 Atividades")
        
        #Importa algumas funções para visualizar e manipular dados
        from backend.turmas_backend import get_alunos_turma, get_aulas_turma, get_atividades_turma
        
        # Obtem os alunos matriculados na turma
        alunos = get_alunos_turma(turma['id'])

        # Se não tiver aluno exibe uma mensagem, se não constroi o resto da interface da tela
        if not alunos:
            ctk.CTkLabel(tabs.tab("👥 Alunos"), text="Nenhum aluno matriculado ainda.", text_color="gray").pack(pady=20)
        else:
            for aluno in alunos:
                #Frame para exibir alunos
                aluno_frame = ctk.CTkFrame(tabs.tab("👥 Alunos"))
                aluno_frame.pack(pady=5, padx=10, fill="x")
                
                #Label com nome e email dos alunos cadastrados na turma
                ctk.CTkLabel(
                    aluno_frame,
                    text=f"👤 {aluno['nome']} - {aluno['email']}",
                    font=ctk.CTkFont(size=14)
                ).pack(side="left", padx=20, pady=10)
        
        # Captura as aulas da turma e realiza a mesma verificação para alunos
        aulas = get_aulas_turma(turma['id'])
        if not aulas:
            ctk.CTkLabel(tabs.tab("📝 Aulas"), text="Nenhuma aula registrada", text_color="gray").pack(pady=20)
        else:
            for aula in aulas:
                # Frame para exibir as aulas
                aula_frame = ctk.CTkFrame(tabs.tab("📝 Aulas"))
                aula_frame.pack(pady=5, padx=10, fill="x")
                
                # Label para exibir data e titulo das aulas
                ctk.CTkLabel(
                    aula_frame,
                    text=f"📅 {aula['data']} - {aula['titulo']}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    wraplength=550
                ).pack(anchor="w", padx=20, pady=(10, 5))
                
                # Text Box para exibir o conteúdo da aula
                conteudo_aula = ctk.CTkTextbox(
                    aula_frame,
                    font=ctk.CTkFont(size=13),
                    text_color="gray",
                    wrap="word",
                    height=120,
                )
                # Algumas propriedades para configurar a exibição da Text Box
                conteudo_aula.pack(anchor="w", pady=(5, 2), fill="x", expand=True)
                conteudo_aula.insert("0.0", aula['conteudo'])
                conteudo_aula.configure(state="disabled")
        
        # Captura a função para exibir as atividades da turma
        atividades = get_atividades_turma(turma['id'])

        # Repete a mesma verificação de aluno e aulas
        if not atividades:
            ctk.CTkLabel(tabs.tab("📋 Atividades"), text="Nenhuma atividade criada", text_color="gray").pack(pady=20)
        else:
            for atividade in atividades:

                # Frame para atividades 
                ativ_frame = ctk.CTkFrame(tabs.tab("📋 Atividades"))
                ativ_frame.pack(pady=5, padx=10, fill="x")
                
                # label para exibir titulo , data de criação, date de entrega e valor da atividade
                ctk.CTkLabel(
                    ativ_frame,
                    text=f"📄 {atividade['titulo']} | Criado em: {atividade['data_criacao']} | Entrega: {atividade['data_entrega']} | Valor: {atividade['valor']} pts",
                    font=ctk.CTkFont(size=13),
                    wraplength=500
                ).pack(side="left", padx=20, pady=10)
        
        #Botão para voltar
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
    
    #função para mostrar a tela de registro de aulas
    def show_registro_aulas(self):
        tela_aulas = TelaRegistroAulas(self.app, self.user_email)
        tela_aulas.show_registro_aulas()
    
    #função para ver os relatórios das aulas
    def show_relatorios_aulas(self):
        self.app.clear_window()
        
        # Frame principal
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titulo
        title_label = ctk.CTkLabel(
            main_frame,
            text="📄 Relatórios de Aulas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # SubTitulo
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Gerencie os relatórios das suas aulas registradas",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 30))
        
        #Importa algumas funções para visualizar e manipular dados
        from backend.turmas_backend import get_todas_aulas_professor, get_relatorio_por_aula, get_detalhes_completos_turma
        
        #captura as aulas criada pelo professor logado
        aulas = get_todas_aulas_professor(self.user_email)
        
        # Faz uma verificação 
        if not aulas:
            empty_label = ctk.CTkLabel(
                main_frame,
                text="Você ainda não possui aulas registradas.\nVá para 'Registro de Aulas' para criar aulas!",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            aulas_por_turma = {}
            for aula in aulas:
                turma_id = aula['turma_id']

                if turma_id not in aulas_por_turma:
                    turma_detalhes = get_detalhes_completos_turma(turma_id)
                    nome = turma_detalhes.get('nome', 'N/A')
                    disciplina = turma_detalhes.get('disciplina', 'N/A')

                    aulas_por_turma[turma_id] = {
                        'turma_nome': nome,
                        'disciplina': disciplina,
                        'aulas': [] 
                    }
                aulas_por_turma[turma_id]['aulas'].append(aula)
            
            for turma_id, dados_turma in aulas_por_turma.items():
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=10, padx=40, fill="x")
                
                turma_header = ctk.CTkLabel(
                    turma_frame,
                    text=f"📚 {dados_turma['turma_nome']} - {dados_turma['disciplina']}",
                    font=ctk.CTkFont(size=18, weight="bold")
                )
                turma_header.pack(pady=15, padx=20, anchor="w")
                
                for aula in dados_turma['aulas']:
                    
                    # Frame para exibir as aulas
                    aula_frame = ctk.CTkFrame(turma_frame)
                    aula_frame.pack(pady=5, padx=20, fill="x")
                    
                    # Frame dentro de aulas_frame para exibir as informações da aula
                    info_frame = ctk.CTkFrame(aula_frame, fg_color="transparent")
                    info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
                    
                    # Titulo da aula
                    titulo_label = ctk.CTkLabel(
                        info_frame,
                        text=f"📝 {aula['titulo']}",
                        font=ctk.CTkFont(size=14, weight="bold"),
                        wraplength=380
                    )
                    titulo_label.pack(anchor="w")
                    
                    # Data de criação da aula
                    data_label = ctk.CTkLabel(
                        info_frame,
                        text=f"Data: {aula['data']}",
                        font=ctk.CTkFont(size=12),
                        text_color="gray"
                    )
                    data_label.pack(anchor="w", pady=2)
                    
                    # Captura os relatórios gerados pelo professor
                    relatorio = get_relatorio_por_aula(aula['id'])
                    
                    # Cria um frame para os botões
                    buttons_frame = ctk.CTkFrame(aula_frame, fg_color="transparent")
                    buttons_frame.pack(side="right", padx=10, pady=10)
                    
                    # Cria uma verificação para exibir os status do relatório(finalizado, rascunho, criar)
                    if relatorio:
                        if relatorio.get('finalizado', False):
                            
                            # Label para exibir os status do relátório
                            status_label = ctk.CTkLabel(
                                buttons_frame,
                                text="✓ Finalizado",
                                font=ctk.CTkFont(size=12, weight="bold"),
                                text_color="#2CC985"
                            )
                            status_label.pack(pady=3)
                            
                            # Botão para visualizar o relatório
                            view_btn = ctk.CTkButton(
                                buttons_frame,
                                text="Ver Relatório",
                                width=130,
                                height=35,
                                fg_color="#16A085",
                                hover_color="#138D75",
                                command=lambda a=aula, r=relatorio: self.show_visualizar_relatorio(a, r)
                            )
                            view_btn.pack(pady=3)
                        else:
                            # Label para exibir os status do relátório
                            status_label = ctk.CTkLabel(
                                buttons_frame,
                                text="⚠ Rascunho",
                                font=ctk.CTkFont(size=12, weight="bold"),
                                text_color="#F39C12"
                            )
                            status_label.pack(pady=3)
                            
                            # Botão para editar o relatório
                            edit_btn = ctk.CTkButton(
                                buttons_frame,
                                text="Editar",
                                width=130,
                                height=35,
                                fg_color="#9B59B6",
                                hover_color="#7D3C98",
                                command=lambda a=aula, r=relatorio: self.show_criar_editar_relatorio(a, r)
                            )
                            edit_btn.pack(pady=3)
                    else:

                        #Botão para criar relatório
                        create_btn = ctk.CTkButton(
                            buttons_frame,
                            text="Criar Relatório",
                            width=130,
                            height=35,
                            fg_color="#2CC985",
                            hover_color="#25A066",
                            command=lambda a=aula: self.show_criar_editar_relatorio(a)
                        )
                        create_btn.pack(pady=3)
        
        # Botão para voltar a tela enterior
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
    
    # Método para criar e editar relatórios
    def show_criar_editar_relatorio(self, aula, relatorio_existente=None):
        # cria e molda as propriedade de uma nova janela
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Relatório de Aula")
        dialog.geometry("700x600")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)

        # Frame principal com rolagem
        main_scroll = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        # Título que muda de acordo com o uso do método (criar ou editar)
        title_text = "✏️ Editar Relatório" if relatorio_existente else "➕ Criar Relatório"
        
        # Label para exibir esse título
        title = ctk.CTkLabel(
            main_scroll,
            text=title_text,
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=20)
        
        # Frame para exibir as informações para criar e editar o relatório
        info_frame = ctk.CTkFrame(main_scroll)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        # Label para exibir o titulo da aula
        ctk.CTkLabel(
            info_frame,
            text=f"Aula: {aula['titulo']}",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 5), padx=20, anchor="w")
        
        # Informa um metodo para obter os dados da turma
        from backend.turmas_backend import get_detalhes_completos_turma
        
        # Captura o ID, dados e o nome da turma
        turma_id = aula['turma_id']
        turma_detalhes = get_detalhes_completos_turma(turma_id)
        nome = turma_detalhes.get('nome', 'N/A')

        # Label para Exibir o a data e nome da turma    
        ctk.CTkLabel(
            info_frame,
            text=f"Data: {aula['data']} | Turma: {nome}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=(0, 15), padx=20, anchor="w")
        
        # Label para exibir um texto sobre o conteúdo do relatório
        ctk.CTkLabel(
            main_scroll,
            text="Conteúdo do Relatório(máximo 2000 caracteres):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 5), padx=20, anchor="w")
        
        # Text Box para escrever o conteúdo do relatório
        relatorio_text = ctk.CTkTextbox(
            main_scroll,
            height=300,
            wrap="word",
            font=ctk.CTkFont(size=13)
        )
        relatorio_text.pack(padx=20, pady=(0, 15), fill="x")
        
        # Se o relatório já existe ele insere o conteúdo desse relatório dentro do Text Box
        if relatorio_existente:
            relatorio_text.insert("1.0", relatorio_existente.get('texto', ''))
        
        # se o relatório já existe cria um label para exibir a data de criação do relatório 
        if relatorio_existente:
            data_label = ctk.CTkLabel(
                main_scroll,
                text=f"Criado em: {relatorio_existente.get('data_criacao', 'N/A')}",
                font=ctk.CTkFont(size=11),
                text_color="gray"
            )
            data_label.pack(pady=(0, 10))
        
        # Frame para exibir botões
        buttons_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        # Método para salvar um rascunho do relatório
        def salvar_rascunho():
            # Captura o conteúdo do relatório
            texto = relatorio_text.get("1.0", "end-1c").strip()
            
            #Certifica que o conteúdo não está vazio e se tiver vazio retorna um erro
            if not texto:
                messagebox.showerror("Erro", "O relatório não pode estar vazio!")
                return
            
            # Usa uma variável para definir um máximo de caracteres no conteúdo do relatório
            limite_texto = 2000
            # Se passar do limite ele gera um erro
            if len(texto) > limite_texto:
                messagebox.showerror("Erro", f"O conteúdo não pode ter mais de {limite_texto} caracteres.")
                return
            
            # Importa os métodos para criar e editar relatório
            from backend.turmas_backend import criar_relatorio_aula, editar_relatorio_aula
            
            # Ele tenta verificar se o relatório existe e passa os parametros necessários para editar o relatório
            try:
                if relatorio_existente:
                    sucesso = editar_relatorio_aula(relatorio_existente['id'], texto)
                    if sucesso:
                        messagebox.showinfo("Sucesso", "Relatório atualizado com sucesso!")
                        dialog.destroy()
                        self.show_relatorios_aulas()
                    else:
                        # retorna um erro se o método não funcionar
                        messagebox.showerror("Erro", "Erro ao atualizar relatório!")
                else:
                    # Se o relatório ainda não existe e apenas cria um novo
                    # Passa os parametros necessários para criar o relatório
                    relatorio_id = criar_relatorio_aula(
                        aula['turma_id'],
                        aula['id'],
                        self.user_email,
                        texto
                    )
                    # confirma se o relatório foi criado e caso não ele retorna um erro
                    if relatorio_id:
                        messagebox.showinfo("Sucesso", "Relatório salvo como rascunho!")
                        dialog.destroy()
                        self.show_relatorios_aulas()
                    else:
                        messagebox.showerror("Erro", "Erro ao criar relatório!")
            # Se houver um erro durante a tentativa de tentar acessar um dos métodos ou de salver o relatório ele retorna uma excessão
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar relatório: {str(e)}")
        
        # Método para entregar o relátório por definitivo
        def finalizar_relatorio():

            # Captura o conteúdo do relatório
            texto = relatorio_text.get("1.0", "end-1c").strip()
            
            # Ve se o conteúdo não está vazio
            if not texto:
                messagebox.showerror("Erro", "O relatório não pode estar vazio!")
                return
            
            # Verifica se o conteúdo não passou o limite de caracteres
            limite_texto = 2000
            if len(texto) > limite_texto:
                messagebox.showerror("Erro", f"O conteúdo não pode ter mais de {limite_texto} caracteres.")
                return
            
            # Exibe uma caixa de resposta para confirmar o envio do relatório por definitivo
            resposta = messagebox.askyesno(
                "Confirmar Finalização",
                "Ao finalizar, o relatório não poderá mais ser editado.\n\nDeseja continuar?"
            )
            
            # Se a resposta for não e retorna
            if not resposta:
                return
            
            # Importa algumas funções para visualizar e manipular dados
            from backend.turmas_backend import criar_relatorio_aula, editar_relatorio_aula, finalizar_relatorio_aula
            
            # ele tenta executar os mesmo passos para criar e editar o relatório 
            try:
                relatorio_id = None
                
                # edita se o relatório existir ou cria um caso o contrário
                if relatorio_existente:
                    editar_relatorio_aula(relatorio_existente['id'], texto)
                    relatorio_id = relatorio_existente['id']
                else:
                    relatorio_id = criar_relatorio_aula(
                        aula['turma_id'],
                        aula['id'],
                        self.user_email,
                        texto
                    )
                
                # tenta finalizar o relatório e retorna se deu certo ou não
                if relatorio_id:
                    sucesso = finalizar_relatorio_aula(relatorio_id)
                    #retorna uma mensagem de sucesso de funcionar e uma de erro se não funcionar
                    if sucesso:
                        messagebox.showinfo(
                            "Sucesso",
                            "Relatório finalizado com sucesso!\n\nEle não poderá mais ser editado."
                        )
                        dialog.destroy()
                        self.show_relatorios_aulas()
                    else:
                        messagebox.showerror("Erro", "Erro ao finalizar relatório!")
                else:
                   messagebox.showerror("Erro", "Erro ao criar relatório!")
            
            # gera uma excessão caso algo dê errado
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao finalizar relatório: {str(e)}")

        #Botão para salvar
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Salvar Rascunho",
            command=salvar_rascunho,
            width=180,
            height=45,
            fg_color="#3498DB",
            hover_color="#2874A6"
        )
        save_btn.pack(side="left", padx=10)
        
        # Botão para enviar em definitivo
        finalize_btn = ctk.CTkButton(
            buttons_frame,
            text="✓ Finalizar Relatório",
            command=finalizar_relatorio,
            width=180,
            height=45,
            fg_color="#2CC985",
            hover_color="#25A066"
        )
        finalize_btn.pack(side="left", padx=10)

        # Botão para voltar
        back_btn = ctk.CTkButton(
            dialog,
            text="fechar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_relatorios_aulas,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    # Método para visualizar relatório
    def show_visualizar_relatorio(self, aula, relatorio):
        # Cria e personaliza as propriedade de uma nova janela
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Visualizar Relatório")
        dialog.geometry("800x700")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)
        
        # Frame principal com rolagem
        main_scroll = ctk.CTkScrollableFrame(dialog, width=750, height=630)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Label para exibir titúlo
        title = ctk.CTkLabel(
            main_scroll,
            text="📄 Relatório de Aula",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=20)
        
        # Frame para exibir os status do relatório
        status_frame = ctk.CTkFrame(main_scroll, fg_color="#2CC985", corner_radius=10)
        status_frame.pack(pady=10)
        
        # Label para exibir os status de finalizado
        ctk.CTkLabel(
            status_frame,
            text="✓ RELATÓRIO FINALIZADO",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        ).pack(padx=20, pady=8)
        
        # Frame para exibir as informações do relatório
        info_frame = ctk.CTkFrame(main_scroll)
        info_frame.pack(pady=15, padx=40, fill="x")
        
        #Importa as informações da turma e captura elas
        from backend.turmas_backend import get_detalhes_completos_turma
        turma_id = relatorio['turma_id']
        titulo = aula.get('titulo', 'N/A')
        data = aula.get('data_registro', 'N/A')
        turma_detalhes = get_detalhes_completos_turma(turma_id)
        nome = turma_detalhes.get('nome', 'N/A')
        disciplina = turma_detalhes.get('disciplina', 'N/A')

        # cria uma lista para exibir as informações da turma
        info_lines = [
            f"Aula: {titulo}",
            f"Data da Aula: {data}",
            f"Turma: {nome} - {disciplina}",
            f"Criado em: {relatorio.get('data_criacao', 'N/A')}",
            f"Finalizado em: {relatorio.get('data_finalizacao', 'N/A')}"
        ]
        
        # Label para exibi cara linha da lista de informações da turma dentro de um label
        for line in info_lines:
            ctk.CTkLabel(
                info_frame,
                text=line,
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(pady=3, padx=20, anchor="w")
        
        # Label para exibir um titúlo
        ctk.CTkLabel(
            main_scroll,
            text="Conteúdo:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 5), padx=40, anchor="w")
        
        # Text Box que exibe o conteúdo do relatório
        relatorio_text = ctk.CTkTextbox(
            main_scroll,
            width=700,
            height=300,
            font=ctk.CTkFont(size=13)
        )
        #propriedade para modificar a exibição do Text Box
        relatorio_text.pack(padx=40, pady=(0, 20))
        relatorio_text.insert("1.0", relatorio.get('texto', ''))
        relatorio_text.configure(state="disabled")
        
        # Botão pra fechar janela
        close_btn = ctk.CTkButton(
            main_scroll,
            text="Fechar",
            command=dialog.destroy,
            width=200,
            height=45,
            fg_color="gray",
            hover_color="darkgray"
        )
        close_btn.pack(pady=20)
    
    # Metodo para exibir as atividades do professor
    def show_atividades_professor(self):
        self.app.clear_window()
        
        # frame principal
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label para exibir um título
        title_label = ctk.CTkLabel(
            main_frame,
            text="📋 Minhas Atividades",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Importa e captura o método para obter as atividade e entregar realizadas
        from backend.turmas_backend import get_atividades_com_entregas
        atividades = get_atividades_com_entregas(self.user_email)
        
        # Verifica se existe uma atividade e não exibe uma mensagem se sim constroi o resto da interface
        if not atividades:
            ctk.CTkLabel(
                main_frame, 
                text="Nenhuma atividade criada ainda.", 
                text_color="gray"
            ).pack(pady=50)
        else:
            for atividade in atividades:

                # Frama para exibir as atividades
                ativ_frame = ctk.CTkFrame(main_frame)
                ativ_frame.pack(pady=8, padx=40, fill="x")
                
                # Frame para exibir as informações das atividades
                info_frame = ctk.CTkFrame(ativ_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                # Label para exibir os títulos das atividades
                ctk.CTkLabel(
                    info_frame,
                    text=f"📄 {atividade['titulo']}",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    wraplength=380
                ).pack(anchor="w")
                
                # Label pra exibir o nome da turma e disciplina da atividade 
                ctk.CTkLabel(
                    info_frame,
                    text=f"Turma: {atividade['turma_nome']} - {atividade['disciplina']}",
                    font=ctk.CTkFont(size=13),
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                # Label para exibir a data de entrega e o valor da atividade
                ctk.CTkLabel(
                    info_frame,
                    text=f"Entrega: {atividade['data_entrega']} | Valor: {atividade['valor']} pts",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                # Captura os dados de atividade
                total_alunos = atividade['total_alunos']
                entregas = atividade['total_entregas']
                corrigidas = atividade['entregas_corrigidas']
                pendentes = atividade['entregas_pendentes']
                nao_entregaram = total_alunos - entregas
                
                # Verifiica e exibir mensagens de acordo com os status de entrega da atividade
                if entregas == 0:
                    status_text = f"⚠️  Nenhuma entrega ainda ({total_alunos} alunos na turma)"
                    status_color = "#E74C3C"
                elif pendentes > 0:
                    status_text = f"📝 {entregas}/{total_alunos} entregas | {pendentes} aguardando correção | {corrigidas} corrigidas"
                    status_color = "#E67E22"
                else:
                    status_text = f"✅ {entregas}/{total_alunos} entregas | Todas corrigidas"
                    status_color = "#2CC985"
                
                # Label para exibir as mensagem de status da atividade
                ctk.CTkLabel(
                    info_frame,
                    text=status_text,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=status_color
                ).pack(anchor="w", pady=5)
                
                # Botão para ver atividades entregues
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
        
        # Botão para vontal a tela anterior
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
    
    # Método para ver as atividades entregues
    def show_entregas_atividade(self, atividade):
        self.app.clear_window()
        
        # Frame principal
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label com o títilo da atividade
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📝 Entregas: {atividade['titulo']}",
            font=ctk.CTkFont(size=24, weight="bold"),
            wraplength=420
        )
        title_label.pack(pady=(20, 10))
        
        # Label com os dados da atividade
        info_label = ctk.CTkLabel(
            main_frame,
            text=f"Turma: {atividade['turma_nome']} | Valor: {atividade['valor']} pontos | Entrega: {atividade['data_entrega']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info_label.pack(pady=(0, 20))
        
        # Importa o método para ver os detalhes da atividade
        from backend.turmas_backend import get_detalhes_atividade_professor
        detalhes = get_detalhes_atividade_professor(atividade['id'])
        
        # gera um erro se houver um erro no método para pegar os detalhes
        if not detalhes:
            ctk.CTkLabel(main_frame, text="Erro ao carregar detalhes da atividade.", text_color="red").pack(pady=50)
            return
        
        # Frame para ver os detalhes
        resumo_frame = ctk.CTkFrame(main_frame)
        resumo_frame.pack(pady=10, padx=40, fill="x")
        
        # Label para ver os status, total de entregas, total de alunos e vários outros detalhes
        ctk.CTkLabel(
            resumo_frame,
            text=f"📊 Status: {detalhes['total_entregas']}/{detalhes['total_alunos']} entregas | {detalhes['total_corrigidas']} corrigidas | {detalhes['total_pendentes']} pendentes",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=15)
        
        # Cria uma Tab VIew
        tabs = ctk.CTkTabview(
            main_frame, 
            width=900, 
            height=400
        )
        tabs.pack(pady=20, padx=40)
        
        # Adiciona uma tab para as atividades entregues e outra para as não entregues
        tabs.add("✅ Entregas Recebidas")
        tabs.add("⚠️ Não Entregaram")
        
        entregas = detalhes['entregas']

        # Se não tiver atividades entregues ele exibe uma mensagem se não ele constrou a interface
        if not entregas:
            ctk.CTkLabel(tabs.tab("✅ Entregas Recebidas"), text="Nenhuma entrega ainda.", text_color="gray").pack(pady=20)
        else:
            for entrega in entregas:
                
                # Frame para as entregas
                entrega_frame = ctk.CTkFrame(tabs.tab("✅ Entregas Recebidas"))
                entrega_frame.pack(pady=8, padx=10, fill="x")
                
                # Frame para as informações das entregas
                info_frame = ctk.CTkFrame(entrega_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
                
                # Label para ver o nome e RM do aluno que fez a entrega
                ctk.CTkLabel(
                    info_frame,
                    text=f"👤 {entrega['aluno_nome']} (RM: {entrega['aluno_rm']})",
                    font=ctk.CTkFont(size=15, weight="bold")
                ).pack(anchor="w")
                
                # Verifica se a entrega já foi avaliada
                if entrega.get('nota') is not None:
                    status_text = f"✅ Nota: {entrega['nota']:.1f}/{atividade['valor']}"
                    status_color = "#2CC985"
                else:
                    status_text = "⏳ Aguardando Correção"
                    status_color = "#E67E22"
                
                # Label para mostrar a data de entregar e os status de entrega
                ctk.CTkLabel(
                    info_frame,
                    text=f"Entregue em: {entrega['data_entrega']} | Status: {status_text}",
                    font=ctk.CTkFont(size=12),
                    text_color=status_color
                ).pack(anchor="w", pady=2)
                
                # Frame para exibir os botões
                btn_frame = ctk.CTkFrame(entrega_frame, fg_color="transparent")
                btn_frame.pack(side="right", padx=10, pady=10)
                
                # Botão para enviar arquivos
                if entrega.get('arquivo'):
                    ctk.CTkButton(
                        btn_frame,
                        text="📥 Baixar",
                        width=100,
                        height=35,
                        command=lambda e=entrega: self.baixar_entrega(e)
                    ).pack(pady=3)
                
                # Texto que muda caso a atividade ainda não tenha cido avaliada
                btn_text = "✏️ Reavaliar" if entrega.get('nota') is not None else "✓ Avaliar"

                # Botão para avaliar a atividade e com o texto que muda
                ctk.CTkButton(
                    btn_frame,
                    text=btn_text,
                    width=100,
                    height=35,
                    fg_color="#2CC985", 
                    hover_color="#25A066",
                    command=lambda e=entrega: self.avaliar_entrega(e, atividade)
                ).pack(pady=3)
        
        # captura os alunos que não entregam a atividade
        nao_entregaram = detalhes['alunos_nao_entregaram']

        # Se todos tiverem entrega exibe uma mensagem caso contrário exibe os aluno que ainda não entregam a atividade
        if not nao_entregaram:
            ctk.CTkLabel(
                tabs.tab("⚠️ Não Entregaram"), 
                text="✅ Todos os alunos já entregaram!", 
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#2CC985"
            ).pack(pady=20)
        else:
            for aluno in nao_entregaram:

                # Frame para exibir aluno
                aluno_frame = ctk.CTkFrame(tabs.tab("⚠️ Não Entregaram"))
                aluno_frame.pack(pady=5, padx=10, fill="x")
                
                # Label para exibir o nome e RM do aluno
                ctk.CTkLabel(
                    aluno_frame,
                    text=f"⚠️ {aluno['nome']} (RM: {aluno['rm']}) - {aluno['email']}",
                    font=ctk.CTkFont(size=14),
                    text_color="#E74C3C"
                ).pack(anchor="w", padx=20, pady=10)
        
        # Botão para voltar
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
    
    # Método para avaliar a atividade entregue
    def avaliar_entrega(self, entrega, atividade):
        # Cria e usa propriedade para ajustar uma janela
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Avaliar Entrega")
        dialog.geometry("700x600")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)
        
        # Frame principal com colagem
        main_scroll = ctk.CTkScrollableFrame(dialog, width=650, height=630)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Label para mostrar um Título  
        title = ctk.CTkLabel(
            main_scroll,
            text=f"📝 Avaliar Entrega",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 5))
        
        # Label para mostrar o nome e RM do aluno que fez a entrega
        aluno_label = ctk.CTkLabel(
            main_scroll,
            text=f"👤 {entrega['aluno_nome']} (RM: {entrega['aluno_rm']})",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        aluno_label.pack(pady=(0, 20))
        
        # Frame para mostar as informações da entrega
        info_frame = ctk.CTkFrame(main_scroll)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        # Label para mostrar o título da atividade
        ctk.CTkLabel(
            info_frame,
            text=f"📄 Atividade: {atividade['titulo']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=550
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        # Label para mostar o valor da atividade
        ctk.CTkLabel(
            info_frame,
            text=f"Valor da atividade: {atividade['valor']} pontos",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w", padx=15, pady=(0, 5))
        
        # Label para ver a tada de entrega da atividade
        ctk.CTkLabel(
            info_frame,
            text=f"📅 Entregue em: {entrega['data_entrega']}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Frame para ver outras informações
        entrega_frame = ctk.CTkFrame(main_scroll)
        entrega_frame.pack(pady=15, padx=20, fill="both", expand=True)
        
        # Label de título
        ctk.CTkLabel(
            entrega_frame,
            text="📋 Resposta do Aluno:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        # Text Box para ver a resposta do aluno
        resposta_text = ctk.CTkTextbox(
            entrega_frame,
            width=600,
            height=180,
            wrap="word"
        )
        resposta_text.pack(padx=15, pady=(0, 15))
        
        # Captura o comentário feito pelo aluno
        comentario = entrega.get('comentario', '')

        # insere o comentário do aluno e retorna uma mensagem se o retorno estiver vázio
        if comentario:
            resposta_text.insert("1.0", comentario)
        else:
            resposta_text.insert("1.0", "Sem resposta escrita.")
        resposta_text.configure(state="disabled")
        
        # Cria um label para exibir um arquivo caso o aluno tenha feito uma entrega
        if entrega.get('arquivo'):
            arquivo_label = ctk.CTkLabel(
                entrega_frame,
                text=f"📎 Arquivo anexado: {entrega.get('arquivo_nome', 'arquivo')}",
                font=ctk.CTkFont(size=12),
                text_color="#3498DB"
            )
            arquivo_label.pack(anchor="w", padx=15, pady=(0, 10))
            
            # Botão para baixar o arquivo entregue
            ctk.CTkButton(
                entrega_frame,
                text="📥 Baixar Arquivo",
                width=150,
                height=35,
                command=lambda: self.baixar_entrega(entrega)
            ).pack(anchor="w", padx=15, pady=(0, 15))
        else:
            # Label para indicar que nenhum arquivo foi entregue
            ctk.CTkLabel(
                entrega_frame,
                text="📎 Nenhum arquivo anexado",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(anchor="w", padx=15, pady=(0, 15))
        
        # Frame para exibir a avaliação do professor
        avaliacao_frame = ctk.CTkFrame(main_scroll)
        avaliacao_frame.pack(pady=15, padx=20, fill="x")
        
        # Label de título
        ctk.CTkLabel(
            avaliacao_frame,
            text="✏️ Nota:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        # Entry para o professor dar a nota da entrega
        nota_entry = ctk.CTkEntry(
            avaliacao_frame,
            placeholder_text=f"0 a {atividade['valor']}",
            width=300,
            height=40
        )
        
        # verifica se o valor de nota não é vazio
        if entrega.get('nota') is not None:
            nota_entry.insert(0, str(entrega['nota']))
        
        nota_entry.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Label de título
        ctk.CTkLabel(
            avaliacao_frame,
            text="💬 Feedback para o aluno(máximo 1000 caracteres):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        # Text Box para o professor conseguir dar um feedback ao aluno
        feedback_text = ctk.CTkTextbox(
            avaliacao_frame,
            width=600,
            height=120,
            wrap="word"
        )
        
        # Captura o texto do feedback se houver um
        if entrega.get('feedback'):
            feedback_text.insert("1.0", entrega['feedback'])
        
        feedback_text.pack(padx=15, pady=(0, 20))
        
        # método para salvar a avialiação do proessor
        def salvar_avaliacao():
            # Captura a nota e o feedback atribuidos a entrega
            nota = nota_entry.get().strip()
            feedback = feedback_text.get("1.0", "end-1c").strip()
            
            # verifica se o campo nota não está vazio
            if not nota:
                messagebox.showerror("Erro", "A nota é obrigatória!")
                return
            
            # tanta verificar e análizar a nota e se hover um erro gera um excessão de valor errado para nota
            try:
                nota_float = float(nota)
                if nota_float < 0 or nota_float > float(atividade['valor']):
                    messagebox.showerror("Erro", f"Nota deve estar entre 0 e {atividade['valor']}!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Nota inválida! Use apenas números.")
                return
            
            # Verifica a quantidade de caracteres e se ela não ultrapassa o limite
            limite_texto = 1000
            if len(feedback) > limite_texto:
                messagebox.showerror("Erro", f"O conteúdo não pode ter mais de {limite_texto} caracteres.")
                return 
            
            # importo o método para avaliar e salvar a entrega
            from backend.turmas_backend import avaliar_entrega
            sucesso = avaliar_entrega(entrega['id'], nota_float, feedback)
            
            # Se funcioar exibe mensaem de sucesso casos contrário retorna um erro
            if sucesso:
                messagebox.showinfo("Sucesso", "Avaliação salva com sucesso!")
                dialog.destroy()
                self.show_entregas_atividade(atividade)
            else:
                messagebox.showerror("Erro", "Erro ao salvar avaliação!")
        
        # Botão para salvar a avaliação
        ctk.CTkButton(
            main_scroll,
            text="💾 Salvar Avaliação",
            command=salvar_avaliacao,
            width=200,
            height=50,
            fg_color="#2CC985",
            hover_color="#25A066",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=25)

        # Botão para fechar a janela atual
        back_btn = ctk.CTkButton(
            main_scroll,
            text="fechar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=dialog.destroy,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    # Método para baixar o arquivo da entrega
    def baixar_entrega(self, entrega):
        # ferifica se um arquivo foi entregue
        if entrega.get('arquivo'):
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=os.path.basename(entrega['arquivo']),
                title="Salvar arquivo"
            )
            # salva o caminho do arquivo e depois baixa ele
            if save_path:
                from backend.turmas_backend import baixar_arquivo_entrega
                sucesso = baixar_arquivo_entrega(entrega['id'], save_path)
                if sucesso:
                    messagebox.showinfo("Sucesso", "Arquivo baixado com sucesso!")
                else:
                    messagebox.showerror("Erro", "Erro ao baixar arquivo!")
        else:
            # exibe uma mensagem se não houver um arquivo entregue
            messagebox.showinfo("Info", "Esta entrega não possui arquivo anexado.")
    
    # Metodo para ver as notas e frequêcia dos alunos
    def show_notas_frequencia(self):
        self.app.clear_window()
        
        # Frame principal com rolagem
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label de titulo
        title_label = ctk.CTkLabel(
            main_frame,
            text="📊 Notas e Frequência",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Importa as turmas do professor
        from backend.turmas_backend import get_turmas_professor
        turmas = get_turmas_professor(self.user_email)
        
        # Cria uma frame pra cada turma que o professor possui
        for turma in turmas:
            turma_frame = ctk.CTkFrame(main_frame)
            turma_frame.pack(pady=10, padx=40, fill="x")
            
            # Label com o nome da turma
            ctk.CTkLabel(
                turma_frame,
                text=f"📖 {turma['nome']}",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(anchor="w", padx=20, pady=(15, 5))
            
            # Botão par ver o Boletim da turma
            ctk.CTkButton(
                turma_frame,
                text="Ver Boletim da Turma",
                width=200,
                command=lambda t=turma: self.show_boletim_turma(t)
            ).pack(anchor="w", padx=20, pady=(5, 15))
        
        # Botão para voltar a tela anterior
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
    
    # Método para ver o boletim da turma
    def show_boletim_turma(self, turma):
        self.app.clear_window()
        
        # Frame principal com rolagem
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titulo com o nome da turma
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📊 Boletim: {turma['nome']}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        #Importa o metodo para ver o boletim da turma e captura o valor do boletim
        from backend.turmas_backend import get_boletim_turma
        boletim = get_boletim_turma(turma['id'])
        
        #Cria um frame para cada aluno 
        for aluno_data in boletim:
            aluno_frame = ctk.CTkFrame(main_frame)
            aluno_frame.pack(pady=8, padx=40, fill="x")
            
            # Label com o nome e RM do aluno
            ctk.CTkLabel(
                aluno_frame,
                text=f"👤 {aluno_data['nome']} (RM: {aluno_data['rm']})",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", padx=20, pady=(10, 5))
            
            # Captura media, frequencia e status do aluno e suas notas
            media = aluno_data['media'] if aluno_data['media'] else 0
            frequencia = aluno_data['frequencia']
            status = aluno_data.get('status', 'Sem notas')
            
            # Exibe um status diferente a partir do valor de status do aluno
            if status == 'Aprovado':
                status_color = "#2CC985"
                status_icon = "✅"
            elif 'Reprovado' in status:
                status_color = "#E74C3C"
                status_icon = "❌"
            else:
                status_color = "gray"
                status_icon = "⏳"
            
            # Label para exbir a média frequência e status do aluno
            ctk.CTkLabel(
                aluno_frame,
                text=f"Média: {media:.2f} | Frequência: {frequencia:.1f}% | {status_icon} {status}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=status_color
            ).pack(anchor="w", padx=20, pady=(2, 10))
        
        # Botão para voltar
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
    
    # Método para criar atividades
    def show_criar_atividade(self, turma=None):
        # cria e personaliza uma janela
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Criar Nova Atividade")
        dialog.geometry("700x600")
        dialog.grab_set()
        dialog.resizable(height=False, width=False)
       
       # Frame principal
        main_scroll = ctk.CTkScrollableFrame(dialog, corner_radius=0)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label de titulo
        title = ctk.CTkLabel(
            main_scroll,
            text="➕ Criar Nova Atividade",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        # Frame para exibir um formulário
        form_frame = ctk.CTkFrame(main_scroll)
        form_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Label para exibir turma
        ctk.CTkLabel(
            form_frame,
            text="Turma:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        #importa um metodo para ver as turmas do professor e captura esse valor
        from backend.turmas_backend import get_turmas_professor
        turmas = get_turmas_professor(self.user_email)
        
        # captura os nomes e disciplinas das turmas
        turma_var = ctk.StringVar()
        turma_options = [f"{t['nome']} - {t['disciplina']}" for t in turmas]
        turma_map = {f"{t['nome']} - {t['disciplina']}": t for t in turmas}
        
        # Verifica se há turmas e exibe ela se não exibe nada
        if turma:
            turma_var.set(f"{turma['nome']} - {turma['disciplina']}")
        elif turmas:
            turma_var.set(turma_options[0])
        
        # Gera um menu de opções para exibir as turmas
        turma_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=turma_var,
            values=turma_options,
            width=600,
            height=40
        )
        turma_menu.pack(padx=20, pady=(0, 15))
        
        # Cria um limete de caracteres e uma variavel de sring
        limite_titulo = 46
        titulo_var = ctk.StringVar()

        # Label para exibir titulo
        ctk.CTkLabel(
            form_frame,
            text="Título da Atividade:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        # Entry par escrever o titulo da atividade e o texto inserido é passado para a varivel string
        titulo_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Trabalho sobre Funções Quadráticas",
            width=600,
            height=40,
            textvariable=titulo_var
        )
        titulo_entry.pack(padx=20, pady=(0, 15))
        # Verifica a quantidade de caracteres na string var de titulo usando um metodo que não permite inserir mais caracteres quando passa o limite
        titulo_var.trace_add("write", self.limitar_caracteres(titulo_var, limite_titulo))
        
        # Label de titulo
        ctk.CTkLabel(
            form_frame,
            text="Descrição(máximo 1000 caracteres):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        # Text Box para escrever a descrição da atividade
        descricao_text = ctk.CTkTextbox(
            form_frame,
            width=600,
            height=150,
            wrap="word",
        )
        descricao_text.pack(padx=20, pady=(0, 15))
        
        # Label de titulo
        ctk.CTkLabel(
            form_frame,
            text="Data de Entrega:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        #Captura a data do dia atual
        from datetime import timedelta
        data_sugerida = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
        
        # Entry para colocar data
        data_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="DD/MM/AAAA",
            width=600,
            height=40
        )
        # Escreve a data atual na entry como sugestão
        data_entry.insert(0, data_sugerida)
        data_entry.pack(padx=20, pady=(0, 15))
        
        # Cria um limete de caracteres e uma variavel de sring
        limite_valor = 3
        valor_var = ctk.StringVar()

        # Label de título
        ctk.CTkLabel(
            form_frame,
            text="Valor (pontos):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        # Entry para escrever o valor da atividade
        valor_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: 10",
            width=600,
            height=40,
            textvariable=valor_var
        )
        valor_entry.pack(padx=20, pady=(0, 15))
        valor_var.trace_add("write", self.limitar_caracteres(valor_var, limite_valor))
        
        arquivo_path = None
        # Label para arquivo 
        arquivo_label = ctk.CTkLabel(
            form_frame,
            text="Nenhum arquivo selecionado",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        # Metodo para selecioar um arquivo
        def selecionar_arquivo():
            nonlocal arquivo_path
            # Pega o caminho do arquivo e define os formatos de arquivo permitido
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
        
        # Botão para anexar o arquivo
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
        
        # Método para salvar a atividade
        def salvar_atividade():
            # Seleciona a turma em que a atividade vai ser salva e exibe uma mensagem erro se não encontrar a turma
            turma_selecionada = turma_map.get(turma_var.get())
            if not turma_selecionada:
                messagebox.showerror("Erro", "Selecione uma turma!")
                return
            
            # Captura as propriedades da atividade
            titulo = titulo_var.get().strip().title()
            descricao = descricao_text.get("1.0", "end-1c").strip()
            data_entrega = data_entry.get().strip()
            valor = valor_var.get().strip()
            
            # Verifica se todos os campos foram preenchidos
            if not all([titulo, descricao, data_entrega, valor]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return

            # Verifica se o limite de caracteres não foi ecedido 
            limite_texto = 1000
            if len(descricao) > limite_texto:
                messagebox.showerror("Erro", f"O conteúdo não pode ter mais de {limite_texto} caracteres.")
                return 
            
            # Tenta verificar o valor da atividade e gera um erro se for menor que zero ou gera uma excessão se o valor for inválido
            try:
                valor_float = float(valor)
                if valor_float <= 0:
                    messagebox.showerror("Erro", "O valor deve ser maior que zero!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
                return
            
            #Importo método para criar atividade e passar os paramentros para criar a atividade
            from backend.turmas_backend import criar_atividade
            atividade_id = criar_atividade(
                turma_selecionada['id'],
                titulo,
                descricao,
                data_entrega,
                valor_float,
                arquivo_path
            )
            
            # verifica se a atividade for salva com sucesso caso contrário exibe um erro
            if atividade_id:
                messagebox.showinfo("Sucesso", "Atividade criada com sucesso!")
                dialog.destroy()
                self.show_atividades_professor()
            else:
                messagebox.showerror("Erro", "Erro ao criar atividade!")
        
         # Botão para criar a atividade
        ctk.CTkButton(
            main_scroll,
            text="✓ Criar Atividade",
            command=salvar_atividade,
            width=200,
            height=50,
            fg_color="#2CC985",
            hover_color="#25A066"
        ).pack(pady=20)

        # Botão para voltar a tela anterior
        back_btn = ctk.CTkButton(
            dialog,
            text="← Voltar",
            font=ctk.CTkFont(size=16),
            width=200,
            height=50,
            command=self.show_atividades_professor,
            fg_color="gray",
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    # Método de estilos
    def darken_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"