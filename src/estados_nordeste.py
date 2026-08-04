
from pymongo import MongoClient
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import MONGO_URL


cliente = MongoClient(MONGO_URL)
colecao = cliente["pipeline_cambio"]["estados"]

resultado = colecao.find(
    {"regiao.nome": "Nordeste"},
    {"_id": 0, "nome": 1, "sigla": 1}
)
for estado in resultado:
    print(estado)
    
cliente.close()    