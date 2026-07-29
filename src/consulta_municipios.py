import requests

def consultar_municipios(sigla):
    
    
    url = (
        f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{sigla}/municipios"
    )
    
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        municipios = resposta.json()
        
        print(f"Quantidade de municípios: {len(municipios)}")
        print("-"*45)
        
        for municipio in municipios[:10]:
            print(f"Municipios: {municipio['nome']}")
            
    except requests.exceptions.HTTPError:
        print("Estado não encontrado")
        
    except requests.exceptions.RequestException as erro:
        print(f"Erro de conexão: {erro}")            
            
def main():        
        sigla = input("Digite a sigla do estado: ").upper()
        print("-"*45)
        print(f"\nOs 10 primeiros municipios de {sigla}\n")
        print("-"*45)
        consultar_municipios(sigla)
main()
    
    
        


      

