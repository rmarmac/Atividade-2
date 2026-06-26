import requests

def Endereco(cep):
    url = "https://viacep.com.br/ws/" + cep + "/json/"
    response = requests.get(url=url)

    if response.status_code == 400:
        return False
    
    dados = response.json()
    return dados