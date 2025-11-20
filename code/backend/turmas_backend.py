import json 
import os 
from datetime import datetime, timedelta 
from pathlib import Path 
import shutil 
import base64 

def safe_parse_date(date_string, date_format, default_date=None):
   
    if default_date is None:
        # Define a data padrão se nenhuma for fornecida (2000-01-01)
        default_date = datetime(2000, 1, 1)
    
    if not date_string or not isinstance(date_string, str):
        # Retorna a data padrão se a entrada não for uma string válida
        return default_date
    
    try:
        # Tenta converter a string de data usando o formato especificado
        return datetime.strptime(date_string, date_format)
    except (ValueError, TypeError): # Captura erros se a string não corresponder ao formato ou se houver um erro de tipo
        return default_date # Retorna a data padrão em caso de exceção

# Define o diretório base. __file__ é o caminho do script atual.
# .resolve() resolve o caminho absoluto.
# .parent.parent move dois níveis acima (assumindo que o script esteja em um subdiretório, como 'src' ou 'utils').
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database" # Define o diretório onde os arquivos de banco de dados serão armazenados.

# Caminhos completos para os arquivos JSON dentro do DATABASE_DIR.
# Estes arquivos armazenam dados para diferentes entidades
TURMAS_FILE = DATABASE_DIR / "turmas.json"
AULAS_FILE = DATABASE_DIR / "aulas.json"
ATIVIDADES_FILE = DATABASE_DIR / "atividades.json"
ENTREGAS_FILE = DATABASE_DIR / "entregas.json"
MATRICULAS_FILE = DATABASE_DIR / "matriculas.json"
USERS_FILE = DATABASE_DIR / "users.json"
FREQUENCIA_FILE = DATABASE_DIR / "frequencia.json"
RELATORIOS_FILE = DATABASE_DIR / "relatorios.json"
ARQUIVOS_DIR = DATABASE_DIR / "arquivos" # Define o diretório para armazenar arquivos

# Cria o diretório 'arquivos' se ele ainda não existir.
# exist_ok=True evita que o programa levante um erro se o diretório já existir.
ARQUIVOS_DIR.mkdir(exist_ok=True)

def carregar_json(arquivo):
    try:
        # Abre o arquivo no modo de leitura ('r') com codificação UTF-8
        with open(arquivo, 'r', encoding='utf-8') as f:
            # Carrega (decodifica) o conteúdo JSON do arquivo para um objeto Python
            return json.load(f)
    except FileNotFoundError:
        # Captura o erro se o arquivo não existir
        return {} # Retorna um dicionário vazio para evitar quebras
    except json.JSONDecodeError:
        # Captura o erro se o conteúdo do arquivo não for um JSON válido
        return {}

def salvar_json(arquivo, dados):
    # Abre o arquivo no modo de escrita ('w') com codificação UTF-8. 
    # Isso sobrescreverá o arquivo se ele já existir.
    with open(arquivo, 'w', encoding='utf-8') as f:
        # Escreve (codifica) o objeto Python 'dados' no arquivo como JSON.
        # indent=5: Formata a saída JSON com 5 espaços de recuo para torná-lo legível (pretty-print).
        # ensure_ascii=False: Garante que caracteres não-ASCII (como acentos e cedilha) sejam salvos diretamente, e não como sequências de escape Unicode.
        json.dump(dados, f, indent=5, ensure_ascii=False)

def get_user_data(email):
    # Função para recuperar os dados de um usuário específico a partir do arquivo USERS_FILE, usando o email como chave.

    dados = carregar_json(USERS_FILE) # Carrega todos os dados do arquivo de usuários (USERS_FILE).
    usuario = dados.get('users', {}).get(email, {}) # Tenta obter os dados do usuário usando o email como chave.

    # Verifica se um dicionário de usuário válido foi encontrado
    if usuario:
        usuario['email'] = email
    return usuario

def get_todos_usuarios(filtro='TODOS', search_term=None):
    
    dados = carregar_json(USERS_FILE)
    usuarios = dados.get('users', {})
    
    lista_usuarios = []
    
    # Prepara o termo de busca para comparação sem distinção de maiúsculas/minúsculas
    search_term_lower = search_term.lower().strip() if search_term else None
    
    # Itera sobre os usuários, onde a chave é o email e o valor são os dados do usuário
    for email, user_data in usuarios.items():
        # Filtro de Role (TODOS ou uma role específica)
        passou_pelo_filtro_role = (filtro == 'TODOS' or user_data.get('role') == filtro)
        
        if passou_pelo_filtro_role:
            passou_pelo_filtro_busca = True
            
            # Aplica o filtro de busca se um termo foi fornecido
            if search_term_lower:
                nome_lower = user_data.get('nome', '').lower()
                email_lower = email.lower()
                
                # O usuário só passa se o termo de busca estiver no nome OU no email
                if search_term_lower not in nome_lower and search_term_lower not in email_lower:
                    passou_pelo_filtro_busca = False
            
            if passou_pelo_filtro_busca:
                # Cria uma cópia dos dados e adiciona o email (que é a chave do dicionário)
                user_info = user_data.copy()
                user_info['email'] = email
                lista_usuarios.append(user_info)
    
    return lista_usuarios

def get_detalhes_completos_usuario(email):
    
    user_data = get_user_data(email) 

    if not user_data:
        return None
    
    detalhes = user_data.copy()
    detalhes['data_cadastro'] = "N/A" # Valor padrão, pode ser sobrescrito
    
    # Lógica para INSTRUCTOR
    if user_data.get('role') == 'INSTRUCTOR':
        turmas = get_turmas_professor(email) 
        detalhes['total_turmas'] = len(turmas)
        # Calcula o total de alunos somando os totais de cada turma
        detalhes['total_alunos'] = sum([t.get('total_alunos', 0) for t in turmas])
        atividades = get_todas_atividades_professor(email) 
        detalhes['total_atividades'] = len(atividades)
        aulas = get_todas_aulas_professor(email) 
        detalhes['total_aulas'] = len(aulas)
    # Lógica para USER (Aluno)
    elif user_data.get('role') == 'USER':
        turmas = get_turmas_aluno(email) 
        detalhes['total_turmas'] = len(turmas)
        entregas = get_atividades_entregues_aluno(email) 
        detalhes['atividades_entregues'] = len(entregas)
        boletim = get_boletim_aluno(email) 
        
        # Calcula a média geral a partir das médias das turmas
        medias = [t['media'] for t in boletim if t.get('media') and t['media'] > 0]
        detalhes['media_geral'] = sum(medias) / len(medias) if medias else 0
        
        frequencia_media = calcular_frequencia_media_aluno(email)
        detalhes['frequencia_media'] = frequencia_media
        
        dados_matriculas = carregar_json(MATRICULAS_FILE)

        # Busca a data da primeira matrícula do aluno
        if email in dados_matriculas.get('matriculas', {}):
            data_matricula = dados_matriculas['matriculas'][email].get('data_matricula', 'N/A')
            detalhes['data_matricula'] = data_matricula
    
    return detalhes

def editar_usuario(email, nome, role, senha_criptografada=None):
    
    dados = carregar_json(USERS_FILE)

    # Verifica se o usuário existe e se a senha NÃO será alterada
    if email in dados.get('users', {}) and senha_criptografada is None:
        dados['users'][email]['nome'] = nome
        dados['users'][email]['role'] = role
        salvar_json(USERS_FILE, dados)
        dados = carregar_json(USERS_FILE) # Recarrega os dados 
        return True
    # Verifica se o usuário existe e se a senha SERÁ alterada
    elif email in dados.get('users', {}) and senha_criptografada is not None:
        dados['users'][email]['nome'] = nome
        dados['users'][email]['role'] = role
        dados['users'][email]['senha'] = senha_criptografada # Atualiza a senha
        salvar_json(USERS_FILE, dados)
        dados = carregar_json(USERS_FILE) # Recarrega os dados
        return True
    else:
        # Usuário não encontrado
        return False
    
def excluir_usuario(email):
    
    dados = carregar_json(USERS_FILE)

    if email in dados.get('users', {}):
        del dados['users'][email] # Remove a entrada do usuário
        salvar_json(USERS_FILE, dados)
        return True
    return False

def adicionar_usuario(nome, email, senha, role):
    
    dados = carregar_json(USERS_FILE)

    if 'users' not in dados:
        dados['users'] = {}
    
    if email in dados['users']:
        # Usuário já existe
        return False
    
    # Importa funções necessárias para criptografia e geração de RM
    from infra.security import criptografar_senha
    from database.banco import gerar_rm
    
    # Monta os dados básicos do novo usuário
    user_data = {
        'nome': nome,
        'senha': criptografar_senha(senha),
        'role': role
    }
    
    # Se for aluno, gera e adiciona o RM
    if role == 'USER':
        user_data['rm'] = gerar_rm()
    
    dados['users'][email] = user_data # Adiciona o novo usuário
    salvar_json(USERS_FILE, dados)
    return True

def criar_turma(professor_email, nome, disciplina, ano, periodo, descricao):
    
    dados = carregar_json(TURMAS_FILE)
    
    if 'turmas' not in dados:
        dados['turmas'] = {}

    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1 # Inicializa o contador de ID
    
    turma_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1 # Incrementa o próximo ID
    
    professor = get_user_data(professor_email) # Busca dados do professor
    
    # Estrutura de dados da nova turma
    dados['turmas'][turma_id] = {
        'id': turma_id,
        'nome': nome,
        'disciplina': disciplina,
        'professor_email': professor_email,
        'professor_nome': professor.get('nome', ''),
        'ano': ano,
        'periodo': periodo,
        'descricao': descricao,
        'data_criacao': datetime.now().strftime("%d/%m/%Y")
    }
    
    salvar_json(TURMAS_FILE, dados)
    return turma_id

def get_turma_por_id(turma_id):
    
    dados = carregar_json(TURMAS_FILE)
    turma = dados.get('turmas', {}).get(str(turma_id))
    
    if turma:
        # Carrega dados de matrícula para contar alunos
        matriculas = carregar_json(MATRICULAS_FILE).get('matriculas', {})
        # Filtra matrículas pertencentes a esta turma
        alunos_turma = [m for m in matriculas.values() if m.get('turma_id') == str(turma_id)]
        
        turma_copy = turma.copy()
        turma_copy['total_alunos'] = len(alunos_turma) # Adiciona a contagem
        return turma_copy
    
    return None

def get_turmas_professor(professor_email):
    
    dados = carregar_json(TURMAS_FILE)
    matriculas = carregar_json(MATRICULAS_FILE).get('matriculas', {})
    
    turmas_prof = []

    for turma_id, turma in dados.get('turmas', {}).items():
        if turma.get('professor_email') == professor_email:
            turma_copy = turma.copy()
            # Conta alunos nesta turma
            alunos_turma = [m for m in matriculas.values() if m.get('turma_id') == turma_id]
            turma_copy['total_alunos'] = len(alunos_turma)
            turmas_prof.append(turma_copy)
    
    return turmas_prof

def get_turmas_aluno(aluno_email):
    
    dados_turmas = carregar_json(TURMAS_FILE)
    matriculas = carregar_json(MATRICULAS_FILE).get('matriculas', {})
    
    turmas_aluno = []

    for matricula in matriculas.values():
        if matricula.get('aluno_email') == aluno_email:
            turma_id = matricula.get('turma_id')
            # Busca os detalhes da turma
            turma = dados_turmas.get('turmas', {}).get(turma_id)
            if turma:
                turmas_aluno.append(turma.copy())
    
    return turmas_aluno

def get_todas_turmas():
    
    dados = carregar_json(TURMAS_FILE)
    matriculas = carregar_json(MATRICULAS_FILE).get('matriculas', {})
    
    todas_turmas = []

    for turma_id, turma in dados.get('turmas', {}).items():
        turma_copy = turma.copy()
        # Conta alunos na turma
        alunos_turma = [m for m in matriculas.values() if m.get('turma_id') == turma_id]
        turma_copy['total_alunos'] = len(alunos_turma)
        todas_turmas.append(turma_copy)
    
    return todas_turmas

def get_detalhes_completos_turma(turma_id):
    
    dados = carregar_json(TURMAS_FILE)
    aulas = carregar_json(AULAS_FILE).get('aulas', {})
    atividades = carregar_json(ATIVIDADES_FILE).get('atividades', {})
    
    turma = dados.get('turmas', {}).get(str(turma_id), {})
    if not turma:
        return None
    
    detalhes = turma.copy()
    # Conta aulas associadas a esta turma
    detalhes['total_aulas'] = len([a for a in aulas.values() if a.get('turma_id') == str(turma_id)])
    # Conta atividades associadas a esta turma
    detalhes['total_atividades'] = len([a for a in atividades.values() if a.get('turma_id') == str(turma_id)])
    
    return detalhes

def get_alunos_turma(turma_id):
    
    matriculas = carregar_json(MATRICULAS_FILE).get('matriculas', {})
    
    alunos = []

    for matricula in matriculas.values():
        if matricula.get('turma_id') == str(turma_id):
            aluno_email = matricula.get('aluno_email')
            aluno_data = get_user_data(aluno_email) # Busca os dados completos do aluno
            if aluno_data:
                alunos.append(aluno_data)
    
    return alunos

def get_alunos_disponiveis(turma_id):
    
    todos_alunos = get_todos_usuarios(filtro='USER') # Assume função existente para filtrar apenas alunos
    dados_matriculas = carregar_json(MATRICULAS_FILE)
    todas_matriculas = dados_matriculas.get('matriculas', {})
    
    # Cria um conjunto de emails de todos os alunos matriculados em *qualquer* turma
    emails_matriculados_em_qualquer_turma = {
        m.get('aluno_email') for m in todas_matriculas.values()
    }
    
    # Filtra a lista de todos os alunos para incluir apenas aqueles cujo email não está no conjunto de matriculados
    alunos_disponiveis = [
        aluno for aluno in todos_alunos
        if aluno['email'] not in emails_matriculados_em_qualquer_turma
    ]
    
    return alunos_disponiveis

def adicionar_aluno_turma(turma_id, aluno_email):
    
    matriculas = carregar_json(MATRICULAS_FILE)
    
    
    if 'matriculas' not in matriculas:
        matriculas['matriculas'] = {}
    
    
    # Verifica se o aluno já está matriculado nesta turma
    for matricula in matriculas['matriculas'].values():
        if (matricula.get('turma_id') == str(turma_id) and 
            matricula.get('aluno_email') == aluno_email):
            return False # Matrícula duplicada
    
    # Adiciona a nova matrícula usando o email do aluno como chave 
    matriculas['matriculas'][aluno_email] = {
        'turma_id': str(turma_id),
        'aluno_email': aluno_email,
        'data_matricula': datetime.now().strftime("%d/%m/%Y")
    }
    
    salvar_json(MATRICULAS_FILE, matriculas)
    return True
    
def atribuir_professor_turma(turma_id, professor_email):
    
    dados_turmas = carregar_json(TURMAS_FILE)
    dados_users = carregar_json(USERS_FILE)
    
    if str(turma_id) not in dados_turmas.get('turmas', {}):
        return False, "Turma não encontrada!"
    
    usuario = dados_users.get('users', {}).get(professor_email)

    if not usuario:
        return False, "Usuário não encontrado!"
    
    if usuario.get('role') != 'INSTRUCTOR':
        return False, "O usuário selecionado não é um professor!"
    
    # Atualiza o email e o nome do professor na turma
    dados_turmas['turmas'][str(turma_id)]['professor_email'] = professor_email
    dados_turmas['turmas'][str(turma_id)]['professor_nome'] = usuario.get('nome', '')
    
    salvar_json(TURMAS_FILE, dados_turmas)
    return True, "Professor atribuído com sucesso!"

def get_professores_disponiveis():
    
    dados = carregar_json(USERS_FILE)
    usuarios = dados.get('users', {})
    
    professores = []

    for email, user_data in usuarios.items():
        if user_data.get('role') == 'INSTRUCTOR':
            prof_info = user_data.copy()
            prof_info['email'] = email
            professores.append(prof_info)
    
    return professores

def editar_turma(turma_id, nome, disciplina, ano, periodo, descricao):
    
    turma_id_str = str(turma_id)
    dados = carregar_json(TURMAS_FILE)
    
    if turma_id_str in dados.get('turmas', {}):
        turma = dados['turmas'][turma_id_str]
        
        # Atualiza os campos
        turma['nome'] = nome
        turma['disciplina'] = disciplina
        turma['ano'] = ano
        turma['periodo'] = periodo
        turma['descricao'] = descricao
        
        salvar_json(TURMAS_FILE, dados)
        return True
    
    return False

def remover_aluno_turma(turma_id, aluno_email):
    
    matriculas = carregar_json(MATRICULAS_FILE)
    matricula_id_remover = None

    # Itera sobre as matrículas para encontrar o ID/chave correspondente à turma e ao aluno
    for matricula_id, matricula in matriculas.get('matriculas', {}).items():
        if (matricula.get('turma_id') == str(turma_id) and 
            matricula.get('aluno_email') == aluno_email):
            matricula_id_remover = matricula_id # Armazena a chave
            break
    
    if matricula_id_remover:
        del matriculas['matriculas'][matricula_id_remover] # Remove a matrícula
        salvar_json(MATRICULAS_FILE, matriculas)
        return True
    
    return False

def limpar_matriculas_turma(turma_id):
    
    matriculas = carregar_json(MATRICULAS_FILE)
    
    # Cria um novo dicionário de matrículas excluindo aquelas com o turma_id especificado
    matriculas_atualizadas = {
        mid: m for mid, m in matriculas.get('matriculas', {}).items()
        if m.get('turma_id') != str(turma_id)
    }
    
    matriculas['matriculas'] = matriculas_atualizadas
    salvar_json(MATRICULAS_FILE, matriculas)
    return True

def limpar_aulas_turma(turma_id):
    
    aulas = carregar_json(AULAS_FILE)
    
    # Cria um novo dicionário de aulas excluindo aquelas com o turma_id especificado
    aulas_atualizadas = {
        aid: a for aid, a in aulas.get('aulas', {}).items()
        if a.get('turma_id') != str(turma_id)
    }
    
    aulas['aulas'] = aulas_atualizadas
    salvar_json(AULAS_FILE, aulas)
    return True

def limpar_atividades_e_entregas(turma_id):
    
    atividades = carregar_json(ATIVIDADES_FILE)
    entregas = carregar_json(ENTREGAS_FILE)
    
    # 1. Identifica os IDs das atividades pertencentes à turma
    atividades_para_remover = [
        aid for aid, a in atividades.get('atividades', {}).items()
        if a.get('turma_id') == str(turma_id)
    ]
    
    # 2. Cria um novo dicionário de entregas, excluindo aquelas cujos IDs de atividade estão na lista de remoção (entregas relacionadas às atividades da turma)
    entregas_atualizadas = {
        eid: e for eid, e in entregas.get('entregas', {}).items()
        if e.get('atividade_id') not in atividades_para_remover
    }
    
    entregas['entregas'] = entregas_atualizadas
    salvar_json(ENTREGAS_FILE, entregas)
    
    # 3. Cria um novo dicionário de atividades, excluindo aquelas identificadas para remoção
    atividades_atualizadas = {
        aid: a for aid, a in atividades.get('atividades', {}).items()
        if aid not in atividades_para_remover
    }
    atividades['atividades'] = atividades_atualizadas
    salvar_json(ATIVIDADES_FILE, atividades)
    
    return True

def excluir_turma(turma_id):
    
    turma_id_str = str(turma_id)
    dados = carregar_json(TURMAS_FILE)
    
    if turma_id_str not in dados.get('turmas', {}):
        return False # Turma não existe
    
    try:
        # Executa as limpezas em cascata
        limpar_matriculas_turma(turma_id_str)
        limpar_aulas_turma(turma_id_str)
        limpar_atividades_e_entregas(turma_id_str)
        
        # Remove a própria turma
        del dados['turmas'][turma_id_str]
        salvar_json(TURMAS_FILE, dados)
        
        return True
    
    except Exception as e:
        print(f"Erro ao excluir turma {turma_id}: {e}")
        return False

def registrar_aula(turma_id, data, titulo, conteudo, observacoes=""):
    
    dados = carregar_json(AULAS_FILE)
    
    if 'aulas' not in dados:
        dados['aulas'] = {}

    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1 # Inicializa o contador de ID
    
    aula_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1 # Incrementa o próximo ID
    
    # Busca a turma para obter o email do professor
    turma = carregar_json(TURMAS_FILE).get('turmas', {}).get(str(turma_id), {})
    
    # Estrutura de dados da nova aula
    dados['aulas'][aula_id] = {
        'id': aula_id,
        'turma_id': str(turma_id),
        'data': data,
        'titulo': titulo,
        'conteudo': conteudo,
        'observacoes': observacoes,
        'professor_email': turma.get('professor_email', ''), # Obtém o email do professor da turma
        'data_registro': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    salvar_json(AULAS_FILE, dados)
    return aula_id

def get_aulas_turma(turma_id):
    
    dados = carregar_json(AULAS_FILE)
    aulas = []
    
    for aula in dados.get('aulas', {}).values():
        if aula.get('turma_id') == str(turma_id):
            aulas.append(aula)
    
    # Ordena as aulas usando a data como chave (convertendo a string de data para um objeto datetime)
    aulas.sort(key=lambda x: safe_parse_date(x.get('data', ''), "%d/%m/%Y"), reverse=True)
    return aulas    

def get_todas_aulas_professor(professor_email):
    
    dados = carregar_json(AULAS_FILE)
    aulas = []
    
    for aula in dados.get('aulas', {}).values():
        if aula.get('professor_email') == professor_email:
            aulas.append(aula)
    
    return aulas

def atualizar_aula(aula_id, data, titulo, conteudo, observacoes):
    
    dados = carregar_json(AULAS_FILE)
    
    if aula_id in dados.get('aulas', {}):
        # Atualiza o dicionário da aula com os novos dados
        dados['aulas'][aula_id].update({
            'data': data,
            'titulo': titulo,
            'conteudo': conteudo,
            'observacoes': observacoes
        })
        salvar_json(AULAS_FILE, dados)
        return True
    
    return False

def editar_aula(aula_id, data, titulo, conteudo, observacoes):
    return atualizar_aula(aula_id, data, titulo, conteudo, observacoes)

def excluir_aula(aula_id):
    
    dados = carregar_json(AULAS_FILE)
    
    if aula_id in dados.get('aulas', {}):
        del dados['aulas'][aula_id] # Remove a aula
        salvar_json(AULAS_FILE, dados)
        return True
    
    return False

def registrar_frequencia(aula_id, aluno_email, presente):
    
    dados = carregar_json(FREQUENCIA_FILE)
    
    if 'frequencias' not in dados:
        dados['frequencias'] = {}
    
    # Cria uma chave única para o registro de frequência
    freq_id = f"{aula_id}_{aluno_email}"
    
    # Armazena o registro de frequência
    dados['frequencias'][freq_id] = {
        'aula_id': str(aula_id),
        'aluno_email': aluno_email,
        'presente': presente, # Valor indicando presença
        'data_registro': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    salvar_json(FREQUENCIA_FILE, dados)
    return True

# --- Funções de Frequência ---
def registrar_chamada(aula_id, presencas_dict):
    
    try:
        # Itera sobre o dicionário e chama 'registrar_frequencia' para cada aluno
        for aluno_email, presente in presencas_dict.items():
            registrar_frequencia(aula_id, aluno_email, presente)
        return True
    except Exception as e:
        print(f"Erro ao registrar chamada: {e}")
        return False

def get_frequencia_aula(aula_id):
    
    dados = carregar_json(FREQUENCIA_FILE)
    frequencias = {}
    
    # Itera sobre todos os registros de frequência
    for freq_id, freq in dados.get('frequencias', {}).items():
        # Filtra registros pela aula_id
        if freq.get('aula_id') == str(aula_id):
            aluno_email = freq.get('aluno_email')
            # Mapeia o email do aluno para o seu status de presença
            frequencias[aluno_email] = freq.get('presente', False)
    
    return frequencias

def calcular_frequencia_aluno_turma(aluno_email, turma_id):
    
    aulas = get_aulas_turma(turma_id)
    
    if not aulas:
        # Se não houver aulas registradas, a frequência é 100%
        return 100.0
    
    dados_freq = carregar_json(FREQUENCIA_FILE)
    presencas = 0
    total_aulas = len(aulas)
    
    for aula in aulas:
        # Constrói a chave composta (aula_id_aluno_email) para buscar o registro de frequência
        freq_id = f"{aula['id']}_{aluno_email}"

        if freq_id in dados_freq.get('frequencias', {}):
            # Verifica se o aluno foi marcado como 'presente' (True)
            if dados_freq['frequencias'][freq_id].get('presente'):
                presencas += 1
    
    # Calcula e retorna a porcentagem de frequência
    return (presencas / total_aulas * 100) if total_aulas > 0 else 100.0

def calcular_frequencia_media_aluno(aluno_email):
    
    turmas = get_turmas_aluno(aluno_email)
    
    if not turmas:
        return 100.0
    
    frequencias = []
    # Calcula a frequência individual para cada turma
    for turma in turmas:
        freq = calcular_frequencia_aluno_turma(aluno_email, turma['id'])
        frequencias.append(freq)
    
    # Calcula a média das frequências
    return sum(frequencias) / len(frequencias) if frequencias else 100.0

def get_relatorio_frequencia_turma(turma_id):
    
    alunos = get_alunos_turma(turma_id)
    aulas = get_aulas_turma(turma_id)
    
    relatorio = []

    for aluno in alunos:
        # Calcula a frequência percentual total do aluno na turma
        freq_percentual = calcular_frequencia_aluno_turma(aluno['email'], turma_id)
        
        presencas = 0
        faltas = 0
        
        dados_freq = carregar_json(FREQUENCIA_FILE)

        # Itera sobre as aulas para contar presenças e faltas detalhadamente
        for aula in aulas:
            freq_id = f"{aula['id']}_{aluno['email']}"
            if freq_id in dados_freq.get('frequencias', {}):
                if dados_freq['frequencias'][freq_id].get('presente'):
                    presencas += 1
                else:
                    faltas += 1
        
        # Adiciona os dados do aluno ao relatório
        relatorio.append({
            'aluno_nome': aluno['nome'],
            'aluno_email': aluno['email'],
            'aluno_rm': aluno.get('rm', 'N/A'),
            'total_aulas': len(aulas),
            'presencas': presencas,
            'faltas': faltas,
            'frequencia_percentual': freq_percentual
        })
    
    return relatorio

# --- Funções de Atividade ---
def criar_atividade(turma_id, titulo, descricao, data_entrega, valor, arquivo_path=None):
    
    dados = carregar_json(ATIVIDADES_FILE)
    
    if 'atividades' not in dados:
        dados['atividades'] = {}

    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1
    
    atividade_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1
    
    turma = carregar_json(TURMAS_FILE).get('turmas', {}).get(str(turma_id), {})
    
    # Estrutura de dados da nova atividade
    atividade = {
        'id': atividade_id,
        'turma_id': str(turma_id),
        'titulo': titulo,
        'descricao': descricao,
        'data_entrega': data_entrega,
        'valor': float(valor),
        'data_criacao': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'professor_email': turma.get('professor_email', '')
    }
    
    # Bloco para lidar com o upload e salvamento de arquivo opcional
    if arquivo_path:
        try:
            arquivo_nome = os.path.basename(arquivo_path)
            # Define o caminho de destino no diretório de arquivos
            destino = ARQUIVOS_DIR / f"atividade_{atividade_id}_{arquivo_nome}"
            shutil.copy2(arquivo_path, destino) # Copia o arquivo
            atividade['arquivo'] = str(destino)
            atividade['arquivo_nome'] = arquivo_nome
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}") 
    
    dados['atividades'][atividade_id] = atividade
    salvar_json(ATIVIDADES_FILE, dados)
    
    return atividade_id

def get_atividades_turma(turma_id):
   
    dados = carregar_json(ATIVIDADES_FILE)
    atividades = []
    
    for atividade in dados.get('atividades', {}).values():
        if atividade.get('turma_id') == str(turma_id):
            atividades.append(atividade)
    
    # Ordena as atividades pela data de entrega (da mais antiga para a mais recente)
    atividades.sort(key=lambda x: datetime.strptime(x['data_entrega'], "%d/%m/%Y"))
    return atividades

def get_atividades_turma_aluno(turma_id, aluno_email):
    
    atividades = get_atividades_turma(turma_id)
    entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})
    
    atividades_aluno = []

    for atividade in atividades:
        ativ_copy = atividade.copy()
        
        entrega_aluno = None

        # Busca a entrega específica deste aluno para esta atividade
        for entrega in entregas.values():
            if (entrega.get('atividade_id') == atividade['id'] and 
                entrega.get('aluno_email') == aluno_email):
                entrega_aluno = entrega
                break
        
        # Adiciona o status de entrega e corrige o status se houver nota
        ativ_copy['entregue'] = entrega_aluno is not None
        ativ_copy['status'] = 'Entregue' if entrega_aluno else 'Pendente'
        
        if entrega_aluno:
            ativ_copy['data_entrega_aluno'] = entrega_aluno.get('data_entrega')
            ativ_copy['nota'] = entrega_aluno.get('nota')
            ativ_copy['feedback'] = entrega_aluno.get('feedback', '')
            ativ_copy['entrega_id'] = entrega_aluno.get('id')
            
            if entrega_aluno.get('nota') is not None:
                ativ_copy['status'] = 'Avaliada'
            else:
                ativ_copy['status'] = 'Aguardando Correção'
        
        atividades_aluno.append(ativ_copy)
    
    return atividades_aluno

def get_atividades_com_entregas(professor_email):
    
    atividades = get_todas_atividades_professor(professor_email)
    entregas_dados = carregar_json(ENTREGAS_FILE).get('entregas', {})
    turmas_dados = carregar_json(TURMAS_FILE).get('turmas', {})
    
    atividades_completas = []

    for atividade in atividades:
        ativ_copy = atividade.copy()
        
        # Adiciona detalhes da turma
        turma = turmas_dados.get(atividade['turma_id'], {})
        ativ_copy['turma_nome'] = turma.get('nome', 'N/A')
        ativ_copy['disciplina'] = turma.get('disciplina', 'N/A')
        
        # Filtra entregas para a atividade atual
        entregas_atividade = [e for e in entregas_dados.values() 
                            if e.get('atividade_id') == atividade['id']]
        
        # Calcula contagens de entregas
        ativ_copy['total_entregas'] = len(entregas_atividade)
        ativ_copy['entregas_corrigidas'] = len([e for e in entregas_atividade 
                                                if e.get('nota') is not None])
        ativ_copy['entregas_pendentes'] = len([e for e in entregas_atividade 
                                               if e.get('nota') is None])
        
        # Conta o total de alunos na turma (para comparar com o total de entregas)
        alunos_turma = get_alunos_turma(atividade['turma_id'])
        ativ_copy['total_alunos'] = len(alunos_turma)
        
        atividades_completas.append(ativ_copy)
    
    return atividades_completas

def get_detalhes_atividade_professor(atividade_id):
    
    dados_atividades = carregar_json(ATIVIDADES_FILE)
    entregas_dados = carregar_json(ENTREGAS_FILE).get('entregas', {})
    
    atividade = dados_atividades.get('atividades', {}).get(str(atividade_id))

    if not atividade:
        return None
    
    entregas = []

    for entrega in entregas_dados.values():
        if entrega.get('atividade_id') == str(atividade_id):
            entrega_copy = entrega.copy()
            
            # Adiciona nome e RM do aluno à entrega
            aluno = get_user_data(entrega['aluno_email'])
            entrega_copy['aluno_nome'] = aluno.get('nome', 'N/A')
            entrega_copy['aluno_rm'] = aluno.get('rm', 'N/A')
            
            # Define o status da entrega
            if entrega.get('nota') is not None:
                entrega_copy['status'] = 'Corrigida'
            else:
                entrega_copy['status'] = 'Aguardando Correção'
            
            entregas.append(entrega_copy)
    
    # Identifica alunos que não entregaram
    alunos_turma = get_alunos_turma(atividade['turma_id'])
    alunos_entregaram = [e['aluno_email'] for e in entregas]
    alunos_nao_entregaram = [
        {
            'nome': a['nome'],
            'email': a['email'],
            'rm': a.get('rm', 'N/A')
        }
        for a in alunos_turma 
        if a['email'] not in alunos_entregaram
    ]
    
    # Retorna o resumo completo da atividade e suas entregas
    return {
        'atividade': atividade,
        'entregas': entregas,
        'alunos_nao_entregaram': alunos_nao_entregaram,
        'total_alunos': len(alunos_turma),
        'total_entregas': len(entregas),
        'total_corrigidas': len([e for e in entregas if e.get('nota') is not None]),
        'total_pendentes': len([e for e in entregas if e.get('nota') is None])
    }

def get_todas_atividades_professor(professor_email):
    
    dados = carregar_json(ATIVIDADES_FILE)
    atividades = []
    
    for atividade in dados.get('atividades', {}).values():
        if atividade.get('professor_email') == professor_email:
            atividades.append(atividade)
    
    return atividades

def editar_atividade(atividade_id, titulo, descricao, data_entrega, valor):
    
    dados = carregar_json(ATIVIDADES_FILE)
    
    if atividade_id in dados.get('atividades', {}):
        # Atualiza os campos da atividade
        dados['atividades'][atividade_id].update({
            'titulo': titulo,
            'descricao': descricao,
            'data_entrega': data_entrega,
            'valor': float(valor)
        })
        salvar_json(ATIVIDADES_FILE, dados)
        return True
    
    return False

def excluir_atividade(atividade_id):
    
    dados = carregar_json(ATIVIDADES_FILE)
    
    if atividade_id in dados.get('atividades', {}):
        atividade = dados['atividades'][atividade_id]
        # Se houver um caminho de arquivo, tenta removê-lo
        if atividade.get('arquivo'):
            try:
                os.remove(atividade['arquivo'])
            except:
                pass # Ignora erro se o arquivo já tiver sido removido ou não puder ser acessado
        
        # Remove a atividade do JSON
        del dados['atividades'][atividade_id]
        salvar_json(ATIVIDADES_FILE, dados)
        return True
    
    return False

def entregar_atividade(atividade_id, aluno_email, arquivo_path=None, comentario=""):
    
    dados = carregar_json(ENTREGAS_FILE)
    
    if 'entregas' not in dados:
        dados['entregas'] = {}

    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1
    
    # Verifica duplicidade de entrega
    for entrega in dados['entregas'].values():
        if (entrega.get('atividade_id') == str(atividade_id) and 
            entrega.get('aluno_email') == aluno_email):
            return False, "Você já entregou esta atividade!"
    
    entrega_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1
    
    aluno = get_user_data(aluno_email)
    
    # Estrutura de dados da nova entrega
    entrega = {
        'id': entrega_id,
        'atividade_id': str(atividade_id),
        'aluno_email': aluno_email,
        'aluno_nome': aluno.get('nome', ''),
        'aluno_rm': aluno.get('rm', 'N/A'),
        'data_entrega': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'comentario': comentario,
        'status': 'Aguardando Correção'
    }
    
    # Bloco para lidar com o upload e salvamento do arquivo de entrega
    if arquivo_path:
        try:
            arquivo_nome = os.path.basename(arquivo_path)
            destino = ARQUIVOS_DIR / f"entrega_{entrega_id}_{arquivo_nome}"
            shutil.copy2(arquivo_path, destino)
            entrega['arquivo'] = str(destino)
            entrega['arquivo_nome'] = arquivo_nome
        except Exception as e:
            return False, f"Erro ao salvar arquivo: {str(e)}"
    
    dados['entregas'][entrega_id] = entrega
    salvar_json(ENTREGAS_FILE, dados)
    
    return True, "Atividade entregue com sucesso!"

def get_entregas_atividade(atividade_id):
    
    dados = carregar_json(ENTREGAS_FILE)
    entregas = []
    
    for entrega in dados.get('entregas', {}).values():
        if entrega.get('atividade_id') == str(atividade_id):
            entrega_copy = entrega.copy()
            
            # Define o status de correção
            if entrega.get('nota') is not None:
                entrega_copy['status'] = 'Corrigida'
            else:
                entrega_copy['status'] = 'Aguardando Correção'
            
            entregas.append(entrega_copy)
    
    return entregas

def avaliar_entrega(entrega_id, nota, feedback):
    
    dados = carregar_json(ENTREGAS_FILE)
    
    if entrega_id in dados.get('entregas', {}):
        # Atualiza os campos de avaliação
        dados['entregas'][entrega_id]['nota'] = float(nota)
        dados['entregas'][entrega_id]['feedback'] = feedback
        dados['entregas'][entrega_id]['data_avaliacao'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        dados['entregas'][entrega_id]['status'] = 'Corrigida'
        salvar_json(ENTREGAS_FILE, dados)
        return True
    
    return False

def baixar_arquivo_entrega(entrega_id, save_path):
    
    dados = carregar_json(ENTREGAS_FILE)
    entrega = dados.get('entregas', {}).get(str(entrega_id))
    
    if entrega and entrega.get('arquivo'):
        try:
            shutil.copy2(entrega['arquivo'], save_path) # Copia o arquivo
            return True
        except Exception as e:
            print(f"Erro ao baixar arquivo: {e}")
            return False
    
    return False

def get_atividades_entregues_aluno(aluno_email):
    
    dados_entregas = carregar_json(ENTREGAS_FILE)
    dados_atividades = carregar_json(ATIVIDADES_FILE)
    dados_turmas = carregar_json(TURMAS_FILE)
    
    atividades_entregues = []
    
    for entrega in dados_entregas.get('entregas', {}).values():
        if entrega.get('aluno_email') == aluno_email:
            atividade_id = entrega.get('atividade_id')
            atividade = dados_atividades.get('atividades', {}).get(atividade_id, {})
            
            if atividade:
                turma_id = atividade.get('turma_id')
                turma = dados_turmas.get('turmas', {}).get(turma_id, {})
                
                # Combina dados da atividade, da entrega e da turma
                atividade_completa = {
                    'titulo': atividade.get('titulo', 'Sem título'),
                    'descricao': atividade.get('descricao', ''),
                    'valor': atividade.get('valor', 0),
                    'data_entrega': entrega.get('data_entrega', 'N/A'),
                    'turma': turma.get('nome', 'N/A'),
                    'turma_nome': turma.get('nome', 'N/A'),
                    'disciplina': turma.get('disciplina', 'N/A'),
                    'nota': entrega.get('nota'),
                    'feedback': entrega.get('feedback', ''),
                    'entrega_id': entrega.get('id'),
                    'atividade_id': atividade_id,
                    'comentario': entrega.get('comentario', ''),
                    'arquivo': entrega.get('arquivo'),
                    'arquivo_nome': entrega.get('arquivo_nome'),
                    'status': 'Avaliada' if entrega.get('nota') is not None else 'Aguardando Correção'
                }
                
                atividades_entregues.append(atividade_completa)
    
    return atividades_entregues

# --- Funções de Avaliação e Boletim ---
def get_notas_aluno_turma(aluno_email, turma_id):
    
    atividades = get_atividades_turma(turma_id)
    entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})
    
    notas = []
    for atividade in atividades:
        for entrega in entregas.values():
            # Filtra por atividade, aluno e se a nota está presente
            if (entrega.get('atividade_id') == atividade['id'] and 
                entrega.get('aluno_email') == aluno_email and
                entrega.get('nota') is not None):
                notas.append({
                    'atividade': atividade['titulo'],
                    'nota': entrega['nota'],
                    'valor': atividade['valor'], # Valor máximo da atividade
                    'feedback': entrega.get('feedback', '')
                })
    
    return notas

def get_boletim_aluno(aluno_email):
    
    turmas = get_turmas_aluno(aluno_email)
    
    boletim = []

    for turma in turmas:
        notas = get_notas_aluno_turma(aluno_email, turma['id'])
        
        media = 0

        if notas:
            # Soma dos pontos obtidos e soma dos valores máximos das atividades
            total_pontos = sum([n['nota'] for n in notas])
            total_valor = sum([n['valor'] for n in notas])
            # Calcula a média ponderada e a escala para 10 (total_pontos/total_valor * 10)
            media = (total_pontos / total_valor * 10) if total_valor > 0 else 0
        
        frequencia = calcular_frequencia_aluno_turma(aluno_email, turma['id'])
        
        status = 'Sem notas' # Status padrão se não houver notas

        if media > 0:
            # Lógica de aprovação/reprovação
            if media >= 7 and frequencia >= 75:
                status = 'Aprovado'
            elif media < 7:
                status = 'Reprovado por nota'
            elif frequencia < 75:
                status = 'Reprovado por frequência'
        
        # Adiciona o resumo da turma ao boletim
        boletim.append({
            'turma': turma['nome'],
            'disciplina': turma['disciplina'],
            'professor': turma['professor_nome'],
            'notas': notas,
            'media': media,
            'frequencia': frequencia,
            'status': status
        })
    
    return boletim

def get_boletim_turma(turma_id):
    
    alunos = get_alunos_turma(turma_id) 
    
    boletim = []

    for aluno in alunos:
        # Obtém notas avaliadas do aluno na turma
        notas = get_notas_aluno_turma(aluno['email'], turma_id) 
        
        media = 0
        if notas:
            # Calcula a média ponderada (pontos obtidos / valor total * 10)
            total_pontos = sum([n['nota'] for n in notas])
            total_valor = sum([n['valor'] for n in notas])
            media = (total_pontos / total_valor * 10) if total_valor > 0 else 0
        
        # Calcula a frequência percentual do aluno na turma
        frequencia = calcular_frequencia_aluno_turma(aluno['email'], turma_id) 
        
        status = 'Sem notas'

        if media > 0:
            # Define o status de aprovação/reprovação (critério: média >= 7 e freq >= 75%)
            if media >= 7 and frequencia >= 75:
                status = 'Aprovado'
            elif media < 7:
                status = 'Reprovado por nota'
            elif frequencia < 75:
                status = 'Reprovado por frequência'
        
        boletim.append({
            'nome': aluno['nome'],
            'email': aluno['email'],
            'rm': aluno.get('rm', 'N/A'),
            'media': media,
            'frequencia': frequencia,
            'status': status
        })
    
    return boletim

def get_estatisticas_gerais():
    
    # Carrega todos os dados necessários
    usuarios = carregar_json(USERS_FILE).get('users', {})
    turmas_data = carregar_json(TURMAS_FILE).get('turmas', {})
    atividades_data = carregar_json(ATIVIDADES_FILE).get('atividades', {})
    entregas_data = carregar_json(ENTREGAS_FILE).get('entregas', {})
    aulas_data = carregar_json(AULAS_FILE).get('aulas', {})
    matriculas = carregar_json(MATRICULAS_FILE).get('matriculas', {}).values()
    
    # 1. Estatísticas de Usuários
    total_usuarios = len(usuarios)
    total_admins = len([u for u in usuarios.values() if u.get('role') == 'ADMIN'])
    total_professores = len([u for u in usuarios.values() if u.get('role') == 'INSTRUCTOR'])
    total_alunos = len([u for u in usuarios.values() if u.get('role') == 'USER'])
    
    # 2. Estatísticas de Turmas e Matrículas
    total_turmas = len(turmas_data)
    total_matriculas = len(matriculas)
    media_alunos_turma = total_matriculas / total_turmas if total_turmas > 0 else 0
    
    # 3. Estatísticas de Atividades e Entregas
    total_atividades = len(atividades_data)
    total_entregas = len(entregas_data)
    # Taxa de entrega = Total entregas / (Total atividades * Total alunos)
    taxa_entrega = (total_entregas / (total_atividades * total_alunos) * 100) if (total_atividades * total_alunos) > 0 else 0
    total_corrigidas = len([e for e in entregas_data.values() if e.get('nota') is not None])
    
    # 4. Estatísticas de Aulas
    total_aulas = len(aulas_data)
    
    # 5. Estatísticas de Desempenho
    entregas_com_nota = [e for e in entregas_data.values() if e.get('nota') is not None]

    if entregas_com_nota:
        medias = []
        # Normaliza cada nota para uma escala de 0 a 10 e adiciona à lista
        for entrega in entregas_com_nota:
            ativ = atividades_data.get(entrega.get('atividade_id'), {})
            if ativ.get('valor'):
                medias.append((entrega['nota'] / ativ['valor']) * 10)
        # Calcula a média geral do sistema (média das notas normalizadas)
        media_geral = sum(medias) / len(medias) if medias else 0
    else:
        media_geral = 0
    
    # Calcula a taxa de aprovação com base nas notas normalizadas (>= 7)
    aprovados = len([m for m in medias if m >= 7]) if entregas_com_nota else 0
    taxa_aprovacao = (aprovados / len(medias) * 100) if 'medias' in locals() and medias else 0
    
    return {
        'total_usuarios': total_usuarios,
        'total_admins': total_admins,
        'total_professores': total_professores,
        'total_alunos': total_alunos,
        'total_turmas': total_turmas,
        'total_matriculas': total_matriculas,
        'media_alunos_turma': media_alunos_turma,
        'total_atividades': total_atividades,
        'total_entregas': total_entregas,
        'taxa_entrega': taxa_entrega,
        'total_corrigidas': total_corrigidas,
        'media_geral_sistema': media_geral,
        'taxa_aprovacao': taxa_aprovacao,
        'total_aulas': total_aulas
    }

def get_estatisticas_detalhadas():
    
    usuarios = get_todos_usuarios('USER')
    
    alunos_com_media = []

    # 1. Top Alunos
    for usuario in usuarios:
        boletim = get_boletim_aluno(usuario['email'])
        # Filtra as médias das turmas (apenas maiores que 0)
        medias = [t['media'] for t in boletim if t.get('media') and t['media'] > 0]

        if medias:
            media_geral = sum(medias) / len(medias) # Média das médias das turmas
            alunos_com_media.append({
                'nome': usuario['nome'],
                'email': usuario['email'],
                'media': media_geral
            })
    
    # Ordena e seleciona o Top 5
    top_alunos = sorted(alunos_com_media, key=lambda x: x['media'], reverse=True)[:5]
    
    professores = get_todos_usuarios('INSTRUCTOR') 
    professores_ativos = []

    # 2. Professores Ativos (por número de atividades criadas)
    for prof in professores:
        turmas = get_turmas_professor(prof['email'])
        atividades = get_todas_atividades_professor(prof['email'])
        aulas = get_todas_aulas_professor(prof['email'])
        professores_ativos.append({
            'nome': prof['nome'],
            'email': prof['email'],
            'turmas': len(turmas),
            'atividades': len(atividades),
            'aulas': len(aulas)
        })
    
    # Ordena e seleciona o Top 5 com base no número de atividades
    professores_ativos = sorted(professores_ativos, key=lambda x: x['atividades'], reverse=True)[:5]
    
    todas_turmas = get_todas_turmas()
    turmas_com_media = []

    # 3. Melhores Turmas (por média da turma)
    for turma in todas_turmas:
        boletim = get_boletim_turma(turma['id'])
        # Filtra as médias dos alunos na turma (apenas maiores que 0)
        medias = [a['media'] for a in boletim if a.get('media') and a['media'] > 0]

        if medias:
            media_turma = sum(medias) / len(medias) # Média das médias dos alunos
            aprovados = len([m for m in medias if m >= 7])
            taxa = (aprovados / len(medias) * 100) if medias else 0
            turmas_com_media.append({
                'nome': turma['nome'],
                'id': turma['id'],
                'media': media_turma,
                'taxa_aprovacao': taxa
            })
    
    # Ordena e seleciona o Top 5 com base na média da turma
    melhores_turmas = sorted(turmas_com_media, key=lambda x: x['media'], reverse=True)[:5]
    
    return {
        'top_alunos': top_alunos,
        'professores_ativos': professores_ativos,
        'melhores_turmas': melhores_turmas
    }

def exportar_relatorio_txt(relatorio, save_path):
    
    try:
        # Abre o arquivo para escrita com codificação UTF-8
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("RELATÓRIO GERAL DO SISTEMA DE GESTÃO ESCOLAR\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            
            # Escreve a seção de USUÁRIOS
            f.write("USUÁRIOS\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de Usuários: {relatorio['total_usuarios']}\n")
            f.write(f"Administradores: {relatorio['total_admins']}\n")
            f.write(f"Professores: {relatorio['total_professores']}\n")
            f.write(f"Alunos: {relatorio['total_alunos']}\n\n")
            
            # Escreve a seção de TURMAS
            f.write("TURMAS\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de Turmas: {relatorio['total_turmas']}\n")
            f.write(f"Alunos Matriculados: {relatorio['total_matriculas']}\n")
            f.write(f"Média de Alunos/Turma: {relatorio['media_alunos_turma']:.1f}\n\n")
            
            # Escreve a seção de AULAS
            f.write("AULAS\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de Aulas Ministradas: {relatorio['total_aulas']}\n\n")
            
            # Escreve a seção de ATIVIDADES
            f.write("ATIVIDADES\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de Atividades: {relatorio['total_atividades']}\n")
            f.write(f"Atividades Entregues: {relatorio['total_entregas']}\n")
            f.write(f"Taxa de Entrega: {relatorio['taxa_entrega']:.1f}%\n")
            f.write(f"Atividades Corrigidas: {relatorio['total_corrigidas']}\n\n")
            
            # Escreve a seção de DESEMPENHO
            f.write("DESEMPENHO\n")
            f.write("-" * 40 + "\n")
            f.write(f"Média Geral do Sistema: {relatorio['media_geral_sistema']:.2f}\n")
            f.write(f"Taxa de Aprovação: {relatorio['taxa_aprovacao']:.1f}%\n")
            
            f.write("\n" + "=" * 60 + "\n")
        
        return True
    except Exception as e:
        print(f"Erro ao exportar relatório: {e}")
        return False

# --- Funções de Relatório de Aula (Diário de Bordo) ---
def criar_relatorio_aula(turma_id, aula_id, professor_email, texto):
    
    dados = carregar_json(RELATORIOS_FILE)
    
    if 'relatorios' not in dados:
        dados['relatorios'] = {}

    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1
    
    relatorio_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1
    
    # Estrutura de dados do novo relatório
    dados['relatorios'][relatorio_id] = {
        'id': relatorio_id,
        'turma_id': turma_id,
        'aula_id': aula_id,
        'professor_email': professor_email,
        'texto': texto,
        'data_criacao': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'data_finalizacao': None,
        'finalizado': False # Status inicial
    }
    
    salvar_json(RELATORIOS_FILE, dados)
    return relatorio_id

def editar_relatorio_aula(relatorio_id, novo_texto):
    
    dados = carregar_json(RELATORIOS_FILE)
    
    if relatorio_id not in dados.get('relatorios', {}):
        return False
    
    relatorio = dados['relatorios'][relatorio_id]
    
    # Verifica se o relatório pode ser editado
    if relatorio.get('finalizado', False):
        return False
    
    dados['relatorios'][relatorio_id]['texto'] = novo_texto
    salvar_json(RELATORIOS_FILE, dados)
    return True

def finalizar_relatorio_aula(relatorio_id):
    
    dados = carregar_json(RELATORIOS_FILE)
    
    if relatorio_id not in dados.get('relatorios', {}):
        return False
    
    # Define os campos de finalização
    dados['relatorios'][relatorio_id]['finalizado'] = True
    dados['relatorios'][relatorio_id]['data_finalizacao'] = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    salvar_json(RELATORIOS_FILE, dados)
    return True

def get_relatorio_por_aula(aula_id):
    
    dados = carregar_json(RELATORIOS_FILE)
    
    for relatorio in dados.get('relatorios', {}).values():
        if relatorio.get('aula_id') == aula_id:
            return relatorio
    
    return None

def get_relatorios_professor(professor_email):
    
    dados = carregar_json(RELATORIOS_FILE)
    relatorios = []
    
    for relatorio in dados.get('relatorios', {}).values():
        if relatorio.get('professor_email') == professor_email:
            relatorio_copy = relatorio.copy()
            
            # Adiciona detalhes da Turma
            turma = carregar_json(TURMAS_FILE).get('turmas', {}).get(relatorio['turma_id'])

            if turma:
                relatorio_copy['turma_nome'] = turma.get('nome', 'N/A')
                relatorio_copy['disciplina'] = turma.get('disciplina', 'N/A')
            
            # Adiciona detalhes da Aula
            aula = get_aula_by_id(relatorio['aula_id']) 

            if aula:
                relatorio_copy['aula_titulo'] = aula.get('titulo', 'N/A')
                relatorio_copy['aula_data'] = aula.get('data', 'N/A')
            
            relatorios.append(relatorio_copy)
    
    return relatorios

def get_relatorios_turma(turma_id):
    
    dados = carregar_json(RELATORIOS_FILE)
    relatorios = []
    
    for relatorio in dados.get('relatorios', {}).values():
        if relatorio.get('turma_id') == turma_id:
            relatorio_copy = relatorio.copy()
            
            # Adiciona detalhes da Aula
            aula = get_aula_by_id(relatorio['aula_id'])

            if aula:
                relatorio_copy['aula_titulo'] = aula.get('titulo', 'N/A')
                relatorio_copy['aula_data'] = aula.get('data', 'N/A')
            
            relatorios.append(relatorio_copy)
    
    return relatorios

def get_todos_relatorios():
    
    dados = carregar_json(RELATORIOS_FILE)
    relatorios = []
    
    for relatorio in dados.get('relatorios', {}).values():
        relatorio_copy = relatorio.copy()
        
        # Adiciona detalhes do Professor
        professor = get_user_data(relatorio['professor_email'])

        if professor:
            relatorio_copy['professor_nome'] = professor.get('nome', 'N/A')
        
        # Adiciona detalhes da Turma
        turma = carregar_json(TURMAS_FILE).get('turmas', {}).get(relatorio['turma_id'])

        if turma:
            relatorio_copy['turma_nome'] = turma.get('nome', 'N/A')
            relatorio_copy['disciplina'] = turma.get('disciplina', 'N/A')
        
        # Adiciona detalhes da Aula
        aula = get_aula_by_id(relatorio['aula_id'])
        
        if aula:
            relatorio_copy['aula_titulo'] = aula.get('titulo', 'N/A')
            relatorio_copy['aula_data'] = aula.get('data', 'N/A')
        
        relatorios.append(relatorio_copy)
    
    return relatorios

def get_aula_by_id(aula_id):
    
    dados = carregar_json(AULAS_FILE)
    return dados.get('aulas', {}).get(aula_id)
    
# --- Funções de Manutenção do Sistema (Limpeza) ---
def limpar_turmas_antigas():
    
    ano_atual = datetime.now().year
    dados = carregar_json(TURMAS_FILE)
    
    turmas_removidas = 0
    turmas_mantidas = {}
    
    for turma_id, turma in dados.get('turmas', {}).items():
        ano_turma = turma.get('ano', '')
        try:
            # Compara o ano da turma com o ano atual
            if int(ano_turma) < ano_atual:
                turmas_removidas += 1
            else:
                turmas_mantidas[turma_id] = turma
        except:
            # Mantém turmas com ano inválido/ausente para evitar perda de dados
            turmas_mantidas[turma_id] = turma
    
    dados['turmas'] = turmas_mantidas
    salvar_json(TURMAS_FILE, dados)
    return turmas_removidas

def limpar_atividades_antigas():
    
    # Define o limite de tempo (um ano atrás)
    data_limite = datetime.now() - timedelta(days=365)
    
    dados = carregar_json(ATIVIDADES_FILE)
    atividades_removidas = 0
    atividades_mantidas = {}
    
    for ativ_id, atividade in dados.get('atividades', {}).items():
        try:
            # Tenta converter a data de criação para comparação
            data_criacao = datetime.strptime(atividade.get('data_criacao', ''), "%d/%m/%Y %H:%M")
            if data_criacao > data_limite:
                atividades_mantidas[ativ_id] = atividade
            else:
                atividades_removidas += 1
        except:
            # Mantém atividades com data inválida/ausente
            atividades_mantidas[ativ_id] = atividade
    
    dados['atividades'] = atividades_mantidas
    salvar_json(ATIVIDADES_FILE, dados)
    return atividades_removidas

def arquivar_usuarios_inativos():
    
    return 0


def get_atividades_pendentes_aluno(aluno_email):
    
    turmas = get_turmas_aluno(aluno_email)
    entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})
    
    atividades_pendentes = []
    
    for turma in turmas:
        atividades = get_atividades_turma(turma['id'])
        
        for atividade in atividades:
            ja_entregou = False
            # Verifica se o aluno já fez uma entrega para esta atividade
            for entrega in entregas.values():
                if (entrega.get('atividade_id') == atividade['id'] and 
                    entrega.get('aluno_email') == aluno_email):
                    ja_entregou = True
                    break
            
            # Se não entregou, adiciona à lista de pendentes
            if not ja_entregou:
                ativ_copy = atividade.copy()
                ativ_copy['turma_nome'] = turma['nome']
                ativ_copy['disciplina'] = turma['disciplina']
                ativ_copy['status'] = 'Pendente'
                atividades_pendentes.append(ativ_copy)
    
    # Ordena as atividades pendentes pela data de entrega
    atividades_pendentes.sort(key=lambda x: datetime.strptime(x['data_entrega'], "%d/%m/%Y"))
    
    return atividades_pendentes

def get_relatorio_geral():
    
    return get_estatisticas_gerais()