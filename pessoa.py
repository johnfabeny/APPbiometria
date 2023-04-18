class Pessoa:
    def __init__(self, nome, id, senha, nivel):
        self.nome = nome
        self.id = id
        self.senha = senha
        self.nivel = nivel

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_senha(self):
        return self.senha

    def set_senha(self, senha):
        self.senha = senha

    def get_nivel(self):
        return self.nivel

    def set_nivel(self, nivel):
        self.nivel = nivel
