import requests

def Endereco(cep):
    url = "https://viacep.com.br/ws/" + cep + "/json/"
    response = requests.get(url=url)

    if response.status_code == 400:
        return False
    
    dados = response.json()
    return dados


def ConsultarCEP(self, event, cep):
    dados = Endereco(cep)
    if dados == False:
        return
    self.ui.SetCampo("logradouro", dados['logradouro'])
    self.ui.SetCampo('bairro', dados['bairro'])
    self.ui.SetCampo('cidade', dados['localidade'])
    self.ui.SetCampo('uf', dados['uf'])
    return True