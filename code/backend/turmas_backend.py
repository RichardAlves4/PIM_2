import json
import os
from datetime import datetime
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"

TURMAS_FILE = DATABASE_DIR / "turmas.json"
AULAS_FILE = DATABASE_DIR / "aulas.json"
ATIVIDADES_FILE = DATABASE_DIR / "atividades.json"
ENTREGAS_FILE = DATABASE_DIR / "entregas.json"
MATRICULAS_FILE = DATABASE_DIR / "matriculas.json"
USERS_FILE = DATABASE_DIR / "users.json"
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
    
    elif user_data.get('role') == 'USER':
        turmas = get_turmas_aluno(email)
        detalhes['total_turmas'] = len(turmas)
        entregas = get_atividades_entregues_aluno(email)
        detalhes['atividades_entregues'] = len(entregas)
        boletim = get_boletim_aluno(email)
        medias = [t['media'] for t in boletim if t.get('media') and t['media'] > 0]
        detalhes['media_geral'] = sum(medias) / len(medias) if medias else 0
    
    return detalhes

def editar_usuario(email, nome, idade, role):
    dados = carregar_json(USERS_FILE)
    if email in dados.get('users', {}):
        dados['users'][email]['nome'] = nome
        dados['users'][email]['idade'] = idade
        dados['users'][email]['role'] = role
        salvar_json(USERS_FILE, dados)
        return True
    return False

def excluir_usuario(email):
    dados = carregar_json(USERS_FILE)
    if email in dados.get('users', {}):
        del dados['users'][email]
        salvar_json(USERS_FILE, dados)
        return True
    return False

def adicionar_usuario(nome, email, idade, senha, role):
    dados = carregar_json(USERS_FILE)
    if 'users' not in dados:
        dados['users'] = {}
    
    if email in dados['users']:
        return False
    
    from infra.security import criptografar_senha
    dados['users'][email] = {
        'nome': nome,
        'idade': idade,
        'senha': criptografar_senha(senha),
        'role': role
    }
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

def get_alunos_disponiveis(turma_id):
    todos_usuarios = get_todos_usuarios('USER')
    alunos_turma = get_alunos_turma(turma_id)
    emails_turma = [a['email'] for a in alunos_turma]
    
    disponiveis = [u for u in todos_usuarios if u['email'] not in emails_turma]
    return disponiveis

def adicionar_aluno_turma(turma_id, aluno_email):
    matriculas_data = carregar_json(MATRICULAS_FILE)
    if 'matriculas' not in matriculas_data:
        matriculas_data['matriculas'] = {}
    
    matricula_id = f"{turma_id}_{aluno_email}"
    
    if matricula_id in matriculas_data['matriculas']:
        return False
    
    matriculas_data['matriculas'][matricula_id] = {
        'turma_id': str(turma_id),
        'aluno_email': aluno_email,
        'data_matricula': datetime.now().strftime("%d/%m/%Y")
    }
    
    salvar_json(MATRICULAS_FILE, matriculas_data)
    return True

def excluir_turma(turma_id):
    dados = carregar_json(TURMAS_FILE)
    if str(turma_id) in dados.get('turmas', {}):
        del dados['turmas'][str(turma_id)]
        salvar_json(TURMAS_FILE, dados)
        return True
    return False

def registrar_aula(turma_id, data, titulo, conteudo):
    dados = carregar_json(AULAS_FILE)
    
    if 'aulas' not in dados:
        dados['aulas'] = {}
    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1
    
    aula_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1
    
    dados['aulas'][aula_id] = {
        'id': aula_id,
        'turma_id': str(turma_id),
        'data': data,
        'titulo': titulo,
        'conteudo': conteudo
    }
    
    salvar_json(AULAS_FILE, dados)
    return True

def get_aulas_turma(turma_id):
    dados = carregar_json(AULAS_FILE)
    aulas_turma = []
    
    for aula in dados.get('aulas', {}).values():
        if aula.get('turma_id') == str(turma_id):
            aulas_turma.append(aula)
    
    return sorted(aulas_turma, key=lambda x: x.get('data', ''), reverse=True)

def get_todas_aulas_professor(professor_email):
    turmas = get_turmas_professor(professor_email)
    turma_ids = [t['id'] for t in turmas]
    
    dados = carregar_json(AULAS_FILE)
    dados_turmas = carregar_json(TURMAS_FILE)
    
    todas_aulas = []
    for aula in dados.get('aulas', {}).values():
        if aula.get('turma_id') in turma_ids:
            aula_copy = aula.copy()
            turma = dados_turmas.get('turmas', {}).get(aula.get('turma_id'), {})
            aula_copy['turma'] = turma.get('nome', 'Turma Desconhecida')
            todas_aulas.append(aula_copy)
    
    return sorted(todas_aulas, key=lambda x: x.get('data', ''), reverse=True)

def get_historico_aulas_aluno(aluno_email):
    turmas = get_turmas_aluno(aluno_email)
    turma_ids = [t['id'] for t in turmas]
    
    dados = carregar_json(AULAS_FILE)
    dados_turmas = carregar_json(TURMAS_FILE)
    
    historico = []
    for aula in dados.get('aulas', {}).values():
        if aula.get('turma_id') in turma_ids:
            aula_copy = aula.copy()
            turma = dados_turmas.get('turmas', {}).get(aula.get('turma_id'), {})
            aula_copy['turma'] = turma.get('nome', 'Turma Desconhecida')
            historico.append(aula_copy)
    
    return sorted(historico, key=lambda x: x.get('data', ''), reverse=True)

def criar_atividade(turma_id, titulo, descricao, prazo, valor, arquivo_path):
    dados = carregar_json(ATIVIDADES_FILE)
    
    if 'atividades' not in dados:
        dados['atividades'] = {}
    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1
    
    atividade_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1
    
    arquivo_salvo = None
    if arquivo_path:
        ext = Path(arquivo_path).suffix
        arquivo_nome = f"atividade_{atividade_id}{ext}"
        destino = ARQUIVOS_DIR / arquivo_nome
        shutil.copy2(arquivo_path, destino)
        arquivo_salvo = arquivo_nome
    
    dados['atividades'][atividade_id] = {
        'id': atividade_id,
        'turma_id': str(turma_id),
        'titulo': titulo,
        'descricao': descricao,
        'prazo': prazo,
        'valor': float(valor),
        'arquivo': arquivo_salvo,
        'data_criacao': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    salvar_json(ATIVIDADES_FILE, dados)
    return True

def get_atividades_turma(turma_id):
    dados = carregar_json(ATIVIDADES_FILE)
    atividades_turma = []
    
    for atividade in dados.get('atividades', {}).values():
        if atividade.get('turma_id') == str(turma_id):
            atividades_turma.append(atividade)
    
    return atividades_turma

def get_atividades_turma_aluno(turma_id, aluno_email):
    atividades = get_atividades_turma(turma_id)
    entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})
    
    resultado = []
    for atividade in atividades:
        ativ_copy = atividade.copy()
        
        entrega = next((e for e in entregas.values() if 
                       e.get('atividade_id') == atividade['id'] and 
                       e.get('aluno_email') == aluno_email), None)
        
        ativ_copy['entregue'] = entrega is not None
        ativ_copy['nota'] = entrega.get('nota') if entrega else None
        ativ_copy['data_entrega'] = entrega.get('data_entrega') if entrega else None
        
        resultado.append(ativ_copy)
    
    return resultado

def get_todas_atividades_professor(professor_email):
    turmas = get_turmas_professor(professor_email)
    turma_ids = [t['id'] for t in turmas]
    
    dados = carregar_json(ATIVIDADES_FILE)
    dados_turmas = carregar_json(TURMAS_FILE)
    
    todas_atividades = []
    for atividade in dados.get('atividades', {}).values():
        if atividade.get('turma_id') in turma_ids:
            ativ_copy = atividade.copy()
            turma = dados_turmas.get('turmas', {}).get(atividade.get('turma_id'), {})
            ativ_copy['turma'] = turma.get('nome', 'Turma Desconhecida')
            todas_atividades.append(ativ_copy)
    
    return todas_atividades

def get_atividades_pendentes_aluno(aluno_email):
    turmas = get_turmas_aluno(aluno_email)
    entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})
    dados_turmas = carregar_json(TURMAS_FILE)
    
    pendentes = []
    for turma in turmas:
        atividades = get_atividades_turma(turma['id'])
        for atividade in atividades:
            entrega = next((e for e in entregas.values() if 
                           e.get('atividade_id') == atividade['id'] and 
                           e.get('aluno_email') == aluno_email), None)
            
            if not entrega:
                ativ_copy = atividade.copy()
                ativ_copy['turma'] = turma['nome']
                ativ_copy['turma_id'] = turma['id']
                pendentes.append(ativ_copy)
    
    return pendentes

def get_atividades_entregues_aluno(aluno_email):
    entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})
    atividades_data = carregar_json(ATIVIDADES_FILE).get('atividades', {})
    turmas_data = carregar_json(TURMAS_FILE).get('turmas', {})
    
    entregues = []
    for entrega in entregas.values():
        if entrega.get('aluno_email') == aluno_email:
            atividade = atividades_data.get(entrega.get('atividade_id'), {})
            if atividade:
                ativ_copy = atividade.copy()
                ativ_copy['data_entrega'] = entrega.get('data_entrega')
                ativ_copy['nota'] = entrega.get('nota')
                
                turma = turmas_data.get(atividade.get('turma_id'), {})
                ativ_copy['turma'] = turma.get('nome', 'Turma Desconhecida')
                entregues.append(ativ_copy)
    
    return entregues

def entregar_atividade(atividade_id, aluno_email, arquivo_path, comentario):
    dados = carregar_json(ENTREGAS_FILE)
    
    if 'entregas' not in dados:
        dados['entregas'] = {}
    if 'proximo_id' not in dados:
        dados['proximo_id'] = 1
    
    entrega_id = str(dados['proximo_id'])
    dados['proximo_id'] += 1
    
    arquivo_salvo = None
    if arquivo_path:
        ext = Path(arquivo_path).suffix
        arquivo_nome = f"entrega_{entrega_id}_{aluno_email.split('@')[0]}{ext}"
        destino = ARQUIVOS_DIR / arquivo_nome
        shutil.copy2(arquivo_path, destino)
        arquivo_salvo = arquivo_nome
    
    aluno_data = get_user_data(aluno_email)
    
    dados['entregas'][entrega_id] = {
        'id': entrega_id,
        'atividade_id': str(atividade_id),
        'aluno_email': aluno_email,
        'aluno_nome': aluno_data.get('nome', ''),
        'arquivo': arquivo_salvo,
        'comentario': comentario,
        'data_entrega': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'nota': None,
        'feedback': None
    }
    
    salvar_json(ENTREGAS_FILE, dados)
    return True

def get_entregas_atividade(atividade_id):
    dados = carregar_json(ENTREGAS_FILE)
    entregas = []
    
    for entrega in dados.get('entregas', {}).values():
        if entrega.get('atividade_id') == str(atividade_id):
            entregas.append(entrega)
    
    return entregas

def get_detalhes_entrega(atividade_id, aluno_email):
    dados = carregar_json(ENTREGAS_FILE)
    
    for entrega in dados.get('entregas', {}).values():
        if (entrega.get('atividade_id') == str(atividade_id) and 
            entrega.get('aluno_email') == aluno_email):
            return entrega
    
    return None

def avaliar_entrega(entrega_id, nota, feedback):
    dados = carregar_json(ENTREGAS_FILE)
    
    if str(entrega_id) in dados.get('entregas', {}):
        dados['entregas'][str(entrega_id)]['nota'] = float(nota)
        dados['entregas'][str(entrega_id)]['feedback'] = feedback
        salvar_json(ENTREGAS_FILE, dados)
        return True
    return False

def baixar_arquivo_entrega(entrega_id, save_path):
    dados = carregar_json(ENTREGAS_FILE)
    entrega = dados.get('entregas', {}).get(str(entrega_id), {})
    
    if entrega and entrega.get('arquivo'):
        arquivo_origem = ARQUIVOS_DIR / entrega['arquivo']
        if arquivo_origem.exists():
            shutil.copy2(arquivo_origem, save_path)
            return True
    return False

def get_notas_aluno_turma(aluno_email, turma_id):
    atividades = get_atividades_turma(turma_id)
    entregas = carregar_json(ENTREGAS_FILE).get('entregas', {})
    
    notas = []
    for atividade in atividades:
        entrega = next((e for e in entregas.values() if 
                       e.get('atividade_id') == atividade['id'] and 
                       e.get('aluno_email') == aluno_email and
                       e.get('nota') is not None), None)
        
        if entrega:
            notas.append({
                'atividade': atividade['titulo'],
                'nota': entrega['nota'],
                'valor': atividade['valor'],
                'data': entrega.get('data_entrega', ''),
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
            total_pontos = sum([n['nota'] for n in notas])
            total_valor = sum([n['valor'] for n in notas])
            media = (total_pontos / total_valor * 10) if total_valor > 0 else 0
        
        boletim.append({
            'turma': turma['nome'],
            'disciplina': turma['disciplina'],
            'professor': turma['professor_nome'],
            'notas': notas,
            'media': media,
            'frequencia': 100
        })
    
    return boletim

def get_boletim_turma(turma_id):
    alunos = get_alunos_turma(turma_id)
    
    boletim = []
    for aluno in alunos:
        notas = get_notas_aluno_turma(aluno['email'], turma_id)
        
        media = 0
        if notas:
            total_pontos = sum([n['nota'] for n in notas])
            total_valor = sum([n['valor'] for n in notas])
            media = (total_pontos / total_valor * 10) if total_valor > 0 else 0
        
        boletim.append({
            'nome': aluno['nome'],
            'email': aluno['email'],
            'media': media,
            'frequencia': 100
        })
    
    return boletim

def get_relatorio_geral():
    usuarios = get_todos_usuarios()
    turmas = get_todas_turmas()
    atividades_data = carregar_json(ATIVIDADES_FILE).get('atividades', {})
    entregas_data = carregar_json(ENTREGAS_FILE).get('entregas', {})
    matriculas = carregar_json(MATRICULAS_FILE).get('matriculas', {})
    
    total_usuarios = len(usuarios)
    total_admins = len([u for u in usuarios if u.get('role') == 'ADMIN'])
    total_professores = len([u for u in usuarios if u.get('role') == 'INSTRUCTOR'])
    total_alunos = len([u for u in usuarios if u.get('role') == 'USER'])
    
    total_turmas = len(turmas)
    total_matriculas = len(matriculas)
    media_alunos_turma = total_matriculas / total_turmas if total_turmas > 0 else 0
    
    total_atividades = len(atividades_data)
    total_entregas = len(entregas_data)
    taxa_entrega = (total_entregas / (total_atividades * total_alunos) * 100) if (total_atividades * total_alunos) > 0 else 0
    total_corrigidas = len([e for e in entregas_data.values() if e.get('nota') is not None])
    
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
    taxa_aprovacao = (aprovados / len(medias) * 100) if medias else 0
    
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
        'taxa_aprovacao': taxa_aprovacao
    }

def get_estatisticas_detalhadas():
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
        professores_ativos.append({
            'nome': prof['nome'],
            'email': prof['email'],
            'turmas': len(turmas),
            'atividades': len(atividades)
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

def limpar_turmas_antigas():
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
    from datetime import datetime, timedelta
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
    return 0
