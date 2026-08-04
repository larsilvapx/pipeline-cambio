"""
Exercicio 07 - Primeiros passos com MongoDB (Aula 7)

O que este script faz:
    Conecta ao seu cluster do MongoDB Atlas, insere documentos de
    exemplo com insert_many e consulta com find - com e sem filtro.

Antes de rodar:
    1. Cluster M0 criado no Atlas, usuario de banco e IP liberado
       (a tarefa critica da aula 6).
    2. Preencha a STRING_CONEXAO abaixo com a SUA connection string
       (no Atlas: Connect -> Drivers -> copie a URI).

Como rodar (com o venv ativo):
    python 07_mongodb_primeiros_passos.py
"""

from pymongo import MongoClient
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from pymongo import MongoClient
from config import MONGO_URL


cliente = MongoClient(MONGO_URL)   # o create_engine do Mongo

# ---------------------------------------------------------------------------
# A connection string - PREENCHA com a sua
# ---------------------------------------------------------------------------
# Formato tipico do Atlas (troque usuario, senha e o endereco do cluster):
#   mongodb+srv://usuario:senha@cluster0.xxxxx.mongodb.net/
#
# ATENCAO: essa string carrega usuario e senha - a regra do modulo vale
# aqui tambem: credencial real NUNCA vai para o GitHub.
STRING_CONEXAO = MONGO_URL


def primeiros_passos():
    # ------------------------------------------------------------------
    # Conexao: cliente -> banco -> colecao
    # ------------------------------------------------------------------
    # MongoClient e a ponte com o cluster (o create_engine do Mongo).
    cliente = MongoClient(STRING_CONEXAO)

    # Banco e colecao sao criados AUTOMATICAMENTE na primeira insercao -
    # nao existe CREATE TABLE no mundo dos documentos.
    banco = cliente["aula07"]
    colecao = banco["alunos"]

    # ------------------------------------------------------------------
    # insert_many: varios documentos de uma vez
    # ------------------------------------------------------------------
    # Cada documento e um dicionario de Python. Repare que o terceiro
    # tem um campo a mais ("bolsista") - no MongoDB isso e permitido:
    # sem esquema fixo, quem garante a consistencia e o SEU codigo.
    documentos = [
        {"nome": "Ana", "cidade": "Recife", "modulos_concluidos": 2},
        {"nome": "Bruno", "cidade": "Olinda", "modulos_concluidos": 3},
        {"nome": "Carla", "cidade": "Recife", "modulos_concluidos": 1, "bolsista": True},
        {"nome": "Diego", "cidade": "Caruaru", "modulos_concluidos": 3},
    ]

    resultado = colecao.insert_many(documentos)
    print(f"{len(resultado.inserted_ids)} documentos inseridos.")
    print("(abra o Browse Collections no Atlas e va conferir!)\n")

    # ------------------------------------------------------------------
    # find sem filtro: todos os documentos da colecao
    # ------------------------------------------------------------------
    # Equivale a um SELECT * FROM alunos. Repare no _id: o MongoDB
    # criou um identificador unico para cada documento, sozinho.
    print("--- Todos os documentos ---")
    for doc in colecao.find():
        print(doc)

    # ------------------------------------------------------------------
    # find com filtro: so quem casa com o criterio
    # ------------------------------------------------------------------
    # O filtro tambem e um dicionario: {"cidade": "Recife"} equivale a
    # WHERE cidade = 'Recife'.
    print("\n--- So quem e de Recife ---")
    for doc in colecao.find({"cidade": "Recife"}):
        print(f'{doc["nome"]} - {doc["cidade"]}')

    # Operadores comecam com $: aqui, $gte significa "maior ou igual"
    # (greater than or equal) - WHERE modulos_concluidos >= 2.
    print("\n--- Quem ja concluiu 2 modulos ou mais ---")
    for doc in colecao.find({"modulos_concluidos": {"$gte": 2}}):
        print(f'{doc["nome"]} - {doc["modulos_concluidos"]} modulos')

    # Boa educacao com conexoes: fechar ao terminar.
    cliente.close()


if __name__ == "__main__":
    primeiros_passos()

# Experimento (ligando com a aula 6): rode o script DUAS vezes e conte
# os documentos. Duplicou? Pois e - insert_many puro nao e idempotente.
# Para limpar a colecao e recomecar, rode uma vez num shell de Python:
#     colecao.delete_many({})