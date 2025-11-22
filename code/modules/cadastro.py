import os
import subprocess 
import json
from pathlib import Path

def cadastro_com_c(role, nome, email, senha):
    # Determinação dos caminhos baseados na localização do script atual.
    # __file__.parent pega o diretório onde este script está.
    # .parent sobe um nível (assumindo que o script está em um subdiretório).
    BASE_DIR = Path(__file__).parent.parent
    # Assume que o executável C está em um subdiretório chamado 'C'.
    C_DIR = BASE_DIR / "C"
    # O caminho completo para o executável compilado.
    C_EXE = C_DIR / "cadastro.exe"
    # O caminho completo para o arquivo temporário que o C irá gerar
    TEMP_FILE = C_DIR / "temp_cadastro.json"

    # 1. Checagem da Existência do Executável C
    if not C_EXE.exists():
        # Se o executável não for encontrado, retorna False e uma mensagem de erro
        return False, f"Executável C não encontrado em: {C_EXE}\n\nCompile o arquivo C:\ncd C\ngcc cadastro.c -o cadastro.exe"
    
    try:
        # 2. Execução do Programa C
        result = subprocess.run([str(C_EXE), role, nome, email, senha], capture_output=True, text=True, cwd=str(C_DIR), encoding='utf-8')
        
        # 3. Tratamento de Erro do Executável C
        if result.returncode != 0:
            # returncode diferente de zero indica erro no programa C.
            erro = result.stderr.strip() # Pega a mensagem de erro que foi impressa no stderr pelo C.

            if "ERRO_VALIDACAO:" in erro:
                # Se for um erro de validação (código 2, 3 ou 4 do C), extrai a mensagem específica e a retorna para o usuário Python.
                mensagem = erro.split("ERRO_VALIDACAO:")[1].strip()
                return False, mensagem
            # Se for outro tipo de erro (ex: erro de argumento, erro de arquivo), retorna o erro completo.
            return False, f"Erro na validação: {erro}"
        
        # 4. Leitura e Limpeza do Arquivo JSON (Sucesso)
        if not TEMP_FILE.exists():
            # Caso o C tenha retornado sucesso (código 0), mas o arquivo não foi gerado.
            return False, "C não gerou o arquivo temporário!"
        # Abre e lê o arquivo JSON gerado pelo C.
        with open(TEMP_FILE, "r", encoding="utf-8") as f:
            # json.load() desserializa a string JSON em um dicionário Python.
            dados_validados = json.load(f)
        # Limpa o arquivo temporário para não deixar lixo no sistema de arquivos.
        TEMP_FILE.unlink()
        # 5. Retorno de Sucesso
        # Retorna True e os dados carregados do JSON.
        return True, dados_validados
    
    except Exception as e:
        # 6. Tratamento de Erro de Execução (Python)
        # Captura exceções que ocorrem durante a chamada do subprocesso.
        return False, f"Erro ao executar C: {str(e)}"