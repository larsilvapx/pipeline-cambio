import time
import requests

URL = "https://servicodados.ibge.gov.br/api/v3/noticias/"

def coletar_noticias(por_pagina: int = 10) -> list[dict]:
    """Percorre páginas da API de notícias até acabar os itens."""
    todas = []
    page = 1
    while True:
        params = {"qtd": por_pagina, "page": page}
        resposta = requests.get(URL, params=params, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()

        # Verifica se existe a chave 'items' ou 'itens'
        itens = dados.get("items") or dados.get("itens", [])
        if not itens:
            print(f"pagina {page}: sem itens, fim da coleta")
            break

        todas.extend(itens)
        print(f"pagina {page}: +{len(itens)} (total {len(todas)})")
        page += 1
        time.sleep(1)  # respeita o servidor

    return todas

# chamada da função
noticias = coletar_noticias(por_pagina=10)
print(f"Total de noticias coletadas: {len(noticias)}")
