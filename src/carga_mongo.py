import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from sqlalchemy import create_engine, text
from config import POSTGRES_URL
from pymongo import MongoClient
from config import MONGO_URL
import pandas as pd
import logging,sys
from venv import logger

def resumir(df: pd.DataFrame) -> list[dict]:
    """Deriva um documento-resumo por moeda."""
    documentos = []
    for moeda, grupo in df.groupby("moeda"):
        recente = grupo.sort_values("data_cotacao").iloc[-1]
        documentos.append({
            "moeda": moeda,
            "ultima_cotacao": float(recente["valor_compra"]),
            "data_ultima": recente["data_cotacao"].isoformat(),
            "media_compra": float(grupo["valor_compra"].mean()),
            "maxima_periodo": float(grupo["maxima_dia"].max()),
            "minima_periodo": float(grupo["minima_dia"].min()),
            "total_coletas": int(len(grupo)),
        })
    return documentos


def main() -> None:
    engine = create_engine(POSTGRES_URL)
    df = pd.read_sql("SELECT * FROM cotacoes", engine)
    logger.info("%d linhas lidas do PostgreSQL", len(df))
    documentos = resumir(df)
    cliente = MongoClient(MONGO_URL)
    colecao = cliente["pipeline_cambio"]["resumo_cotacoes"]
    colecao.delete_many({})   # o "replace" do mundo Mongo
    colecao.insert_many(documentos)
    logger.info("resumo gravado: %d documentos", len(documentos))
    cliente.close()