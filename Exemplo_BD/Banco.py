#importando módulo do SQlite
import sqlite3


class Banco():


    def __init__(self):
        self.conexao = sqlite3.connect('musica.db')
        self.createTable()


    def createTable(self):
        c = self.conexao.cursor()

        c.execute("""create table if not exists musicas(
                     cd_musica integer primary key autoincrement,
                     titulo text,
                     artista text,
                     genero text)""")
        self.conexao.commit()
        c.close()