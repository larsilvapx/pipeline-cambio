import requests


url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/PE/municipios"

resposta = requests.get(url, timeout=10)

resposta.raise_for_status()

municipios = resposta.json()
print(f"Quantidade de municipios: {len(municipios)}")

print("\nPrimeiros 10 municipios de Pernambuco\n")

for municipio in municipios[:10]:
    print(municipio["nome"])