import csv

class ArquivoConfiguracao:
    def __init__(self, arquivo_path):
        self.arquivo_path = arquivo_path

    def ler_configuracoes(self):
        pessoas = []
        with open(self.arquivo_path, 'r') as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                nome = linha[0]
                id = linha[1]
                senha = linha[2]
                nivel = int(linha[3])
                pessoa = Pessoa(nome, id, senha, nivel)
                pessoas.append(pessoa)
        return pessoas

    def escrever_configuracoes(self, pessoas):
        with open(self.arquivo_path, 'w', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            for pessoa in pessoas:
                linha = [pessoa.get_nome(), pessoa.get_id(), pessoa.get_senha(), pessoa.get_nivel()]
                escritor.writerow(linha)
