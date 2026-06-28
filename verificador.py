import datetime
from tkinter import messagebox

def VerificarCPF(cpf : str):
    cpf = [s for s in cpf if s.isdigit()]
    if len(cpf) != 11:
        return False
    verificacao = cpf[0:9]
    soma = 0
    for i in range(10,1,-1):
        soma += int(verificacao[10 - i]) * i
    digito1 = 0
    if soma % 11 >= 2:
        digito1 = 11 - (soma % 11)
    verificacao = verificacao + [str(digito1)]
    soma = 0
    for i in range(11,1,-1):
        soma += int(verificacao[11 - i]) * i
    digito2 = 0
    if soma % 11 >= 2:
        digito2 = 11 - (soma % 11)
    verificacao = verificacao + [str(digito2)]

    return cpf == verificacao

def VerificarCNPJ(cnpj : str):
    cnpj = [s for s in cnpj if s.isdigit()]
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
    verificacao = verificacao + [str(digito1)]

    coeficientes.insert(0, 6)
    soma = 0
    for i,coef in enumerate(coeficientes):
        soma += coef*int(verificacao[i])
    digito2 = 0
    if soma % 11 >= 2:
        digito2 = 11 - (soma % 11)
    verificacao = verificacao + [str(digito2)]

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



def VerificacaoCadastro(ctk_master):
    if ctk_master.ui.GetCampo("id") == "":
        messagebox.showerror("Sem ID", "Insira um ID")
        return False
    if ctk_master.ui.GetCampo("nome") == "":
        messagebox.showerror("Sem nome", "Insira seu nome")
        return False
    if not ExecutarVerificacoesCPF_CNPJ(ctk_master.ui.GetCampo("cpf_cnpj")):
        messagebox.showerror("CPF ou CNPJ inválido", "Verifique o CPF ou CNPJ.")
        return False
    data = ExecutarVerificacaoDataNasc(ctk_master.ui.GetCampo("data"))
    if not data:
        messagebox.showerror("Data inválida", "Insira uma data válida")
        return False
    else:
        ctk_master.ui.SetCampo("data", f"{data.day:02}" + "/" + f"{data.month:02}" + "/" + f"{data.year:04}")
    data = "datetime('" + str(data) + "')"
    if not ExecutarVerificacaoCEP(ctk_master.ui.GetCampo("cep")):
        messagebox.showerror("Erro no CEP", "CEP inválido.")
        return False
    if not ExecutarVerificacaoNumero(ctk_master.ui.GetCampo("contato")):
        messagebox.showerror("Número de celular inválido", "Confira o número de celular (lembre-se do DDD)")
        return False
    numero_logradouro= ctk_master.ui.GetCampo("numero")
    if numero_logradouro != "":
        try:
            numero_logradouro = int(numero_logradouro)
        except:
            messagebox.showerror("Campo inválido", "O número do endereço está inválido.")
            return False
    else:
        numero_logradouro = None

    cpf_cnpj = ctk_master.ui.GetCampo("cpf_cnpj")
    cpf_cnpj = "".join([s for s in cpf_cnpj if s.isdigit()])
    contato = int(ctk_master.ui.GetCampo("contato"))
    cep = int(ctk_master.ui.GetCampo("cep"))

    logradouro = ctk_master.ui.GetCampo("logradouro")
    if logradouro == "":
        logradouro = None
    complemento = ctk_master.ui.GetCampo("complemento")
    if complemento == "":
        complemento = None
    bairro = ctk_master.ui.GetCampo("bairro")
    if bairro == "":
        bairro = None
    cidade = ctk_master.ui.GetCampo("cidade")
    if cidade == "":
        cidade = None
    uf = ctk_master.ui.GetCampo("uf")
    if uf == "":
        uf = None
    
    parametros = (
        ctk_master.ui.GetCampo("id"),
        ctk_master.ui.GetCampo("nome"),
        cpf_cnpj,
        data,
        cep,
        contato,
        logradouro,
        numero_logradouro,
        complemento,
        bairro,
        cidade,
        uf)

    return parametros