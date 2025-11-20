import customtkinter as ctk 
from tkinter import messagebox, filedialog 
from datetime import datetime 
from backend.turmas_backend import get_turmas_aluno, get_atividades_turma 

# Tenta importar as classes necessárias da biblioteca ReportLab para gerar documentos PDF.
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    # Define uma flag para indicar se o ReportLab está disponível.
    REPORTLAB_AVAILABLE = True
except ImportError:
    # Se ReportLab não estiver instalado, a flag é definida como False.
    # Funções de exportação de PDF devem checar esta flag antes de tentar usar o ReportLab.
    REPORTLAB_AVAILABLE = False

class TelasAluno:
    
    # Método construtor da classe
    def __init__(self, app, user_email):
        # Armazena a referência à janela principal da aplicação (ou objeto App)
        self.app = app 
        # Armazena o email do usuário logado para buscar dados específicos
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

    # Método principal que exibe o menu inicial do aluno
    def show_aluno_menu(self):
        # Limpa todos os widgets existentes na janela principal da aplicação
        self.app.clear_window() 

        # Cria um frame com barra de rolagem para acomodar o conteúdo (útil para telas menores)
        scroll_container = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Frame principal dentro do container de rolagem
        main_frame = ctk.CTkFrame(scroll_container, corner_radius=0)
        main_frame.pack(padx=20, pady=20, fill="x")

        # Importa as funções de dados necessárias (isso pode ser movido para o topo do arquivo)
        from backend.turmas_backend import get_user_data
        from database.banco import users_db
        # Tenta obter os dados do usuário do banco de dados ou chama a função de busca
        user_data = users_db.get(self.user_email, get_user_data(self.user_email))

        # Cabeçalho de Boas-Vindas
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=20, pady=(20, 30))

        # Rótulo de título com o nome do aluno e emoji
        title_label = ctk.CTkLabel(
            header_frame, 
            text=f"👨‍🎓 Bem-vindo, {user_data['nome']}!", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)

        # Rótulo condicional para o RM (Registro de Matrícula), se existir
        if user_data.get('rm'):
            rm_label = ctk.CTkLabel(
                header_frame, 
                text=f"RM: {user_data['rm']}", 
                font=ctk.CTkFont(size=16, weight="bold"), 
                text_color="#3498DB"
            )
            rm_label.pack(pady=5)

        # Rótulo para o email do aluno
        subtitle_label = ctk.CTkLabel(
            header_frame, 
            text=f"Email: {self.user_email}", 
            font=ctk.CTkFont(size=14), 
            text_color="gray"
        )
        subtitle_label.pack()

        # Botões de Navegação do Menu
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(expand=True)

        # Lista de tuplas: (Texto do Botão, Comando de Função, Cor)
        buttons_data = [
            ("📚 Turmas", self.show_turmas_aluno, "#3498DB"), # Azul: Turmas
            ("📋 Atividades Pendentes", self.show_atividades_pendentes, "#E67E22"), # Laranja: Pendentes
            ("✅ Atividades Concluídas", self.show_atividades_entregues, "#2CC985"), # Verde: Concluídas
            ("📊 Boletim Escolar", self.show_boletim_completo, "#9B59B6"), # Roxo: Boletim
            ("🚪 Sair", lambda: self.app.logout(), "#E74C3C") # Vermelho: Sair
        ]
        
        # Cria e empacota os botões dinamicamente
        for text, command, color in buttons_data:
            btn = ctk.CTkButton(
                buttons_frame, 
                text=text, 
                font=ctk.CTkFont(size=16, weight="bold"), 
                width=400, 
                height=55,  
                fg_color=color, 
                hover_color=self.darken_color(color), # Assume a existência de darken_color
                command=command
            )
            btn.pack(pady=8)
    
    # Método para exibir a lista de turmas em que o aluno está matriculado
    def show_turmas_aluno(self):
        self.app.clear_window()

        # Cria o frame de rolagem para a lista de turmas
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título da tela
        title_label = ctk.CTkLabel(
            main_frame, 
            text="📚 Minhas Turmas", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        # Busca as turmas do aluno no backend
        from backend.turmas_backend import get_turmas_aluno # Importação local desnecessária se já estiver no topo
        turmas = get_turmas_aluno(self.user_email)

        # Verifica se há turmas e exibe a mensagem apropriada
        if not turmas:
            empty_label = ctk.CTkLabel(
                main_frame, 
                text="Você ainda não está matriculado em nenhuma turma.\nAguarde seu professor adicioná-lo a uma turma!", 
                font=ctk.CTkFont(size=16), 
                text_color="gray"
            )
            empty_label.pack(pady=50)
        else:
            # Itera sobre cada turma encontrada
            for turma in turmas:
                # Frame individual para cada turma
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=10, padx=40, fill="x")

                # Frame para as informações da turma (para alinhamento à esquerda)
                info_frame = ctk.CTkFrame(turma_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)

                # Rótulos com nome, disciplina e professor/período da turma
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

                professor_label = ctk.CTkLabel(
                    info_frame, 
                    text=f"Professor: {turma['professor_nome']} | {turma['periodo']}", 
                    font=ctk.CTkFont(size=12), 
                    text_color="gray"
                )
                professor_label.pack(anchor="w", pady=2)

                # Botão para ver detalhes da turma (chama a próxima tela)
                view_btn = ctk.CTkButton(
                    turma_frame, 
                    text="Ver Detalhes",
                    width=120, height=40, 
                    # Usa lambda para passar o objeto 'turma' como argumento para a função
                    command=lambda t=turma: self.show_detalhes_turma_aluno(t)
                )
                view_btn.pack(side="right", padx=10, pady=10)

        # Botão para voltar ao menu principal do aluno
        back_btn = ctk.CTkButton(
            main_frame, 
            text="← Voltar", 
            font=ctk.CTkFont(size=16), 
            width=200, 
            height=50, 
            fg_color="gray", 
            hover_color="darkgray",
            command=self.show_aluno_menu 
        )
        back_btn.pack(pady=30)
    
    # Método para exibir os detalhes de uma turma específica
    def show_detalhes_turma_aluno(self, turma):
        self.app.clear_window()

        # Cria o frame de rolagem
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título e informações da turma
        title_label = ctk.CTkLabel(
            main_frame, 
            text=f"📖 {turma['nome']}", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        info_label = ctk.CTkLabel(
            main_frame, 
            text=f"{turma['disciplina']} | Prof. {turma['professor_nome']} | {turma['periodo']}", 
            font=ctk.CTkFont(size=14), 
            text_color="gray"
        )
        info_label.pack(pady=(0, 30))

        # Abas de Visualização (Aulas, Atividades, Notas)
        tabs = ctk.CTkTabview(
            main_frame, 
            width=800, 
            height=400
        )
        tabs.pack(pady=20, padx=40)

        tabs.add("📝 Aulas Ministradas")
        tabs.add("📋 Atividades")
        tabs.add("📊 Minhas Notas")

        # Busca as aulas registradas para a turma
        from backend.turmas_backend import get_aulas_turma, get_atividades_turma_aluno, get_notas_aluno_turma
        aulas = get_aulas_turma(turma['id'])

        if not aulas:
            ctk.CTkLabel(tabs.tab("📝 Aulas Ministradas"), text="Nenhuma aula registrada ainda.", text_color="gray").pack(pady=20)
        else:
            # Itera e exibe cada aula em um frame
            for aula in aulas:
                aula_frame = ctk.CTkFrame(tabs.tab("📝 Aulas Ministradas"))
                aula_frame.pack(pady=5, padx=10, fill="x")

                # Título da aula e data
                ctk.CTkLabel(
                    aula_frame, 
                    text=f"📅 {aula['data']} - {aula['titulo']}", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    wraplength=500
                ).pack(anchor="w", padx=20, pady=(10, 5))
                
                # Campo de texto (somente leitura) com o conteúdo da aula
                conteudo_aula = ctk.CTkTextbox(
                    aula_frame,
                    font=ctk.CTkFont(size=13),
                    text_color="gray",
                    wrap="word",
                    height=120,
                )
                conteudo_aula.pack(anchor="w", pady=(5, 2),fill="x", expand=True)
                conteudo_aula.insert("0.0", aula['conteudo'])
                conteudo_aula.configure(state="disabled") # Desabilita edição

        # Busca as atividades da turma, incluindo o status de entrega do aluno
        atividades = get_atividades_turma_aluno(turma['id'], self.user_email)

        if not atividades:
            ctk.CTkLabel(tabs.tab("📋 Atividades"), text="Nenhuma atividade disponível.", text_color="gray").pack(pady=20)
        else:
            # Itera e exibe cada atividade
            for atividade in atividades:
                ativ_frame = ctk.CTkFrame(tabs.tab("📋 Atividades"))
                ativ_frame.pack(pady=5, padx=10, fill="x")

                info_frame = ctk.CTkFrame(ativ_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=10)

                # Define o ícone de status (Entregue ou Pendente)
                status_icon = "✅" if atividade['entregue'] else "⏰"

                # Título da atividade com status
                ctk.CTkLabel(
                    info_frame, 
                    text=f"{status_icon} {atividade['titulo']}", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    wraplength=400
                ).pack(anchor="w")

                # Prazo e valor da atividade
                ctk.CTkLabel(
                    info_frame, 
                    text=f"Prazo: {atividade['data_entrega']} | Valor: {atividade['valor']} pontos", 
                    font=ctk.CTkFont(size=12), 
                    text_color="gray"
                ).pack(anchor="w", pady=2)

                # Verifica se a atividade foi entregue
                if atividade['entregue']:
                    # Se entregue e com nota, exibe a nota
                    if atividade.get('nota'):
                        ctk.CTkLabel(
                            info_frame, 
                            text=f"Nota: {atividade['nota']}/{atividade['valor']}", 
                            font=ctk.CTkFont(size=12, weight="bold"), 
                            text_color="#2CC985"
                        ).pack(anchor="w", pady=2)
                    # Se entregue e sem nota, exibe "Aguardando correção"
                    else:
                        ctk.CTkLabel(
                            info_frame, 
                            text="Aguardando correção", 
                            font=ctk.CTkFont(size=12), 
                            text_color="#E67E22"
                        ).pack(anchor="w", pady=2)
                    
                    # Botão para ver a entrega
                    ctk.CTkButton(
                        ativ_frame, 
                        text="Ver Entrega", 
                        width=100, 
                        height=30, 
                        command=lambda a=atividade: self.show_ver_entrega(a)
                    ).pack(side="right", padx=5, pady=5)
                # Se não foi entregue, exibe o botão "Entregar"
                else:
                    ctk.CTkButton(
                        ativ_frame, 
                        text="Entregar", 
                        width=100, 
                        height=30, 
                        fg_color="#2CC985", 
                        hover_color="#25A066",
                        command=lambda a=atividade: self.show_entregar_atividade(a)
                    ).pack(side="right", padx=5, pady=5)

        # Busca as notas do aluno para esta turma
        notas = get_notas_aluno_turma(turma['id'], self.user_email)

        if not notas:
            ctk.CTkLabel(
                tabs.tab("📊 Minhas Notas"), 
                text="Nenhuma nota disponível ainda.", 
                text_color="gray"
            ).pack(pady=20)
        else:
            # Calcula a média ponderada (ou simples, dependendo de como 'valor' é usado)
            # Média = (Soma das Notas) / (Soma dos Valores) * 10
            media_total = sum([nota['nota'] for nota in notas]) 
            valor_total = sum([nota['valor'] for nota in notas])
            media = (media_total / valor_total * 10) if valor_total > 0 else 0

            # Exibe a média e muda a cor com base no resultado (e.g., >= 7 é verde/aprovado)
            media_label = ctk.CTkLabel(
                tabs.tab("📊 Minhas Notas"), 
                text=f"📊 Média: {media:.2f}", 
                font=ctk.CTkFont(size=18, weight="bold"), 
                text_color="#2CC985" if media >= 7 else "#E74C3C"
            )
            media_label.pack(pady=20)

            # Exibe cada nota individual em um frame
            for nota in notas:
                nota_frame = ctk.CTkFrame(tabs.tab("📊 Minhas Notas"))
                nota_frame.pack(pady=5, padx=10, fill="x")

                ctk.CTkLabel(
                    nota_frame, 
                    text=f"📝 {nota['atividade']}: {nota['nota']}/{nota['valor']}", # Título da atividade e nota
                    font=ctk.CTkFont(size=13)
                ).pack(anchor="w", padx=20, pady=10)

        # Botão para voltar para a lista de turmas
        back_btn = ctk.CTkButton(
            main_frame, text="← Voltar", 
            font=ctk.CTkFont(size=16), 
            width=200, 
            height=50, 
            command=self.show_turmas_aluno, 
            fg_color="gray", 
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)
    
    # Método para exibir a tela de entrega de uma atividade pendente
    def show_entregar_atividade(self, atividade):
        self.app.clear_window()
        
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título da atividade a ser entregue
        title_label = ctk.CTkLabel(
            main_frame, 
            text=f"📤 Entregar: {atividade['titulo']}", 
            font=ctk.CTkFont(size=24, weight="bold"),
            wraplength=400
        )
        title_label.pack(pady=(20, 10))

        # Informações de prazo e valor
        info_label = ctk.CTkLabel(
            main_frame, 
            text=f"Prazo: {atividade['data_entrega']} | Valor: {atividade['valor']} pontos", 
            font=ctk.CTkFont(size=14), 
            text_color="gray"
        )
        info_label.pack(pady=(0, 20))

        # Frame de conteúdo para descrição e resposta
        desc_frame = ctk.CTkFrame(main_frame)
        desc_frame.pack(pady=10, padx=50, fill="both", expand=True)

        # Exibe a descrição da atividade (somente leitura)
        ctk.CTkLabel(
            desc_frame, 
            text="Descrição da Atividade:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))

        desc_text = ctk.CTkTextbox(
            desc_frame, 
            height=150,
            font=ctk.CTkFont(size=13),
            text_color="gray",
            wrap="word",
        )
        desc_text.pack(anchor="w", pady=(5, 2), fill="x", expand=True)
        desc_text.insert("0.0", atividade['descricao'])
        desc_text.configure(state="disabled")

        # Campo para o aluno digitar a resposta
        ctk.CTkLabel(
            desc_frame, 
            text="Sua Resposta(máximo 2000 caracteres): ", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))

        resposta_text = ctk.CTkTextbox(
            desc_frame,
            height=150,
            wrap="word",
        )
        resposta_text.pack(pady=5, padx=20, fill="both", expand=True)

        # Rótulo para exibir o arquivo selecionado
        file_label = ctk.CTkLabel(
            desc_frame, 
            text="Nenhum arquivo selecionado", 
            font=ctk.CTkFont(size=12), text_color="gray"
        )
        file_label.pack(pady=10)
        # Dicionário para armazenar o caminho do arquivo selecionado (mutável)
        selected_file = {"path": None}
        
        # Função para abrir a caixa de diálogo de seleção de arquivo
        def select_file():
            filepath = filedialog.askopenfilename(title="Selecionar Arquivo", filetypes=[("Todos os arquivos", "*.*"), ("PDFs", "*.pdf"), ("Documentos", "*.doc;*.docx"), ("Imagens", "*.png;*.jpg;*.jpeg")])
            
            if filepath:
                selected_file["path"] = filepath
                # Atualiza o rótulo para mostrar o nome do arquivo
                file_label.configure(text=f"Arquivo: {filepath.split('/')[-1]}")

        # Botão para anexar arquivo
        file_btn = ctk.CTkButton(
            desc_frame, 
            text="📎 Anexar Arquivo (Opcional)", 
            width=200, 
            command=select_file
        )
        file_btn.pack(pady=10)

        # Função que processa a entrega da atividade
        def process_entrega():
            # Obtém e limpa a resposta de texto
            resposta = resposta_text.get("1.0", "end-1c").strip()
            limite_texto = 2000

            # Validação: requer texto ou arquivo
            if not resposta and not selected_file["path"]:
                messagebox.showerror("Erro", "Você precisa escrever uma resposta ou anexar um arquivo!")
                return
            
            # Validação: limite de caracteres
            if len(resposta) > limite_texto:
                messagebox.showerror("Erro", f"O conteúdo não pode ter mais de {limite_texto} caracteres.")
                return
            
            # Chama a função de backend para registrar a entrega
            from backend.turmas_backend import entregar_atividade # Importação local
            sucesso, mensagem = entregar_atividade(atividade['id'], self.user_email, selected_file["path"], resposta)
            
            # Exibe o resultado e navega para a tela de atividades pendentes
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.show_atividades_pendentes()
            else:
                messagebox.showerror("Erro", mensagem)

        # Botões de Ação (Entregar e Cancelar)
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)

        submit_btn = ctk.CTkButton(
            buttons_frame, 
            text="✓ Entregar", 
            font=ctk.CTkFont(size=16, weight="bold"),
            width=190, 
            height=50, 
            command=process_entrega, # Chama a função de processamento
            fg_color="#2CC985", 
            hover_color="#25A066"
        )
        submit_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(
            buttons_frame, 
            text="← Cancelar", 
            font=ctk.CTkFont(size=16),
            width=190, 
            height=50, 
            # Volta para a tela de atividades pendentes
            command=self.show_atividades_pendentes, 
            fg_color="gray", 
            hover_color="darkgray"
        )
        cancel_btn.pack(side="left", padx=10)
    
    # Método para exibir os detalhes de uma atividade já entregue (incluindo nota/feedback)
    def show_ver_entrega(self, atividade):
        self.app.clear_window()

        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título da atividade
        title_label = ctk.CTkLabel(
            main_frame, text=f"📄 {atividade['titulo']}", 
            font=ctk.CTkFont(size=24, weight="bold"),
            wraplength=400
        )
        title_label.pack(pady=(20, 10))

        # Data de entrega
        info_label = ctk.CTkLabel(
            main_frame, 
            text=f"Entregue em: {atividade['data_entrega']}", 
            font=ctk.CTkFont(size=14), text_color="gray")
        info_label.pack(pady=(0, 20))

        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(pady=10, padx=50, fill="both", expand=True)

        # Resposta do Aluno
        ctk.CTkLabel(
            content_frame, 
            text="Sua Resposta:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))

        resposta_text = ctk.CTkTextbox(
            content_frame, 
            height=150, 
            state="normal"
        )
        resposta_text.pack(pady=5, padx=20, fill="both", expand=True)
        # Insere o texto da resposta (usa 'comentario' para a resposta textual do aluno)
        resposta_text.insert("1.0", atividade.get('comentario', 'Nenhuma resposta escrita'))
        resposta_text.configure(state="disabled")

        # Exibe o arquivo anexado, se houver
        if atividade.get('arquivo'):
            ctk.CTkLabel(
                content_frame, 
                text=f"📎 Arquivo anexado: {atividade.get('arquivo_nome', 'arquivo')}", 
                font=ctk.CTkFont(size=12), 
                text_color="gray"
            ).pack(pady=10)
        
        # Nota e Feedback do Professor
        if atividade.get('nota'):
            # Se houver nota, exibe a nota em um frame verde
            nota_frame = ctk.CTkFrame(
                content_frame, 
                fg_color="#2CC985"
            )
            nota_frame.pack(pady=20, padx=20, fill="x")

            ctk.CTkLabel(
                nota_frame, 
                text=f"⭐ Nota: {atividade['nota']}/{atividade['valor']}", 
                font=ctk.CTkFont(size=18, weight="bold"), 
                text_color="white"
            ).pack(pady=15)

            # Exibe o feedback do professor, se houver
            if atividade.get('feedback'):
                ctk.CTkLabel(
                    content_frame, 
                    text="Feedback do Professor:", 
                    font=ctk.CTkFont(size=14, weight="bold")
                ).pack(anchor="w", padx=20, pady=(20, 5))

                feedback_text = ctk.CTkTextbox(
                    content_frame, 
                    height=100, 
                    state="normal"
                )
                feedback_text.pack(pady=5, padx=20, fill="x")
                feedback_text.insert("1.0", atividade['feedback'])
                feedback_text.configure(state="disabled")
        else:
            # Se não houver nota, exibe "Aguardando Correção" em um frame laranja
            status_frame = ctk.CTkFrame(content_frame, fg_color="#E67E22")
            status_frame.pack(pady=20, padx=20, fill="x")

            ctk.CTkLabel(
                status_frame, 
                text="⏳ Aguardando Correção", 
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="white"
            ).pack(pady=15)

        # Botão para voltar para a lista de atividades entregues
        back_btn = ctk.CTkButton(
            main_frame, 
            text="← Voltar", 
            font=ctk.CTkFont(size=16), 
            width=200, 
            height=50, 
            fg_color="gray", 
            hover_color="darkgray",
            # Chama o método para voltar para a tela de atividades concluídas (entregues)
            command=self.show_atividades_entregues 
        )
        back_btn.pack(pady=30)
    
    def show_atividades_pendentes(self):
        # 1. Limpa a janela principal para renderizar o novo conteúdo.
        self.app.clear_window()

        # 2. Cria um frame rolável principal para acomodar a lista de atividades.
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 3. Rótulo de título para a seção.
        title_label = ctk.CTkLabel(
            main_frame, 
            text="📋 Atividades Pendentes", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        # 4. Obtém as turmas das quais o aluno faz parte, usando o email do usuário.
        turmas = get_turmas_aluno(self.user_email)

        # 5. Importa as funções e a constante de arquivo para entregas.
        from backend.turmas_backend import carregar_json, ENTREGAS_FILE
        # 6. Carrega os dados de todas as entregas e extrai o dicionário 'entregas'.
        entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})

        # 7. Inicializa a lista que armazenará as atividades que ainda não foram entregues.
        atividades = []

        # 8. Loop principal para verificar as atividades pendentes.
        for turma in turmas:
            # 8.1. Obtém todas as atividades da turma atual.
            atividades_turma = get_atividades_turma(turma['id'])
            for atividade in atividades_turma:
                # 8.2. Flag para indicar se o aluno já entregou esta atividade.
                ja_entregou = False
                # 8.3. Percorre todas as entregas para verificar se há uma correspondente.
                for entrega in entregas.values():
                    if (entrega.get('atividade_id') == atividade['id'] and 
                        entrega.get('aluno_email') == self.user_email):
                        # 8.4. Se encontrar uma entrega para esta atividade e este aluno, marca como entregue.
                        ja_entregou = True
                        break
                
                # 8.5. Se a atividade não foi entregue, adiciona-a à lista de pendentes.
                if not ja_entregou:
                    ativ_copy = atividade.copy()
                    # 8.6. Adiciona informações da turma para exibição.
                    ativ_copy['turma_nome'] = turma['nome']
                    ativ_copy['disciplina'] = turma['disciplina']
                    atividades.append(ativ_copy)

        # 9. Exibição das atividades na interface.
        if not atividades:
            # 9.1. Mensagem de sucesso se não houver atividades pendentes.
            empty_label = ctk.CTkLabel(main_frame, text="Parabéns! Você não possui atividades pendentes. 🎉", font=ctk.CTkFont(size=16), text_color="gray")
            empty_label.pack(pady=50)
        else:
            # 9.2. Cria um widget para cada atividade pendente.
            for atividade in atividades:
                ativ_frame = ctk.CTkFrame(main_frame)
                ativ_frame.pack(pady=10, padx=40, fill="x")

                # Frame para as informações de texto.
                info_frame = ctk.CTkFrame(ativ_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)

                # Rótulo do Título da Atividade.
                ctk.CTkLabel(
                    info_frame, text=f"⏰ {atividade['titulo']}", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    wraplength=400
                ).pack(anchor="w")

                # Rótulo com o Nome da Turma e Prazo.
                ctk.CTkLabel(
                    info_frame, 
                    text=f"Turma: {atividade.get('turma_nome', 'N/A')} | Prazo: {atividade['data_entrega']}", 
                    font=ctk.CTkFont(size=13), text_color="gray"
                ).pack(anchor="w", pady=2)

                # Rótulo com o Valor (pontuação) da Atividade.
                ctk.CTkLabel(
                    info_frame, 
                    text=f"Valor: {atividade['valor']} pontos", 
                    font=ctk.CTkFont(size=12), text_color="gray"
                ).pack(anchor="w", pady=2)

                # Botão de Entregar Atividade.
                ctk.CTkButton(
                    ativ_frame, 
                    text="Entregar", 
                    width=120, 
                    height=35, 
                    fg_color="#2CC985", # Cor de destaque (verde)
                    hover_color="#25A066", 
                    # Chama o método de entrega, passando a atividade como argumento (lambda para capturar o valor correto).
                    command=lambda a=atividade: self.show_entregar_atividade(a) 
                ).pack(side="right", padx=10, pady=10)

        # 10. Botão para retornar ao menu do aluno.
        back_btn = ctk.CTkButton(
            main_frame, text="← Voltar", 
            font=ctk.CTkFont(size=16), 
            width=200, 
            height=50, 
            command=self.show_aluno_menu, fg_color="gray", hover_color="darkgray")
        back_btn.pack(pady=30)

    def show_atividades_entregues(self):
        # 1. Limpa a janela principal.
        self.app.clear_window()

        # 2. Cria um frame rolável principal.
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 3. Rótulo de título para a seção.
        title_label = ctk.CTkLabel(
            main_frame, 
            text="✅ Atividades Concluídas", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        # 4. Importa a função de backend e obtém todas as atividades já entregues pelo aluno.
        from backend.turmas_backend import get_atividades_entregues_aluno
        atividades = get_atividades_entregues_aluno(self.user_email)

        # 5. Exibição das atividades na interface.
        if not atividades:
            # 5.1. Mensagem se nenhuma atividade foi entregue.
            empty_label = ctk.CTkLabel(main_frame, text="Você ainda não entregou nenhuma atividade.", font=ctk.CTkFont(size=16), text_color="gray")
            empty_label.pack(pady=50)
        else:
            # 5.2. Cria um widget para cada atividade entregue.
            for atividade in atividades:
                ativ_frame = ctk.CTkFrame(main_frame)
                ativ_frame.pack(pady=10, padx=40, fill="x")

                # Frame para as informações de texto.
                info_frame = ctk.CTkFrame(ativ_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)

                # Rótulo do Título da Atividade (com checkmark).
                ctk.CTkLabel(
                    info_frame, 
                    text=f"✅ {atividade['titulo']}", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    wraplength=400
                ).pack(anchor="w")

                # Rótulo com o Nome da Turma e Data de Entrega.
                ctk.CTkLabel(
                    info_frame, 
                    text=f"Turma: {atividade['turma']} | Entregue em: {atividade['data_entrega']}", 
                    font=ctk.CTkFont(size=13), 
                    text_color="gray"
                ).pack(anchor="w", pady=2)
                
                # 5.3. Exibe a Nota ou o status de "Aguardando correção".
                if atividade.get('nota'):
                    # Nota exibida em verde.
                    ctk.CTkLabel(info_frame, text=f"Nota: {atividade['nota']}/{atividade['valor']}", font=ctk.CTkFont(size=13, weight="bold"), text_color="#2CC985").pack(anchor="w", pady=2)
                else:
                    # Status de aguardando correção exibido em laranja.
                    ctk.CTkLabel(info_frame, text="Aguardando correção", font=ctk.CTkFont(size=12), text_color="#E67E22").pack(anchor="w", pady=2)

                # 5.4. Botão para ver os detalhes da entrega.
                ctk.CTkButton(
                    ativ_frame, 
                    text="Ver Detalhes", 
                    width=120, 
                    height=35, 
                    # Chama o método de visualização, passando a atividade (entrega) como argumento.
                    command=lambda a=atividade: self.show_ver_entrega(a)
                ).pack(side="right", padx=10, pady=10)

        # 6. Botão para retornar ao menu do aluno.
        back_btn = ctk.CTkButton(
            main_frame, 
            text="← Voltar", font=ctk.CTkFont(size=16), 
            width=200, 
            height=50, 
            fg_color="gray", 
            hover_color="darkgray",
            command=self.show_aluno_menu 
        )
        back_btn.pack(pady=30)

def show_boletim_completo(self):
        # 1. Limpa a janela principal.
        self.app.clear_window()

        # 2. Cria um frame rolável principal.
        main_frame = ctk.CTkScrollableFrame(self.app, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 3. Rótulo de título para a seção.
        title_label = ctk.CTkLabel(
            main_frame, 
            text="📊 Boletim Escolar", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        # 4. Importa as funções de backend e carrega os dados do boletim e do usuário.
        from backend.turmas_backend import get_boletim_aluno
        from database.banco import users_db
        user_data = users_db.get(self.user_email, {})
        # Obtém o boletim do aluno, que contém notas agrupadas por turma/disciplina.
        boletim = get_boletim_aluno(self.user_email)

        # 5. Frame para exibir informações básicas do aluno.
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(pady=10, padx=40, fill="x")

        # Rótulos de Nome, Email e RM do Aluno.
        ctk.CTkLabel(
            info_frame, 
            text=f"👨‍🎓 Aluno: {user_data.get('nome', 'N/A')}", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            info_frame, 
            text=f"📧 Email: {self.user_email}", 
            font=ctk.CTkFont(size=14), 
            text_color="gray"
        ).pack(anchor="w", padx=20, pady=2)

        if user_data.get('rm'):
            ctk.CTkLabel(
                info_frame, 
                text=f"🎫 RM: {user_data['rm']}", 
                font=ctk.CTkFont(size=14), 
                text_color="gray"
            ).pack(anchor="w", padx=20, pady=(2, 15))
        
        # 6. Exibição do boletim.
        if not boletim:
            # 6.1. Mensagem se não houver notas.
            ctk.CTkLabel(
                main_frame, 
                text="Você ainda não possui notas registradas.", 
                font=ctk.CTkFont(size=16), 
                text_color="gray"
            ).pack(pady=50)
        else:
            # 6.2. Calcula a média geral das turmas que possuem média.
            turmas_com_media = [t for t in boletim if t.get('media')]
            if turmas_com_media:
                media_geral = sum([turma['media'] for turma in turmas_com_media]) / len(turmas_com_media)
            else:
                media_geral = 0

            # 6.3. Frame de resumo (Média Geral).
            resumo_frame = ctk.CTkFrame(main_frame)
            resumo_frame.pack(pady=10, padx=40, fill="x")

            # Exibe a Média Geral com cor de destaque (verde >= 7, vermelho < 7).
            ctk.CTkLabel(
                resumo_frame, 
                text=f"📊 Média Geral: {media_geral:.2f}", 
                font=ctk.CTkFont(size=20, weight="bold"), 
                text_color="#2CC985" if media_geral >= 7 else "#E74C3C" # Verde ou Vermelho
            ).pack(pady=20)

            # 6.4. Cria um frame detalhado para cada turma/disciplina.
            for turma_data in boletim:
                turma_frame = ctk.CTkFrame(main_frame)
                turma_frame.pack(pady=10, padx=40, fill="x")

                # Título da Turma.
                ctk.CTkLabel(
                    turma_frame, 
                    text=f"📖 {turma_data['turma']}", 
                    font=ctk.CTkFont(size=18, weight="bold")
                ).pack(anchor="w", padx=20, pady=(15, 5))

                # Informações adicionais da Turma (Disciplina e Professor).
                ctk.CTkLabel(
                    turma_frame, 
                    text=f"Disciplina: {turma_data['disciplina']} | Professor: {turma_data['professor']}", 
                    font=ctk.CTkFont(size=13), 
                    text_color="gray"
                ).pack(anchor="w", padx=20, pady=2)

                # Cálculo de Status e cor.
                media = turma_data['media'] if turma_data['media'] else 0
                status = "Aprovado ✓" if media >= 7 else "Reprovado ✗" if media > 0 else "Sem notas"
                status_color = "#2CC985" if media >= 7 else "#E74C3C" if media > 0 else "gray"

                # Linha de Média, Frequência e Status (com cor).
                ctk.CTkLabel(
                    turma_frame, 
                    text=f"Média: {media:.2f} | Frequência: {turma_data['frequencia']}% | Status: {status}", 
                    font=ctk.CTkFont(size=14, weight="bold"), 
                    text_color=status_color
                ).pack(anchor="w", padx=20, pady=(5, 10))
                
                # Exibe a lista de notas por atividade.
                if turma_data['notas']:
                    notas_header = ctk.CTkLabel(
                        turma_frame, 
                        text="Notas por atividade:", 
                        font=ctk.CTkFont(size=13, weight="bold"),    
                    )
                    notas_header.pack(anchor="w", padx=20, pady=(5, 5))

                    for nota in turma_data['notas']:
                        nota_line = ctk.CTkLabel(
                            turma_frame, 
                            text=f"  • {nota['atividade']}: {nota['nota']}/{nota['valor']}", 
                            font=ctk.CTkFont(size=12), text_color="gray",
                            wraplength=500
                        )
                        nota_line.pack(anchor="w", padx=40, pady=2)

                turma_frame.pack_configure(pady=(10, 15))

            # 6.5. Botão de Exportar para PDF (somente se a biblioteca ReportLab estiver disponível).
            if REPORTLAB_AVAILABLE:
                export_btn = ctk.CTkButton(
                    main_frame, 
                    text="📥 Exportar Boletim (PDF)", 
                    font=ctk.CTkFont(size=16, weight="bold"), 
                    width=250, 
                    height=50, 
                    # Chama o método de exportação, passando dados do aluno e o boletim.
                    command=lambda: self.exportar_boletim_pdf(user_data, boletim), 
                    fg_color="#3498DB", # Cor azul para download
                    hover_color="#2874A6"
                )
                export_btn.pack(pady=20)

        # 7. Botão para retornar ao menu do aluno.
        back_btn = ctk.CTkButton(
            main_frame, 
            text="← Voltar", 
            font=ctk.CTkFont(size=16), 
            width=200, 
            height=50, 
            command=self.show_aluno_menu, 
            fg_color="gray", 
            hover_color="darkgray"
        )
        back_btn.pack(pady=30)

def exportar_boletim_pdf(self, user_data, boletim):
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from datetime import datetime
        from tkinter import filedialog, messagebox

        try:
            # 1. Abre a caixa de diálogo para salvar o arquivo PDF.
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialfile=f"Boletim_{user_data.get('rm', 'aluno')}.pdf")
            
            if not filename:
                return # Retorna se o usuário cancelar.
            
            # 2. Configurações básicas do documento PDF.
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = [] # Lista de elementos que comporão o PDF.
            styles = getSampleStyleSheet()

            # 3. Título do Boletim.
            title_style = ParagraphStyle(
                'CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#3498DB'), spaceAfter=30, alignment=1)
            story.append(Paragraph("📊 BOLETIM ESCOLAR", title_style))
            story.append(Spacer(1, 0.5*cm))

            # 4. Tabela de Informações do Aluno.
            info_data = [["Aluno:", user_data.get('nome', 'N/A')], ["RM:", user_data.get('rm', 'N/A')], ["Email:", user_data.get('email', 'N/A')], ["Data:", datetime.now().strftime("%d/%m/%Y")]]
            info_table = Table(info_data, colWidths=[4*cm, 12*cm])
            # Estilos da tabela de informações.
            info_table.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 10), ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10), ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey), ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1'))]))
            
            story.append(info_table)
            story.append(Spacer(1, 1*cm))

            # 5. Se houver boletim, exibe o resumo e detalhes por turma.
            if boletim:
                # 5.1. Tabela de Média Geral.
                media_geral = sum([t['media'] for t in boletim if t['media']]) / len([t for t in boletim if t['media']]) if [t for t in boletim if t['media']] else 0
                resumo_data = [["MÉDIA GERAL", f"{media_geral:.2f}"]]
                resumo_table = Table(resumo_data, colWidths=[12*cm, 4*cm])
                # Estilo de destaque (verde/vermelho) para a Média Geral.
                resumo_table.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 14), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2CC985' if media_geral >= 7 else '#E74C3C')), ('TEXTCOLOR', (0, 0), (-1, -1), colors.white), ('GRID', (0, 0), (-1, -1), 1, colors.white)]))
                
                story.append(resumo_table)
                story.append(Spacer(1, 0.7*cm))

                # 5.2. Loop para detalhar cada turma.
                for turma_data in boletim:
                    # Título da Turma (Disciplina).
                    story.append(Paragraph(f"<b>{turma_data['turma']}</b>", styles['Heading2']))
                    story.append(Spacer(1, 0.3*cm))
                    
                    # Tabela de Informações da Turma (Disciplina e Professor).
                    turma_info = [[f"Disciplina: {turma_data['disciplina']}", f"Professor: {turma_data['professor']}"]]
                    turma_table = Table(turma_info, colWidths=[8*cm, 8*cm])
                    turma_table.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 9), ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
                    
                    story.append(turma_table)
                    story.append(Spacer(1, 0.3*cm))
                    
                    # Tabela de Desempenho (Média, Frequência, Status).
                    media = turma_data['media'] if turma_data['media'] else 0
                    status = "Aprovado" if media >= 7 else "Reprovado" if media > 0 else "Sem notas"
                    
                    desempenho_data = [["Média", "Frequência", "Status"], [f"{media:.2f}", f"{turma_data['frequencia']}%", status]]
                    desempenho_table = Table(desempenho_data, colWidths=[5*cm, 5*cm, 6*cm])
                    # Estilos da tabela de desempenho, destacando o Status.
                    desempenho_table.setStyle(TableStyle([('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10), ('FONT', (0, 1), (-1, -1), 'Helvetica', 10), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), ('BACKGROUND', (2, 1), (2, 1), colors.HexColor('#2CC985' if media >= 7 else '#E74C3C')), ('TEXTCOLOR', (2, 1), (2, 1), colors.white if media != 0 else colors.black)]))
                    
                    story.append(desempenho_table)
                    
                    # Tabela de Notas por Atividade (detalhada).
                    if turma_data['notas']:
                        story.append(Spacer(1, 0.3*cm))
                        notas_data = [["Atividade", "Nota", "Valor"]]

                        # Define um estilo de parágrafo menor para o texto das atividades na tabela.
                        body_style = styles['Normal']
                        body_style.fontSize = 8
                        body_style.leading = 10

                        for nota in turma_data['notas']:
                            # Usa Paragraph para permitir que o texto quebre linhas automaticamente na célula.
                            titulo_atividade = Paragraph(nota['atividade'], body_style)

                            notas_data.append([
                                titulo_atividade, 
                                str(nota['nota']), 
                                str(nota['valor'])
                            ])

                        notas_table = Table(notas_data, colWidths=[10*cm, 3*cm, 3*cm])
                        # Estilos da tabela de notas.
                        notas_table.setStyle(TableStyle([
                            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9), 
                            ('FONT', (0, 1), (-1, -1), 'Helvetica', 8), 
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'), 
                            ('ALIGN', (1, 0), (-1, -1), 'CENTER'), 
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey), 
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ECF0F1'))
                        ]))
                        story.append(notas_table)
                    story.append(Spacer(1, 0.7*cm))
            
            # 6. Constrói o PDF e exibe mensagem de sucesso.
            doc.build(story)
            messagebox.showinfo("Sucesso", f"Boletim exportado com sucesso!\n{filename}")
        except Exception as e:
            # 7. Trata erros na exportação.
            messagebox.showerror("Erro", f"Erro ao exportar boletim:\n{str(e)}")
    
def darken_color(self, hex_color):
        # 1. Remove o '#' inicial.
        hex_color = hex_color.lstrip('#')
        # 2. Converte a cor hexadecimal para uma tupla RGB de inteiros.
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        # 3. Escurece cada componente RGB em 20% (multiplica por 0.8) e garante que o valor mínimo seja 0.
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        # 4. Converte a tupla RGB escurecida de volta para uma string hexadecimal.
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"