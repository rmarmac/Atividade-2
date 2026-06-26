import sqlite3


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