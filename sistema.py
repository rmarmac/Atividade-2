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

class Aplicativo(ctk.CTk):
    def __init__(self, title: str):
        super().__init__()
        self.banco = Banco()
        self.geometry("1400x900")
        self.title(title)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.janela_abas = ctk.CTkTabview(self)
        self.janela_abas.grid(row=0, column=0, sticky="nsew", padx=default_spacing, pady=default_spacing)

        self.janela_abas.add("Cadastro")
        self.janela_abas.add("Consulta")
        self.ConstrAbaCadastro()
        self.ConstrAbaConsulta()
    
    def _GerarCampoCadastro(self, texto, placeholder, posicao):
        label = ctk.CTkLabel(posicao, text=texto)
        label.pack(pady=(default_spacing,0))
        campo = ctk.CTkEntry(posicao,
                                  placeholder_text=placeholder,
                                  width=default_txtbar_size)
        campo.pack(pady = (0,default_spacing))
        return campo


    def ConstrAbaCadastro(self):
        self.aba_cadastro = self.janela_abas.tab("Cadastro")
        self.aba_cadastro.grid_columnconfigure(0, weight=1)
        self.aba_cadastro.grid_columnconfigure(1, weight=1)
        self.aba_esq = ctk.CTkFrame(self.aba_cadastro)
        self.aba_esq.grid(row=0, column=0, sticky="nsew")
        self.aba_dir = ctk.CTkFrame(self.aba_cadastro)
        self.aba_dir.grid(row=0, column=1, sticky="nsew")

        self.campo_id = self._GerarCampoCadastro("ID",
                                                "Digite seu ID",
                                                self.aba_esq)
        self.campo_nome = self._GerarCampoCadastro("Nome",
                                                    "Digite seu nome",
                                                    self.aba_esq)
        self.campo_CPF_CNPJ = self._GerarCampoCadastro("CPF ou CNPJ",
                                                        "Digite seu CPF ou CNPJ (somente números)",
                                                        self.aba_esq)
        self.campo_nscmnt = self._GerarCampoCadastro("Data de Nascimento",
                                                    "Digite sua data de nascimento XX/XX/XXXX",
                                                    self.aba_esq)
        self.campo_cep = self._GerarCampoCadastro("CEP",
                                                "Digite o CEP",
                                                self.aba_esq)
        self.campo_contato = self._GerarCampoCadastro("Número para contato",
                                                    "Digite o número para contato com DDD",
                                                    self.aba_esq)

        self.delete_button = ctk.CTkButton(self.aba_esq, text="Deletar")
        self.delete_button.pack(pady=(default_spacing, default_spacing))
        self.update_button = ctk.CTkButton(self.aba_esq, text="Atualizar")
        self.update_button.pack(pady=(default_spacing, default_spacing))
        self.campo_logradouro = self._GerarCampoCadastro("Logradouro",
                                                         "Digite a Rua",
                                                         self.aba_dir)
        self.campo_numero = self._GerarCampoCadastro("Número",
                                                    "Digite o Número",
                                                    self.aba_dir)
        self.campo_complemento = self._GerarCampoCadastro("Complemento",
                                                        "Digite o Complemento",
                                                        self.aba_dir)
        self.campo_bairro = self._GerarCampoCadastro("Bairro",
                                                    "Digite o Bairro",
                                                    self.aba_dir)
        self.campo_cidade = self._GerarCampoCadastro("Cidade",
                                                    "Digite a Cidade",
                                                    self.aba_dir)
        self.campo_uf = self._GerarCampoCadastro("UF",
                                                "Digite a Unidade Federativa",
                                                self.aba_dir)

        self.botao_cadastro = ctk.CTkButton(self.aba_dir, text="Cadastrar", command=self._Cadastrar)
        self.botao_cadastro.pack(pady = (default_spacing, 0))

        self.campo_cep.bind("<Return>", lambda event: self._ConsultarCEP(event, self.campo_cep.get()))


    def AtualizarConsulta(self, event, pesquisa):
        if pesquisa != "":
            self.respostaBD = self.banco.PesquisarNPrestadores(pesquisa)
        else:
            self.respostaBD = self.banco.GetNPrestadores()
        for i in range(N_PRESTADORES):
            for j in range(N_COLUNAS_CONSULTA):
                if i < len(self.respostaBD):
                    self.consulta_labels[i][j].configure(text=self.respostaBD[i][j + 1])
                else:
                    self.consulta_labels[i][j].configure(text="")

    def ConstrAbaConsulta(self):
        self.aba_consulta = self.janela_abas.tab("Consulta")
        self.aba_consulta.grid_columnconfigure(0, weight=1)
        self.aba_consulta.grid_rowconfigure(1, weight=1)
        self.superior_consulta = ctk.CTkFrame(self.aba_consulta)
        self.superior_consulta.grid(row=0, column=0, sticky="nsew")
        self.inferior_consulta = ctk.CTkFrame(self.aba_consulta)
        self.inferior_consulta.grid(row=1, column=0, sticky="nsew")
        label = ctk.CTkLabel(self.superior_consulta, text="Consulta de Prestador", font=('Arial', 20))
        label.pack(pady=(default_spacing, default_spacing))
        self.pesquisa = ctk.CTkEntry(self.superior_consulta,
                                     placeholder_text="Pesquise pelo nome de um prestador",
                                     width=default_txtbar_size)
        self.pesquisa.pack(pady=(default_spacing,default_spacing))
        self.pesquisa.bind("<Return>", lambda event: self.AtualizarConsulta(event, self.pesquisa.get()))

        for i in range(N_PRESTADORES + 1):
            self.inferior_consulta.grid_rowconfigure(i, weight=1)
        for i in range(N_COLUNAS_CONSULTA):
            self.inferior_consulta.grid_columnconfigure(i, weight=1)
        
        self.grid_consulta = [[None for _ in range(N_COLUNAS_CONSULTA)] for _ in range(N_PRESTADORES)]
        self.consulta_labels = [[None for _ in range(N_COLUNAS_CONSULTA)] for _ in range(N_PRESTADORES)]

        first_row_labels = ["cadastro","nome","cpf ou cnpj","nascimento","cep","contato","logradouro","numero","complemento","bairro","cidade","uf"]
        for j in range(N_COLUNAS_CONSULTA):
            frame_first_row = ctk.CTkFrame(self.inferior_consulta,fg_color="#124161",border_width=5,corner_radius=0)
            frame_first_row.grid(row=0, column=j, sticky="nsew")
            first_row_label = ctk.CTkLabel(frame_first_row, text=first_row_labels[j])
            first_row_label.pack(expand=True)
        for i in range(N_PRESTADORES):
            for j in range(N_COLUNAS_CONSULTA):
                self.grid_consulta[i][j] = ctk.CTkFrame(self.inferior_consulta, corner_radius=0)
                self.grid_consulta[i][j].grid(row=i + 1, column=j, sticky="nsew")
                self.consulta_labels[i][j] = ctk.CTkLabel(self.grid_consulta[i][j], text=None)
                self.consulta_labels[i][j].pack(expand=True)

        self.respostaBD = self.banco.GetNPrestadores()
        for i in range(N_PRESTADORES):
            for j in range(N_COLUNAS_CONSULTA):
                if i < len(self.respostaBD):
                    self.consulta_labels[i][j].configure(text=self.respostaBD[i][j + 1])




    def _ConsultarCEP(self, event, cep):
        dados = Endereco(cep)
        if dados == False:
            return
        self.campo_logradouro.set(dados['logradouro'])
        self.campo_bairro.set(dados['bairro'])
        self.campo_cidade.set(dados['localidade'])
        self.campo_uf.set(dados['uf'])
        return True

    def _Cadastrar(self):
        if len(self.campo_id.get()) == 0:
            messagebox.showerror("Sem ID", "Insira um ID")
            return
        if len(self.campo_nome.get()) == 0:
            messagebox.showerror("Sem nome", "Insira seu nome")
            return

        if not ExecutarVerificacoesCPF_CNPJ(self.campo_CPF_CNPJ.get()):
            messagebox.showerror("CPF ou CNPJ inválido", "Verifique o CPF ou CNPJ.")
            return
        cpf_cnpj = int(self.campo_CPF_CNPJ.get())

        data = ExecutarVerificacaoDataNasc(self.campo_nscmnt.get())
        if not data:
            messagebox.showerror("Data inválida", "Insira uma data válida")
            return
        else:
            self.campo_nscmnt.set(f"{data.day:02}" + "/" + f"{data.month:02}" + "/" + f"{data.year:04}")
        data = "datetime('" + str(data) + "')"

        if not ExecutarVerificacaoCEP(self.campo_cep.get()):
            messagebox.showerror("Erro no CEP", "CEP inválido.")
            return
        cep = int(self.campo_cep.get())

        if not ExecutarVerificacaoNumero(self.campo_contato.get()):
            messagebox.showerror("Número de celular inválido", "Confira o número de celular (lembre-se do DDD)")
            return
        contato = int(self.campo_contato.get())

        numero_logradouro= self.campo_numero.get()
        if numero_logradouro != "":
            try:
                numero_logradouro = int(numero_logradouro)
            except:
                messagebox.showerror("Campo inválido", "O número do endereço está inválido.")
                return
        else:
            numero_logradouro = None

        logradouro = None
        if self.campo_logradouro.get() != "":
            logradouro = self.campo_logradouro.get()
        complemento = None
        if self.campo_complemento.get() != "":
            complemento = self.campo_complemento.get()
        bairro = None
        if self.campo_bairro.get() != "":
            bairro = self.campo_bairro.get()
        cidade = None
        if self.campo_cidade.get() != "":
            cidade = self.campo_cidade.get()
        uf = None
        if self.campo_uf.get() != "":
            uf = self.campo_uf.get()
        
        parametros = (
            self.campo_id.get(),
            self.campo_nome.get(),
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
        error = self.banco.InsertPrestador(parametros)
        self.AtualizarConsulta(None, "")
        if error != None:
            messagebox.showerror("Error", f"Error {error}")
        else:
            messagebox.showinfo("Cadastro Realizado", "Cadastro Realizado com Sucesso!")


def MainLoop():
    root = Aplicativo("Banco de dados")
    root.mainloop()

MainLoop()