import tkinter as tk
from botao import Botao
from tela_login import TelaLogin
from tela_informacao_nivel1 import TelaInformacaoNivel1
from tela_informacao_nivel2 import TelaInformacaoNivel2
from tela_informacao_nivel3 import TelaInformacaoNivel3
from reconhecimento_facial import ReconhecimentoFacial
from arquivo_configuracao import ArquivoConfiguracao
from pessoa import Pessoa

class Janela:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Autenticação Biométrica")
        self.janela.geometry("500x300")

        self.arquivo_configuracao = ArquivoConfiguracao("config.csv")
        self.reconhecimento_facial = ReconhecimentoFacial()
        self.pessoas = self.arquivo_configuracao.carregar_pessoas()

        self.tela_login = TelaLogin(self.janela, self.reconhecimento_facial, self.pessoas, self.abrir_tela_nivel1, self.abrir_tela_nivel2, self.abrir_tela_nivel3)
        self.tela_informacao_nivel1 = TelaInformacaoNivel1()
        self.tela_informacao_nivel2 = TelaInformacaoNivel2()
        self.tela_informacao_nivel3 = TelaInformacaoNivel3()

        self.botao_sair = Botao(self.janela, "Sair", self.janela.quit)

    def abrir_tela_nivel1(self):
        self.tela_informacao_nivel1.janela.deiconify()
        self.tela_informacao_nivel1.janela.lift()

    def abrir_tela_nivel2(self):
        if self.tela_login.pessoa_atual.eh_supervisor():
            self.tela_informacao_nivel2.janela.deiconify()
            self.tela_informacao_nivel2.janela.lift()

    def abrir_tela_nivel3(self):
        if self.tela_login.pessoa_atual.eh_coordenador():
            self.tela_informacao_nivel3.janela.deiconify()
            self.tela_informacao_nivel3.janela.lift()

    def iniciar(self):
        self.janela.mainloop()
