import customtkinter as ctk
from endereco import Endereco
from verificador import *
from tkinter import messagebox
from banco import Banco
from banco import N_PRESTADORES

N_COLUNAS_CONSULTA = 12

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
default_spacing = 15
default_txtbar_size = 300

class UI():
    def __init__(self):
        self.dimensions = "1400x900"
        self.campos_preenchimento : dict[str, ctk.CTkEntry] = {}

    def GerarTela(self, ctk_master : ctk.CTk, title):
        ctk_master.geometry(self.dimensions)
        ctk_master.title(title)
        ctk_master.grid_columnconfigure(0, weight=1)
        ctk_master.grid_rowconfigure(0, weight=1)

        self.janela_abas = ctk.CTkTabview(ctk_master)
        self.janela_abas.grid(row=0, column=0, sticky="nsew", padx=default_spacing, pady=default_spacing)

        self.janela_abas.add("Cadastro")
        self.janela_abas.add("Consulta")
        self.ConstrAbaCadastro(ctk_master)
        self.ConstrAbaConsulta(ctk_master)

    def ConstrAbaCadastro(self, ctk_master : Aplicativo):
        self.aba_cadastro = self.janela_abas.tab("Cadastro")
        self.aba_cadastro.grid_columnconfigure(0, weight=1)
        self.aba_cadastro.grid_columnconfigure(1, weight=1)
        self.aba_esq = ctk.CTkFrame(self.aba_cadastro)
        self.aba_esq.grid(row=0, column=0, sticky="nsew")
        self.aba_dir = ctk.CTkFrame(self.aba_cadastro)
        self.aba_dir.grid(row=0, column=1, sticky="nsew")

        self.CriarCampoPreenchimento(self.aba_esq, "id", "ID", "Digite seu ID")
        self.CriarCampoPreenchimento(self.aba_esq, "nome", "Nome", "Digite seu nome")
        self.CriarCampoPreenchimento(self.aba_esq, "cpf_cnpj", "CPF ou CNPJ","Digite seu CPF ou CNPJ (somente números)")
        self.CriarCampoPreenchimento(self.aba_esq, "data", "Data de Nascimento","Digite sua data de nascimento XX/XX/XXXX")
        self.CriarCampoPreenchimento(self.aba_esq, "cep", "CEP","Digite o CEP")
        self.CriarCampoPreenchimento(self.aba_esq, "contato", "Número para contato","Digite o número para contato com DDD")
        self.CriarCampoPreenchimento(self.aba_dir, "logradouro", "Logradouro","Digite a Rua")
        self.CriarCampoPreenchimento(self.aba_dir, "numero", "Número","Digite o Número")
        self.CriarCampoPreenchimento(self.aba_dir, "complemento", "Complemento","Digite o Complemento")
        self.CriarCampoPreenchimento(self.aba_dir, "bairro", "Bairro","Digite o Bairro")
        self.CriarCampoPreenchimento(self.aba_dir, "cidade", "Cidade","Digite a Cidade")
        self.CriarCampoPreenchimento(self.aba_dir, "uf", "UF","Digite a Unidade Federativa")

        self.delete_button = ctk.CTkButton(self.aba_esq, text="Deletar", command=ctk_master.Delete)
        self.delete_button.pack(pady=(default_spacing, default_spacing))
        self.update_button = ctk.CTkButton(self.aba_esq, text="Atualizar", command=ctk_master.AtualizarInfo)
        self.update_button.pack(pady=(default_spacing, default_spacing))

        self.botao_cadastro = ctk.CTkButton(self.aba_dir, text="Cadastrar", command=ctk_master.Cadastrar)
        self.botao_cadastro.pack(pady = (default_spacing, 0))

        self.campos_preenchimento["cep"].bind("<Return>", lambda event: self.PreencherAutoCEP(event, self.GetCampo("cep")))

    def ConstrAbaConsulta(self, ctk_master : Aplicativo):
        self.aba_consulta = self.janela_abas.tab("Consulta")
        self.aba_consulta.grid_columnconfigure(0, weight=1)
        self.aba_consulta.grid_rowconfigure(1, weight=1)
        self.superior_consulta = ctk.CTkFrame(self.aba_consulta)
        self.superior_consulta.grid(row=0, column=0, sticky="nsew")
        self.inferior_consulta = ctk.CTkFrame(self.aba_consulta)
        self.inferior_consulta.grid(row=1, column=0, sticky="nsew")
        label = ctk.CTkLabel(self.superior_consulta, text="Consulta de Prestador", font=('Arial', 20))
        label.pack(pady=(default_spacing, default_spacing))
        self.CriarCampoPreenchimento(self.superior_consulta, "pesquisa", None, "Pesquise pelo nome de um prestador")

        self.campos_preenchimento["pesquisa"].bind("<Return>", lambda event: self.AtualizarUIPesquisa(event,
                                                                                                      self.GetCampo("pesquisa"),
                                                                                                      ctk_master))

        for i in range(N_PRESTADORES + 1):
            self.inferior_consulta.grid_rowconfigure(i, weight=1)
        for i in range(N_COLUNAS_CONSULTA):
            self.inferior_consulta.grid_columnconfigure(i, weight=1)
        
        self.grid_consulta = [[None for _ in range(N_COLUNAS_CONSULTA)] for _ in range(N_PRESTADORES)]
        self.consulta_labels = [[None for _ in range(N_COLUNAS_CONSULTA)] for _ in range(N_PRESTADORES)]

        first_row_labels = ["cadastro","nome","cpf ou cnpj","nascimento","cep","contato","logradouro","numero","complemento","bairro","cidade","uf"]
        for j in range(N_COLUNAS_CONSULTA):
            frame_first_row = ctk.CTkFrame(self.inferior_consulta,fg_color="#124161",border_width=3,corner_radius=0)
            frame_first_row.grid(row=0, column=j, sticky="nsew")
            first_row_label = ctk.CTkLabel(frame_first_row, text=first_row_labels[j])
            first_row_label.pack(expand=True)
        for i in range(N_PRESTADORES):
            for j in range(N_COLUNAS_CONSULTA):
                self.grid_consulta[i][j] = ctk.CTkFrame(self.inferior_consulta, fg_color="#151F30", corner_radius=0)
                self.grid_consulta[i][j].grid(row=i + 1, column=j, sticky="nsew")
                self.consulta_labels[i][j] = ctk.CTkLabel(self.grid_consulta[i][j], text=None)
                self.consulta_labels[i][j].pack(expand=True)

        resp = ctk_master.banco.GetNPrestadores()
        for i in range(len(resp)):
            for j in range(N_COLUNAS_CONSULTA):
                self.consulta_labels[i][j].configure(text=resp[i][j + 1])

    def AtualizarUIPesquisa(self, event, pesquisa, ctk_master : Aplicativo):
        resp = []
        if pesquisa != "":
            resp = ctk_master.banco.PesquisarNPrestadores(pesquisa)
        else:
            resp = ctk_master.banco.GetNPrestadores()
        for i in range(N_PRESTADORES):
            for j in range(N_COLUNAS_CONSULTA):
                if i < len(resp):
                    self.consulta_labels[i][j].configure(text=resp[i][j + 1])
                else:
                    self.consulta_labels[i][j].configure(text="")

    def CriarCampoPreenchimento(self, ctk_master, key, titulo_campo, placeholder, gap=(default_spacing, default_spacing)):
        temp_gap = default_spacing
        if titulo_campo != None:
            label = ctk.CTkLabel(ctk_master, text=titulo_campo)
            label.pack(pady=(gap[0], 0))
            temp_gap = 0

        self.campos_preenchimento[key] = ctk.CTkEntry(ctk_master, placeholder_text=placeholder, width=default_txtbar_size)
        self.campos_preenchimento[key].pack(pady=(temp_gap, default_spacing))
    
    def PreencherAutoCEP(self, event, cep):
        dados = Endereco(cep)
        if not dados:
            return
        self.SetCampo("logradouro", dados['logradouro'])
        self.SetCampo('bairro', dados['bairro'])
        self.SetCampo('cidade', dados['localidade'])
        self.SetCampo('uf', dados['uf'])

    def GetCampo(self, key : str):
        return self.campos_preenchimento[key].get()
    def SetCampo(self, key : str, valor : str):
        self.campos_preenchimento[key].set(valor)



class Aplicativo(ctk.CTk):
    def __init__(self, title: str):
        super().__init__()
        self.banco = Banco()
        self.ui = UI()
        self.ui.GerarTela(self, title)

    def AtualizarInfo(self):
        try:
            resp = self.banco.GetPrestadorCPF_CNPJ(int(self.ui.GetCampo("cpf_cnpj")))
            if resp == False:
                messagebox.showerror("CPF ou CNPJ não encontrado", "Não encontramos o prestador.")
                return
            resp = resp[0]
            for i, key in enumerate(self.ui.campos_preenchimento):
                if i + 1 == len(resp):
                    break
                if self.ui.GetCampo(key) == "":
                    if resp[i + 1] != None:
                        self.ui.SetCampo(key, resp[i + 1])
            self.ui.SetCampo("data", datetime.datetime.strptime(resp[4], "datetime('%Y-%m-%d %H:%M:%S')").strftime('%d/%m/%Y'))
            
            self.banco.DeletePrestadorCPF_CNPJ(int(self.ui.GetCampo("cpf_cnpj")))
            self.Cadastrar()
        except:
            messagebox.showerror("Falha ao Atualizar","Não foi possível atualizar o elemento. Verifique o preenchimento do campo.")

    def Delete(self):
        try:
            if self.banco.DeletePrestadorCPF_CNPJ(int(self.ui.GetCampo("cpf_cnpj"))) == False:
                messagebox.showerror("CPF ou CNPJ não encontrado", "Não encontramos o prestador.")
                return
            self.ui.AtualizarUIPesquisa(None, "", self)
            messagebox.showinfo("Removido","O prestador foi removido da nossa Base de Dados com sucesso!")
        except:
            messagebox.showerror("Falha ao Deletar","Não foi possível deletar o elemento. Verifique o preenchimento do campo.")

    def Cadastrar(self):
        parametros = VerificacaoCadastro(self)
        if not parametros:
            return
        error = self.banco.InsertPrestador(parametros)
        self.ui.AtualizarUIPesquisa(None, "", self)
        if error != None:
            messagebox.showerror("Error", f"Error {error}")
        else:
            messagebox.showinfo("Cadastro Realizado", "Cadastro Realizado com Sucesso!")

def MainLoop():
    root = Aplicativo("Banco de dados")
    root.mainloop()
