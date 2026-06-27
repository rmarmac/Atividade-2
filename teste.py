import datetime
from banco import Banco

banco = Banco()
resp = banco.GetPrestadorCPF_CNPJ("11144477735")
dt_format = datetime.datetime.strptime(resp[0][4], "datetime('%Y-%m-%d %H:%M:%S')")
print(dt_format.strftime('%d/%m/%Y'))