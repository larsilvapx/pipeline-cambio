import requests

URL = "https://servicodados.ibge.gov.br/api/v3/noticias/"
corpo = requests.get(URL, params={"qtd": 10, "page": 1},
                     timeout=10).json()
print(corpo.keys())
# dict_keys(['count', 'page', 'totalPages', 'items', ...])