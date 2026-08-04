import requests
from pymongo import MongoClient
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import MONGO_URL

URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

resposta = requests.get(URL, timeout=10)
resposta.raise_for_status()

estados = resposta.json()

cliente = MongoClient(MONGO_URL)

db = cliente["pipeline_cambio"]
colecao = db["estados"]

# Limpa coleção antes de inserir
colecao.delete_many({})
colecao.insert_many(estados)
print("estados inseridos com sucesso!")

print(type(estados))
print(len(estados))
print(estados[0])

cliente.close()



    



