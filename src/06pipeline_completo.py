import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from sqlalchemy import create_engine

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

URL_API = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

# Substitua 'SUA_SENHA' pela senha real do seu PostgreSQL local
STRING_CONEXAO = "postgresql+psycopg2://postgres:root@localhost:5432/pipeline_dados"

NOME_TABELA = "estados"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def extract():
    """Coleta os dados da API e devolve o JSON já convertido em Python.

    Responsabilidades: coletar com segurança e preservar o dado bruto.
    """
    logger.info("Extração iniciada: %s", URL_API)

    # TODO 1: Recomposição segura com timeout e raise_for_status
    resposta = requests.get(URL_API, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()

    # TODO 2: Salvar cópia bruta em raw/
    os.makedirs("raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    caminho_raw = f"raw/{timestamp}_estados.json"

    with open(caminho_raw, "w", encoding="utf-8") as file:
        json.dump(dados, file, ensure_ascii=False, indent=4)

    logger.info("Dado bruto salvo em: %s", caminho_raw)
    logger.info("Extração concluída.")
    return dados


def transform(dados):
    """Transforma o JSON cru em um DataFrame limpo e validado."""
    logger.info("Transformação iniciada.")

    # TODO 3: Achatamento da estrutura JSON aninhada
    df = pd.json_normalize(dados, sep="_")

    # TODO 4: Renomear colunas para um padrão claro e limpo
    colunas_mapa = {
        "id": "id_estado",
        "sigla": "sigla_uf",
        "nome": "nome_estado",
        "regiao_id": "id_regiao",
        "regiao_sigla": "sigla_regiao",
        "regiao_nome": "nome_regiao",
    }
    df = df.rename(columns=colunas_mapa)

    # TODO 5: Validações de Qualidade de Dados (Data Quality)
    # Validação 1: O Brasil deve ter exatamente 27 Unidades Federativas
    total_linhas = len(df)
    assert total_linhas == 27, f"Erro de Qualidade: Esperado 27 estados, obtido {total_linhas}"

    # Validação 2: Nenhuma chave primária pode ser nula
    nulos_id = df["id_estado"].isnull().sum()
    assert nulos_id == 0, f"Erro de Qualidade: Encontrados {nulos_id} valores nulos no ID do estado"

    logger.info("Validações concluídas: %d estados validados com sucesso.", total_linhas)
    logger.info("Transformação concluída.")
    return df


def load(df):
    """Carrega o DataFrame no PostgreSQL de forma idempotente."""
    logger.info("Carga iniciada na tabela '%s'.", NOME_TABELA)

    # TODO 6: Conexão e gravação idempotente (if_exists="replace")
    engine = create_engine(STRING_CONEXAO)
    df.to_sql(name=NOME_TABELA, con=engine, if_exists="replace", index=False)

    # TODO 7 (bônus): Leitura de confirmação direto do banco
    df_verificacao = pd.read_sql(f"SELECT COUNT(*) AS total FROM {NOME_TABELA}", con=engine)
    total_banco = df_verificacao["total"].iloc[0]

    logger.info("Carga concluída. Linhas confirmadas na tabela '%s': %d", NOME_TABELA, total_banco)


def main():
    """Rege a orquestra: extract -> transform -> load, nessa ordem."""
    logger.info("Pipeline iniciado.")
    dados = extract()
    df = transform(dados)
    load(df)
    logger.info("Pipeline concluído com sucesso.")


if __name__ == "__main__":
    main()
    

