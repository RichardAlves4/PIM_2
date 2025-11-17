import os
import subprocess 
import json
from pathlib import Path

def cadastro_com_c(role, nome, email, senha):
    BASE_DIR = Path(__file__).parent.parent
    C_DIR = BASE_DIR / "C"
    C_EXE = C_DIR / "cadastro.exe"
    TEMP_FILE = C_DIR / "temp_cadastro.json"

    if not C_EXE.exists():
        return False, f"Executável C não encontrado em: {C_EXE}\n\nCompile o arquivo C:\ncd C\ngcc cadastro.c -o cadastro.exe"
    
    try:
        result = subprocess.run([str(C_EXE), role, nome, email, senha], capture_output=True, text=True, cwd=str(C_DIR), encoding='utf-8')
        
        if result.returncode != 0:
            erro = result.stderr.strip()

            if "ERRO_VALIDACAO:" in erro:
                mensagem = erro.split("ERRO_VALIDACAO:")[1].strip()
                return False, mensagem
            return False, f"Erro na validação: {erro}"
        
        if not TEMP_FILE.exists():
            return False, "C não gerou o arquivo temporário!"
        with open(TEMP_FILE, "r", encoding="utf-8") as f:
            dados_validados = json.load(f)
        TEMP_FILE.unlink()
        return True, dados_validados
    
    except Exception as e:
        return False, f"Erro ao executar C: {str(e)}"