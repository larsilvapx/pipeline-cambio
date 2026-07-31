# src/pipeline.py: o pipeline de cambio completo
import logging, sys
from pathlib import Path
from venv import logger
sys.path.append(str(Path(__file__).resolve().parent.parent))
import pandas as pd
from sqlalchemy import create_engine
from coleta import coletar_cotacoes, salvar_raw      # Aula 4: o E
from transforma import (listar_raws, carregar_raw,
                        transformar, validar)         # Aula 5: o T
from config import POSTGRES_URL
NOME_TABELA = "cotacoes"    


def extract() -> None:
    """E: coleta a cotacao atual e acrescenta um raw."""
    caminho = salvar_raw(coletar_cotacoes())
    logger.info("raw salvo em %s", caminho)
def transform() -> pd.DataFrame:
    """T: reconstroi a foto inteira a partir de TODOS os raws."""
    arquivos = listar_raws()
    logger.info("%d arquivos raw encontrados", len(arquivos))
    tabelas = [transformar(carregar_raw(c), origem=c.name)
               for c in arquivos]
    df = pd.concat(tabelas, ignore_index=True)
    validar(df)
    return df


def load(df: pd.DataFrame) -> None:
    """L: grava a foto inteira. replace = reexecutavel sem medo."""
    engine = create_engine(POSTGRES_URL)
    df.to_sql(NOME_TABELA, engine, if_exists="replace", index=False)
    total = pd.read_sql(
        f"SELECT COUNT(*) AS n FROM {NOME_TABELA}", engine)["n"][0]
    logger.info("carga concluida: %d linhas", total)
def main() -> None:
    logger.info("pipeline iniciado")
    extract()
    df = transform()
    load(df)
    logger.info("pipeline concluido com sucesso")
if __name__ == "__main__":
    main()