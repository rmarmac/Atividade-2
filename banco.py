import sqlite3

N_PRESTADORES = 8

class Banco():
    def __init__(self):
        self.conexao = sqlite3.connect('prestadores.db')
        self.createTable()


    def createTable(self):
        self.cursor = self.conexao.cursor()

        self.cursor.execute("""create table if not exists prestadores(
                     id_prestador integer primary key autoincrement,
                     id_cadastro text NOT NULL,
                     nome text NOT NULL,
                     cpf_cnpj int NOT NULL UNIQUE,
                     data_nasc text NOT NULL,
                     cep int NOT NULL,
                     numero_contato int NOT NULL,
                     logradouro text,
                     numero int,
                     complemento text,
                     bairro text,
                     cidade text,
                     uf text)""")
        self.conexao.commit()
    
    def InsertPrestador(self, parametros):
        try:
            sql = '''insert into prestadores
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            parametros = (None,) + parametros
            self.cursor.execute(sql, parametros)
            self.conexao.commit()
            return None
        except Exception as e:
            return e
    
    def GetNPrestadores(self):
        sql = '''select * from prestadores'''
        self.cursor.execute(sql)
        resp = self.cursor.fetchmany(N_PRESTADORES)
        self.conexao.commit()
        return resp
    
    def PesquisarNPrestadores(self, pesquisa):
        sql = f'''select * from prestadores where nome like '%{pesquisa}%' '''
        self.cursor.execute(sql)
        resp = self.cursor.fetchmany(N_PRESTADORES)
        self.conexao.commit()
        return resp