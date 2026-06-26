import datetime

def VerificarCPF(cpf : str):
    try:
        int(cpf)
    except:
        return False
    if len(cpf) != 11:
        return False
    verificacao = cpf[0:9]
    soma = 0
    for i in range(10,1,-1):
        soma += int(verificacao[10 - i]) * i
    digito1 = 0
    if soma % 11 >= 2:
        digito1 = 11 - (soma % 11)
    verificacao = verificacao + str(digito1)
    soma = 0
    for i in range(11,1,-1):
        soma += int(verificacao[11 - i]) * i
    digito2 = 0
    if soma % 11 >= 2:
        digito2 = 11 - (soma % 11)
    verificacao = verificacao + str(digito2)

    return cpf == verificacao

def VerificarCNPJ(cnpj : str):
    try:
        int(cnpj)
    except:
        return False
    if len(cnpj) != 14:
        return False
    verificacao = cnpj[0:12]
    coeficientes = [5,4,3,2,9,8,7,6,5,4,3,2]
    soma = 0
    for i,coef in enumerate(coeficientes):
        soma += coef*int(verificacao[i])
    digito1 = 0
    if soma % 11 >= 2:
        digito1 = 11 - (soma % 11)
    verificacao = verificacao + str(digito1)

    coeficientes.insert(0, 6)
    soma = 0
    for i,coef in enumerate(coeficientes):
        soma += coef*int(verificacao[i])
    digito2 = 0
    if soma % 11 >= 2:
        digito2 = 11 - (soma % 11)
    verificacao = verificacao + str(digito2)

    return cnpj == verificacao


def ExecutarVerificacoesCPF_CNPJ(cpf_ou_cnpj: str):
    return (VerificarCPF(cpf_ou_cnpj) or VerificarCNPJ(cpf_ou_cnpj))

def ExecutarVerificacaoDataNasc(data : str):
    data = [s for s in data if s.isdigit()]
    
    if len(data) != 8:
        return False
    year = "".join(data[4:8])
    month = "".join(data[2:4])
    day = "".join(data[0:2])
    try:
        data_nscmnt = datetime.datetime(int(year), int(month), int(day))
        if data_nscmnt > datetime.datetime.now():
            return False
        return data_nscmnt
    except:
        return False

def ExecutarVerificacaoNumero(numero : str):
    try:
        int(numero)
    except:
        return False
    if len(numero) != 11:
        return False
    return True

def ExecutarVerificacaoCEP(cep : str):
    try:
        int(cep)
    except:
        return False
    if len(cep) != 8:
        return False
    return True