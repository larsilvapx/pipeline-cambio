# src/mongo_conexao.py: o primeiro documento na nuvem
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from pymongo import MongoClient
from config import MONGO_URL
cliente = MongoClient(MONGO_URL)   # o create_engine do Mongo
banco = cliente["pipeline_cambio"]  # nasce na 1a insercao
colecao = banco["teste"]            # idem: sem CREATE TABLE
resultado = colecao.insert_one({
    "quem": "Luciano", "aula": 7,
    "mensagem": "primeiro documento na nuvem"})
print(f"documento inserido com _id = {resultado.inserted_id}")
cliente.close()