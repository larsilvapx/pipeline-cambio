import json
from pathlib import Path
arquivos = sorted(Path("data/raw").glob("cotacoes_*.json"))
print(arquivos)              # alfabetica = cronologica!
with open(arquivos[-1], encoding="utf-8") as f:  # o mais recente
    dados = json.load(f)
print(type(dados))           # <class 'dict'>  (nao e lista!)
print(dados.keys())          # dict_keys(['USDBRL', 'EURBRL'])
print(dados["USDBRL"]["bid"])  # '5.43...'  string!