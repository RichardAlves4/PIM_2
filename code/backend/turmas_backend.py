import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import base64

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"

TURMAS_FILE = DATABASE_DIR / "turmas.json"
AULAS_FILE = DATABASE_DIR / "aulas.json"
ATIVIDADES_FILE = DATABASE_DIR / "atividades.json"
ENTREGAS_FILE = DATABASE_DIR / "entregas.json"
MATRICULAS_FILE = DATABASE_DIR / "matriculas.json"
USERS_FILE = DATABASE_DIR / "users.json"
FREQUENCIA_FILE = DATABASE_DIR / "frequencia.json"
ARQUIVOS_DIR = DATABASE_DIR / "arquivos"

ARQUIVOS_DIR.mkdir(exist_ok=True)

def carregar_json(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def salvar_json(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=5, ensure_ascii=False)

def get_user_data(email):
    dados = carregar_json(USERS_FILE)
    usuario = dados.get('users', {}).get(email, {})
    if usuario:
        usuario['email'] = email
    return usuario

def get_todos_usuarios(filtro='TODOS'):
    dados = carregar_json(USERS_FILE)
    usuarios = dados.get('users', {})
    
    lista_usuarios = []
    for email, user_data in usuarios.items():
        user_info = user_data.copy()
        user_info['email'] = email
        if filtro == 'TODOS' or user_data.get('role') == filtro:
            lista_usuarios.append(user_info)
    
    return lista_usuarios

def get_detalhes_completos_usuario(email):
    user_data = get_user_data(email)
    if not user_data:
        return None
    
    detalhes = user_data.copy()
    detalhes['data_cadastro'] = "N/A"
    
    if user_data.get('role') == 'INSTRUCTOR':
        turmas = get_turmas_professor(email)
        detalhes['total_turmas'] = len(turmas)
        detalhes['total_alunos'] = sum([t.get('total_alunos', 0) for t in turmas])
        atividades = get_todas_atividades_professor(email)
        detalhes['total_atividades'] = len(atividades)
        aulas = get_todas_aulas_professor(email)
        detalhes['total_aulas'] = len(aulas)
    
    elif user_data.get('role') == 'USER':
        turmas = get_turmas_aluno(email)
        detalhes['total_turmas'] = len(turmas)
        entregas = get_atividades_entregues_aluno(email)
        detalhes['atividades_entregues'] = len(entregas)
        boletim = get_boletim_aluno(email)
        medias = [t['media'] for t in boletim if t.get('media') and t['media'] > 0]
        detalhes['media_geral'] = sum(medias) / len(medias) if medias else 0
        frequencia_media = calcular_frequencia_media_aluno(email)
        detalhes['frequencia_media'] = frequencia_media
    
    return detalhes

def editar_usuario(email, nome, role, senha_criptografada=None):
    dados = carregar_json(USERS_FILE)

    if email in dados.get('users', {}) and senha_criptografada is None:
        dados['users'][email]['nome'] = nome
        dados['users'][email]['role'] = role
        salvar_json(USERS_FILE, dados)
        dados = carregar_json(USERS_FILE)
        return True
    elif email in dados.get('users', {}) and senha_criptografada is not None:
        dados['users'][email]['nome'] = nome
        dados['users'][email]['role'] = role
        dados['users'][email]['senha'] = senha_criptografada
        salvar_json(USERS_FILE, dados)
        dados = carregar_json(USERS_FILE)
        return True
    else:
        return False
    
def excluir_usuario(email):
    dados = carregar_json(USERS_FILE)
    if email in dados.get('users', {}):
        del dados['users'][email]
        salvar_json(USERS_FILE, dados)
        return True
    return False

def adicionar_usuario(nome, email, senha, role):
    dados = carregar_json(USERS_FILE)
    if 'users' not in dados:
        dados['users'] = {}
    
    if email in dados['users']:
        return False
    
    from infra.security import criptografar_senha
    from database.banco import gerar_rm
    
    user_data = {
        'nome': nome,
        'senha': criptografar_senha(senha),
        'role': role
    }
    
    # Adicionar RM apenas para alunos
    if role == 'USER':
        user_data['rm'] = gerar_rm()
    
    dados['users'][email] = user_data
    salvar_json(USERS_FILE, dados)
    return True

def criar_turma(professor_email, nome, disciplina, ano, periodo, descricao):
    dados = carregar_json(TURMAS_FILE)
    
    if 'turmas' not in dados:
        dados['turmas'] = {}
    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1
    
    turma_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1
    
    professor = get_user_data(professor_email)
    
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
    return True

def get_turmas_professor(professor_email):
    dados = carregar_json(TURMAS_FILE)
    matriculas = carregar_json(MATRICULAS_FILE).get('matriculas', {})
    
    turmas_prof = []
    for turma_id, turma in dados.get('turmas', {}).items():
        if turma.get('professor_email') == professor_email:
            turma_copy = turma.copy()
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
    detalhes['total_aulas'] = len([a for a in aulas.values() if a.get('turma_id') == str(turma_id)])
    detalhes['total_atividades'] = len([a for a in atividades.values() if a.get('turma_id') == str(turma_id)])
    
    return detalhes

def get_alunos_turma(turma_id):
    matriculas = carregar_json(MATRICULAS_FILE).get('matriculas', {})
    
    alunos = []
    for matricula in matriculas.values():
        if matricula.get('turma_id') == str(turma_id):
            aluno_email = matricula.get('aluno_email')
            aluno_data = get_user_data(aluno_email)
            if aluno_data:
                alunos.append(aluno_data)
    
    return alunos

def adicionar_aluno_turma(turma_id, aluno_email):
    matriculas = carregar_json(MATRICULAS_FILE)
    
    if 'matriculas' not in matriculas:
        matriculas['matriculas'] = {}
    if 'proximo_id' not in matriculas:
        matriculas['proximo_id'] = 1
    
    # Verificar se já está matriculado
    for matricula in matriculas['matriculas'].values():
        if (matricula.get('turma_id') == str(turma_id) and 
            matricula.get('aluno_email') == aluno_email):
            return False
    
    matricula_id = str(matriculas['proximo_id'])
    matriculas['proximo_id'] += 1
    
    matriculas['matriculas'][matricula_id] = {
        'id': matricula_id,
        'turma_id': str(turma_id),
        'aluno_email': aluno_email,
        'data_matricula': datetime.now().strftime("%d/%m/%Y")
    }
    
    salvar_json(MATRICULAS_FILE, matriculas)
    return True

def remover_aluno_turma(turma_id, aluno_email):
    matriculas = carregar_json(MATRICULAS_FILE)
    
    matricula_id_remover = None
    for matricula_id, matricula in matriculas.get('matriculas', {}).items():
        if (matricula.get('turma_id') == str(turma_id) and 
            matricula.get('aluno_email') == aluno_email):
            matricula_id_remover = matricula_id
            break
    
    if matricula_id_remover:
        del matriculas['matriculas'][matricula_id_remover]
        salvar_json(MATRICULAS_FILE, matriculas)
        return True
    
    return False

# ==================== SISTEMA DE AULAS ====================

def registrar_aula(turma_id, data, titulo, conteudo, observacoes=""):
    dados = carregar_json(AULAS_FILE)
    
    if 'aulas' not in dados:
        dados['aulas'] = {}
    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1
    
    aula_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1
    
    turma = carregar_json(TURMAS_FILE).get('turmas', {}).get(str(turma_id), {})
    
    dados['aulas'][aula_id] = {
        'id': aula_id,
        'turma_id': str(turma_id),
        'data': data,
        'titulo': titulo,
        'conteudo': conteudo,
        'observacoes': observacoes,
        'professor_email': turma.get('professor_email', ''),
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
    
    # Ordenar por data
    aulas.sort(key=lambda x: datetime.strptime(x['data'], "%d/%m/%Y"), reverse=True)
    return aulas

def get_todas_aulas_professor(professor_email):
    dados = carregar_json(AULAS_FILE)
    aulas = []
    
    for aula in dados.get('aulas', {}).values():
        if aula.get('professor_email') == professor_email:
            aulas.append(aula)
    
    return aulas

def editar_aula(aula_id, data, titulo, conteudo, observacoes):
    dados = carregar_json(AULAS_FILE)
    
    if aula_id in dados.get('aulas', {}):
        dados['aulas'][aula_id].update({
            'data': data,
            'titulo': titulo,
            'conteudo': conteudo,
            'observacoes': observacoes
        })
        salvar_json(AULAS_FILE, dados)
        return True
    
    return False

def excluir_aula(aula_id):
    dados = carregar_json(AULAS_FILE)
    
    if aula_id in dados.get('aulas', {}):
        del dados['aulas'][aula_id]
        salvar_json(AULAS_FILE, dados)
        return True
    
    return False

# ==================== SISTEMA DE FREQUÊNCIA ====================

def registrar_frequencia(aula_id, aluno_email, presente):
    """Registra presença ou falta de um aluno em uma aula"""
    dados = carregar_json(FREQUENCIA_FILE)
    
    if 'frequencias' not in dados:
        dados['frequencias'] = {}
    
    # ID único: aula_id + aluno_email
    freq_id = f"{aula_id}_{aluno_email}"
    
    dados['frequencias'][freq_id] = {
        'aula_id': str(aula_id),
        'aluno_email': aluno_email,
        'presente': presente,
        'data_registro': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    salvar_json(FREQUENCIA_FILE, dados)
    return True

def calcular_frequencia_aluno_turma(aluno_email, turma_id):
    """Calcula a frequência percentual de um aluno em uma turma"""
    aulas = get_aulas_turma(turma_id)
    
    if not aulas:
        return 100.0
    
    dados_freq = carregar_json(FREQUENCIA_FILE)
    presencas = 0
    total_aulas = len(aulas)
    
    for aula in aulas:
        freq_id = f"{aula['id']}_{aluno_email}"
        if freq_id in dados_freq.get('frequencias', {}):
            if dados_freq['frequencias'][freq_id].get('presente'):
                presencas += 1
    
    return (presencas / total_aulas * 100) if total_aulas > 0 else 100.0

def calcular_frequencia_media_aluno(aluno_email):
    """Calcula a frequência média de um aluno em todas as suas turmas"""
    turmas = get_turmas_aluno(aluno_email)
    
    if not turmas:
        return 100.0
    
    frequencias = []
    for turma in turmas:
        freq = calcular_frequencia_aluno_turma(aluno_email, turma['id'])
        frequencias.append(freq)
    
    return sum(frequencias) / len(frequencias) if frequencias else 100.0

def get_relatorio_frequencia_turma(turma_id):
    """Obtém relatório completo de frequência de uma turma"""
    alunos = get_alunos_turma(turma_id)
    aulas = get_aulas_turma(turma_id)
    
    relatorio = []
    for aluno in alunos:
        freq_percentual = calcular_frequencia_aluno_turma(aluno['email'], turma_id)
        
        # Contar presenças e faltas
        presencas = 0
        faltas = 0
        
        dados_freq = carregar_json(FREQUENCIA_FILE)
        for aula in aulas:
            freq_id = f"{aula['id']}_{aluno['email']}"
            if freq_id in dados_freq.get('frequencias', {}):
                if dados_freq['frequencias'][freq_id].get('presente'):
                    presencas += 1
                else:
                    faltas += 1
        
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

# ==================== SISTEMA DE ATIVIDADES (COMPLETO) ====================

def criar_atividade(turma_id, titulo, descricao, data_entrega, valor, arquivo_path=None):
    """Cria uma nova atividade"""
    dados = carregar_json(ATIVIDADES_FILE)
    
    if 'atividades' not in dados:
        dados['atividades'] = {}
    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1
    
    atividade_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1
    
    turma = carregar_json(TURMAS_FILE).get('turmas', {}).get(str(turma_id), {})
    
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
    
    # Salvar arquivo anexado se houver
    if arquivo_path:
        try:
            arquivo_nome = os.path.basename(arquivo_path)
            destino = ARQUIVOS_DIR / f"atividade_{atividade_id}_{arquivo_nome}"
            shutil.copy2(arquivo_path, destino)
            atividade['arquivo'] = str(destino)
            atividade['arquivo_nome'] = arquivo_nome
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
    
    dados['atividades'][atividade_id] = atividade
    salvar_json(ATIVIDADES_FILE, dados)
    
    return atividade_id

def get_atividades_turma(turma_id):
    """Obtém todas as atividades de uma turma"""
    dados = carregar_json(ATIVIDADES_FILE)
    atividades = []
    
    for atividade in dados.get('atividades', {}).values():
        if atividade.get('turma_id') == str(turma_id):
            atividades.append(atividade)
    
    # Ordenar por data de entrega
    atividades.sort(key=lambda x: datetime.strptime(x['data_entrega'], "%d/%m/%Y"))
    return atividades

def get_atividades_turma_aluno(turma_id, aluno_email):
    """Obtém atividades de uma turma com status de entrega do aluno"""
    atividades = get_atividades_turma(turma_id)
    entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})
    
    atividades_aluno = []
    for atividade in atividades:
        ativ_copy = atividade.copy()
        
        # Verificar se o aluno já entregou
        entrega_aluno = None
        for entrega in entregas.values():
            if (entrega.get('atividade_id') == atividade['id'] and 
                entrega.get('aluno_email') == aluno_email):
                entrega_aluno = entrega
                break
        
        ativ_copy['entregue'] = entrega_aluno is not None
        ativ_copy['status'] = 'Entregue' if entrega_aluno else 'Pendente'
        
        if entrega_aluno:
            ativ_copy['data_entrega_aluno'] = entrega_aluno.get('data_entrega')
            ativ_copy['nota'] = entrega_aluno.get('nota')
            ativ_copy['feedback'] = entrega_aluno.get('feedback', '')
            ativ_copy['entrega_id'] = entrega_aluno.get('id')
            
            # Status mais detalhado
            if entrega_aluno.get('nota') is not None:
                ativ_copy['status'] = 'Avaliada'
            else:
                ativ_copy['status'] = 'Aguardando Correção'
        
        atividades_aluno.append(ativ_copy)
    
    return atividades_aluno

def get_atividades_com_entregas(professor_email):
    """NOVA FUNÇÃO: Obtém todas as atividades do professor com informações de entregas"""
    atividades = get_todas_atividades_professor(professor_email)
    entregas_dados = carregar_json(ENTREGAS_FILE).get('entregas', {})
    turmas_dados = carregar_json(TURMAS_FILE).get('turmas', {})
    
    atividades_completas = []
    for atividade in atividades:
        ativ_copy = atividade.copy()
        
        # Adicionar informações da turma
        turma = turmas_dados.get(atividade['turma_id'], {})
        ativ_copy['turma_nome'] = turma.get('nome', 'N/A')
        ativ_copy['disciplina'] = turma.get('disciplina', 'N/A')
        
        # Contar entregas
        entregas_atividade = [e for e in entregas_dados.values() 
                             if e.get('atividade_id') == atividade['id']]
        
        ativ_copy['total_entregas'] = len(entregas_atividade)
        ativ_copy['entregas_corrigidas'] = len([e for e in entregas_atividade 
                                                if e.get('nota') is not None])
        ativ_copy['entregas_pendentes'] = len([e for e in entregas_atividade 
                                               if e.get('nota') is None])
        
        # Total de alunos na turma
        alunos_turma = get_alunos_turma(atividade['turma_id'])
        ativ_copy['total_alunos'] = len(alunos_turma)
        
        atividades_completas.append(ativ_copy)
    
    return atividades_completas

def get_detalhes_atividade_professor(atividade_id):
    """NOVA FUNÇÃO: Obtém detalhes completos de uma atividade para o professor"""
    dados_atividades = carregar_json(ATIVIDADES_FILE)
    entregas_dados = carregar_json(ENTREGAS_FILE).get('entregas', {})
    
    atividade = dados_atividades.get('atividades', {}).get(str(atividade_id))
    if not atividade:
        return None
    
    # Obter todas as entregas desta atividade
    entregas = []
    for entrega in entregas_dados.values():
        if entrega.get('atividade_id') == str(atividade_id):
            entrega_copy = entrega.copy()
            
            # Adicionar informações do aluno
            aluno = get_user_data(entrega['aluno_email'])
            entrega_copy['aluno_nome'] = aluno.get('nome', 'N/A')
            entrega_copy['aluno_rm'] = aluno.get('rm', 'N/A')
            
            # Status da entrega
            if entrega.get('nota') is not None:
                entrega_copy['status'] = 'Corrigida'
            else:
                entrega_copy['status'] = 'Aguardando Correção'
            
            entregas.append(entrega_copy)
    
    # Alunos que não entregaram
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
    """Obtém todas as atividades criadas por um professor"""
    dados = carregar_json(ATIVIDADES_FILE)
    atividades = []
    
    for atividade in dados.get('atividades', {}).values():
        if atividade.get('professor_email') == professor_email:
            atividades.append(atividade)
    
    return atividades

def editar_atividade(atividade_id, titulo, descricao, data_entrega, valor):
    """Edita uma atividade existente"""
    dados = carregar_json(ATIVIDADES_FILE)
    
    if atividade_id in dados.get('atividades', {}):
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
    """Exclui uma atividade"""
    dados = carregar_json(ATIVIDADES_FILE)
    
    if atividade_id in dados.get('atividades', {}):
        # Remover arquivo se existir
        atividade = dados['atividades'][atividade_id]
        if atividade.get('arquivo'):
            try:
                os.remove(atividade['arquivo'])
            except:
                pass
        
        del dados['atividades'][atividade_id]
        salvar_json(ATIVIDADES_FILE, dados)
        return True
    
    return False

def entregar_atividade(atividade_id, aluno_email, arquivo_path=None, comentario=""):
    """Aluno entrega uma atividade"""
    dados = carregar_json(ENTREGAS_FILE)
    
    if 'entregas' not in dados:
        dados['entregas'] = {}
    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1
    
    # Verificar se já existe entrega
    for entrega in dados['entregas'].values():
        if (entrega.get('atividade_id') == str(atividade_id) and 
            entrega.get('aluno_email') == aluno_email):
            # Já entregou
            return False, "Você já entregou esta atividade!"
    
    entrega_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1
    
    aluno = get_user_data(aluno_email)
    
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
    
    # Salvar arquivo se houver
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
    """Obtém todas as entregas de uma atividade"""
    dados = carregar_json(ENTREGAS_FILE)
    entregas = []
    
    for entrega in dados.get('entregas', {}).values():
        if entrega.get('atividade_id') == str(atividade_id):
            entrega_copy = entrega.copy()
            
            # Adicionar status atualizado
            if entrega.get('nota') is not None:
                entrega_copy['status'] = 'Corrigida'
            else:
                entrega_copy['status'] = 'Aguardando Correção'
            
            entregas.append(entrega_copy)
    
    return entregas

def avaliar_entrega(entrega_id, nota, feedback):
    """Professor avalia uma entrega"""
    dados = carregar_json(ENTREGAS_FILE)
    
    if entrega_id in dados.get('entregas', {}):
        dados['entregas'][entrega_id]['nota'] = float(nota)
        dados['entregas'][entrega_id]['feedback'] = feedback
        dados['entregas'][entrega_id]['data_avaliacao'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        dados['entregas'][entrega_id]['status'] = 'Corrigida'
        salvar_json(ENTREGAS_FILE, dados)
        return True
    
    return False

def baixar_arquivo_entrega(entrega_id, save_path):
    """Baixa o arquivo de uma entrega"""
    dados = carregar_json(ENTREGAS_FILE)
    entrega = dados.get('entregas', {}).get(str(entrega_id))
    
    if entrega and entrega.get('arquivo'):
        try:
            shutil.copy2(entrega['arquivo'], save_path)
            return True
        except Exception as e:
            print(f"Erro ao baixar arquivo: {e}")
            return False
    
    return False

def get_atividades_entregues_aluno(aluno_email):
    """Obtém todas as atividades que o aluno entregou COM DADOS COMPLETOS"""
    dados_entregas = carregar_json(ENTREGAS_FILE)
    dados_atividades = carregar_json(ATIVIDADES_FILE)
    dados_turmas = carregar_json(TURMAS_FILE)
    
    atividades_entregues = []
    
    for entrega in dados_entregas.get('entregas', {}).values():
        if entrega.get('aluno_email') == aluno_email:
            # Buscar dados da atividade
            atividade_id = entrega.get('atividade_id')
            atividade = dados_atividades.get('atividades', {}).get(atividade_id, {})
            
            if atividade:
                # Buscar dados da turma
                turma_id = atividade.get('turma_id')
                turma = dados_turmas.get('turmas', {}).get(turma_id, {})
                
                # Combinar dados
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

def get_notas_aluno_turma(aluno_email, turma_id):
    """Obtém as notas de um aluno em uma turma específica"""
    atividades = get_atividades_turma(turma_id)
    entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})
    
    notas = []
    for atividade in atividades:
        for entrega in entregas.values():
            if (entrega.get('atividade_id') == atividade['id'] and 
                entrega.get('aluno_email') == aluno_email and
                entrega.get('nota') is not None):
                notas.append({
                    'atividade': atividade['titulo'],
                    'nota': entrega['nota'],
                    'valor': atividade['valor'],
                    'feedback': entrega.get('feedback', '')
                })
    
    return notas

# ==================== SISTEMA DE BOLETIM ====================

def get_boletim_aluno(aluno_email):
    """Gera o boletim completo de um aluno"""
    turmas = get_turmas_aluno(aluno_email)
    
    boletim = []
    for turma in turmas:
        notas = get_notas_aluno_turma(aluno_email, turma['id'])
        
        # Calcular média
        media = 0
        if notas:
            total_pontos = sum([n['nota'] for n in notas])
            total_valor = sum([n['valor'] for n in notas])
            media = (total_pontos / total_valor * 10) if total_valor > 0 else 0
        
        # Calcular frequência
        frequencia = calcular_frequencia_aluno_turma(aluno_email, turma['id'])
        
        # Status de aprovação
        status = 'Sem notas'
        if media > 0:
            if media >= 7 and frequencia >= 75:
                status = 'Aprovado'
            elif media < 7:
                status = 'Reprovado por nota'
            elif frequencia < 75:
                status = 'Reprovado por frequência'
        
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
    """Gera o boletim de uma turma inteira"""
    alunos = get_alunos_turma(turma_id)
    
    boletim = []
    for aluno in alunos:
        notas = get_notas_aluno_turma(aluno['email'], turma_id)
        
        media = 0
        if notas:
            total_pontos = sum([n['nota'] for n in notas])
            total_valor = sum([n['valor'] for n in notas])
            media = (total_pontos / total_valor * 10) if total_valor > 0 else 0
        
        frequencia = calcular_frequencia_aluno_turma(aluno['email'], turma_id)
        
        # Status de aprovação
        status = 'Sem notas'
        if media > 0:
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

# ==================== RELATÓRIOS E ESTATÍSTICAS ====================

def get_estatisticas_gerais():
    """Calcula estatísticas gerais do sistema"""
    usuarios = carregar_json(USERS_FILE).get('users', {})
    turmas_data = carregar_json(TURMAS_FILE).get('turmas', {})
    atividades_data = carregar_json(ATIVIDADES_FILE).get('atividades', {})
    entregas_data = carregar_json(ENTREGAS_FILE).get('entregas', {})
    aulas_data = carregar_json(AULAS_FILE).get('aulas', {})
    matriculas = carregar_json(MATRICULAS_FILE).get('matriculas', {}).values()
    
    total_usuarios = len(usuarios)
    total_admins = len([u for u in usuarios.values() if u.get('role') == 'ADMIN'])
    total_professores = len([u for u in usuarios.values() if u.get('role') == 'INSTRUCTOR'])
    total_alunos = len([u for u in usuarios.values() if u.get('role') == 'USER'])
    
    total_turmas = len(turmas_data)
    total_matriculas = len(matriculas)
    media_alunos_turma = total_matriculas / total_turmas if total_turmas > 0 else 0
    
    total_atividades = len(atividades_data)
    total_entregas = len(entregas_data)
    taxa_entrega = (total_entregas / (total_atividades * total_alunos) * 100) if (total_atividades * total_alunos) > 0 else 0
    total_corrigidas = len([e for e in entregas_data.values() if e.get('nota') is not None])
    
    total_aulas = len(aulas_data)
    
    entregas_com_nota = [e for e in entregas_data.values() if e.get('nota') is not None]
    if entregas_com_nota:
        medias = []
        for entrega in entregas_com_nota:
            ativ = atividades_data.get(entrega.get('atividade_id'), {})
            if ativ.get('valor'):
                medias.append((entrega['nota'] / ativ['valor']) * 10)
        media_geral = sum(medias) / len(medias) if medias else 0
    else:
        media_geral = 0
    
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
    """Gera estatísticas detalhadas do sistema"""
    usuarios = get_todos_usuarios('USER')
    
    alunos_com_media = []
    for usuario in usuarios:
        boletim = get_boletim_aluno(usuario['email'])
        medias = [t['media'] for t in boletim if t.get('media') and t['media'] > 0]
        if medias:
            media_geral = sum(medias) / len(medias)
            alunos_com_media.append({
                'nome': usuario['nome'],
                'email': usuario['email'],
                'media': media_geral
            })
    
    top_alunos = sorted(alunos_com_media, key=lambda x: x['media'], reverse=True)[:5]
    
    professores = get_todos_usuarios('INSTRUCTOR')
    professores_ativos = []
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
    
    professores_ativos = sorted(professores_ativos, key=lambda x: x['atividades'], reverse=True)[:5]
    
    todas_turmas = get_todas_turmas()
    turmas_com_media = []
    for turma in todas_turmas:
        boletim = get_boletim_turma(turma['id'])
        medias = [a['media'] for a in boletim if a.get('media') and a['media'] > 0]
        if medias:
            media_turma = sum(medias) / len(medias)
            aprovados = len([m for m in medias if m >= 7])
            taxa = (aprovados / len(medias) * 100) if medias else 0
            turmas_com_media.append({
                'nome': turma['nome'],
                'id': turma['id'],
                'media': media_turma,
                'taxa_aprovacao': taxa
            })
    
    melhores_turmas = sorted(turmas_com_media, key=lambda x: x['media'], reverse=True)[:5]
    
    return {
        'top_alunos': top_alunos,
        'professores_ativos': professores_ativos,
        'melhores_turmas': melhores_turmas
    }

def exportar_relatorio_txt(relatorio, save_path):
    """Exporta relatório em formato TXT"""
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("RELATÓRIO GERAL DO SISTEMA DE GESTÃO ESCOLAR\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            
            f.write("USUÁRIOS\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de Usuários: {relatorio['total_usuarios']}\n")
            f.write(f"Administradores: {relatorio['total_admins']}\n")
            f.write(f"Professores: {relatorio['total_professores']}\n")
            f.write(f"Alunos: {relatorio['total_alunos']}\n\n")
            
            f.write("TURMAS\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de Turmas: {relatorio['total_turmas']}\n")
            f.write(f"Alunos Matriculados: {relatorio['total_matriculas']}\n")
            f.write(f"Média de Alunos/Turma: {relatorio['media_alunos_turma']:.1f}\n\n")
            
            f.write("AULAS\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de Aulas Ministradas: {relatorio['total_aulas']}\n\n")
            
            f.write("ATIVIDADES\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de Atividades: {relatorio['total_atividades']}\n")
            f.write(f"Atividades Entregues: {relatorio['total_entregas']}\n")
            f.write(f"Taxa de Entrega: {relatorio['taxa_entrega']:.1f}%\n")
            f.write(f"Atividades Corrigidas: {relatorio['total_corrigidas']}\n\n")
            
            f.write("DESEMPENHO\n")
            f.write("-" * 40 + "\n")
            f.write(f"Média Geral do Sistema: {relatorio['media_geral_sistema']:.2f}\n")
            f.write(f"Taxa de Aprovação: {relatorio['taxa_aprovacao']:.1f}%\n")
            
            f.write("\n" + "=" * 60 + "\n")
        
        return True
    except Exception as e:
        print(f"Erro ao exportar relatório: {e}")
        return False

# ==================== LIMPEZA DE DADOS ====================

def limpar_turmas_antigas():
    """Remove turmas de anos anteriores"""
    ano_atual = datetime.now().year
    dados = carregar_json(TURMAS_FILE)
    
    turmas_removidas = 0
    turmas_mantidas = {}
    
    for turma_id, turma in dados.get('turmas', {}).items():
        ano_turma = turma.get('ano', '')
        try:
            if int(ano_turma) < ano_atual:
                turmas_removidas += 1
            else:
                turmas_mantidas[turma_id] = turma
        except:
            turmas_mantidas[turma_id] = turma
    
    dados['turmas'] = turmas_mantidas
    salvar_json(TURMAS_FILE, dados)
    return turmas_removidas

def limpar_atividades_antigas():
    """Remove atividades antigas"""
    data_limite = datetime.now() - timedelta(days=365)
    
    dados = carregar_json(ATIVIDADES_FILE)
    atividades_removidas = 0
    atividades_mantidas = {}
    
    for ativ_id, atividade in dados.get('atividades', {}).items():
        try:
            data_criacao = datetime.strptime(atividade.get('data_criacao', ''), "%d/%m/%Y %H:%M")
            if data_criacao > data_limite:
                atividades_mantidas[ativ_id] = atividade
            else:
                atividades_removidas += 1
        except:
            atividades_mantidas[ativ_id] = atividade
    
    dados['atividades'] = atividades_mantidas
    salvar_json(ATIVIDADES_FILE, dados)
    return atividades_removidas

def arquivar_usuarios_inativos():
    """Arquiva usuários inativos (funcionalidade placeholder)"""
    return 0

def get_atividades_pendentes_aluno(aluno_email):
    """Obtém todas as atividades que o aluno ainda não entregou"""
    turmas = get_turmas_aluno(aluno_email)
    entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})
    
    atividades_pendentes = []
    
    for turma in turmas:
        atividades = get_atividades_turma(turma['id'])
        
        for atividade in atividades:
            # Verificar se já entregou
            ja_entregou = False
            for entrega in entregas.values():
                if (entrega.get('atividade_id') == atividade['id'] and 
                    entrega.get('aluno_email') == aluno_email):
                    ja_entregou = True
                    break
            
            if not ja_entregou:
                ativ_copy = atividade.copy()
                ativ_copy['turma_nome'] = turma['nome']
                ativ_copy['disciplina'] = turma['disciplina']
                ativ_copy['status'] = 'Pendente'
                atividades_pendentes.append(ativ_copy)
    
    # Ordenar por data de entrega
    atividades_pendentes.sort(key=lambda x: datetime.strptime(x['data_entrega'], "%d/%m/%Y"))
    
    return atividades_pendentes