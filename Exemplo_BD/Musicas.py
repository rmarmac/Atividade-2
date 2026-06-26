from Banco import Banco


class Musica(object):


    def __init__(self, cd_musica=0, titulo="", artista="", genero=""):
        self.info = {}
        self.cd_musica = cd_musica
        self.titulo = titulo
        self.artista = artista
        self.genero = genero


    def insertMusic(self):
        banco = Banco()
        try:

            c = banco.conexao.cursor()

            c.execute("insert into musicas (titulo, artista, genero) values('" + self.titulo + "', '" +
                      self.artista + "', '" + self.genero + "' )")

            banco.conexao.commit()
            c.close()

            return "Música cadastrada com sucesso!"
        except:
            return "Ocorreu um erro na inserção da música"


    @property
    def updateMusic(self):
        banco = Banco()
        try:

            c = banco.conexao.cursor()

            c.execute("update musicas set titulo = '" + self.titulo + "', artista = '" + self.artista +
                      "', genero = '" + self.genero + "' where cd_musica = " + self.cd_musica + " ")

            banco.conexao.commit()
            c.close()

            return "Música atualizada com sucesso!"
        except:
            return "Ocorreu um erro na alteração da música"


    @property
    def deleteMusic(self):
        banco = Banco()
        try:

            c = banco.conexao.cursor()

            c.execute("delete from musicas where cd_musica = " + self.cd_musica + " ")

            banco.conexao.commit()
            c.close()

            return "Música excluída com sucesso!"
        except:
            return "Ocorreu um erro na exclusão da música"


    def selectMusic(self, cd_musica):
        banco = Banco()
        try:

            c = banco.conexao.cursor()

            c.execute("select * from musicas where cd_musica = " + cd_musica + "  ")

            for linha in c:
                self.cd_musica = linha[0]
                self.titulo = linha[1]
                self.artista = linha[2]
                self.genero = linha[3]

            c.close()

            return "Busca feita com sucesso!"
        except:
            return "Ocorreu um erro na busca da música"