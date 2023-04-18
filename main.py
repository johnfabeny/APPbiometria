from tkinter import messagebox
from pessoa import Pessoa
from reconhecimento_facial import ReconhecimentoFacial
from arquivo_configuracao import ArquivoConfiguracao
from tela_login import TelaLogin
from tela_informacao_nivel1 import TelaInformacaoNivel1
from tela_informacao_nivel2 import TelaInformacaoNivel2
from tela_informacao_nivel3 import TelaInformacaoNivel3
from botao import Botao
from janela import Janela





class Main:
    def __init__(self):
        # Instanciando objetos das classes necessárias
        self.arquivo_config = ArquivoConfiguracao()
        self.reconhecimento_facial = ReconhecimentoFacial()
        self.tela_login = TelaLogin()
        self.tela_nivel1 = TelaInformacaoNivel1()
        self.tela_nivel2 = TelaInformacaoNivel2()
        self.tela_nivel3 = TelaInformacaoNivel3()
        self.janela_principal = Janela()

        # Configurando a janela principal
        self.janela_principal.titulo("Sistema de Controle de Acesso")
        self.janela_principal.adicionar_tela(self.tela_login)

        # Configurando os botões de cada tela
        self.configurar_botoes_tela_login()
        self.configurar_botoes_tela_nivel1()
        self.configurar_botoes_tela_nivel2()
        self.configurar_botoes_tela_nivel3()

        # Lendo as informações de autenticação e permissão de acesso do arquivo de configuração
        self.arquivo_config.ler_arquivo()

    def run(self):
        # Inicializando a aplicação
        self.janela_principal.run()

    def autenticar_usuario(self):
        # Verificando se o usuário é reconhecido pela câmera
        if self.reconhecimento_facial.reconhecer_usuario():
            # Obtendo as informações do usuário autenticado
            pessoa = self.arquivo_config.buscar_pessoa(self.reconhecimento_facial.id_pessoa_autenticada)

            # Verificando se o usuário possui permissão de acesso à tela de nível 1
            if pessoa.nivel_acesso >= 1:
                # Atualizando a janela principal com a tela de nível 1
                self.janela_principal.remover_tela(self.tela_login)
                self.janela_principal.adicionar_tela(self.tela_nivel1)

                # Exibindo as informações de nível 1
                self.tela_nivel1.exibir_informacoes()
            else:
                # Exibindo mensagem de erro de permissão de acesso
                self.tela_login.exibir_mensagem("Usuário não possui permissão de acesso!")
        else:
            # Exibindo mensagem de erro de autenticação
            self.tela_login.exibir_mensagem("Usuário não reconhecido pela câmera!")

    def acessar_tela_nivel2(self):
        # Verificando se o usuário possui permissão de acesso à tela de nível 2
        if self.arquivo_config.buscar_pessoa(self.reconhecimento_facial.id_pessoa_autenticada).nivel_acesso >= 2:
            # Atualizando a janela principal com a tela de nível 2
            self.janela_principal.limpar_tela()
            self.janela_principal.atualizar_titulo("Tela de Informações - Nível 2")
            self.janela_principal.adicionar_widget(self.tela_nivel2)
        else:
            messagebox.showerror("Erro de Autenticação", "Usuário sem permissão para acessar esta tela!")

    def acessar_tela_nivel3(self):
        # Verificando se o usuário possui permissão de acesso à tela de nível 3
        if self.arquivo_config.buscar_pessoa(self.reconhecimento_facial.id_pessoa_autenticada).nivel_acesso >= 3:
            # Atualizando a janela principal com a tela de nível 3
            self.janela_principal.limpar_tela()
            self.janela_principal.atualizar_titulo("Tela de Informações - Nível 3")
            self.janela_principal.adicionar_widget(self.tela_nivel3)
        else:
            messagebox.showerror("Erro de Autenticação", "Usuário sem permissão para acessar esta tela!")

    def sair(self):
        self.janela_principal.fechar_janela()
        # Finalizando a câmera
        self.reconhecimento_facial.finalizar_camera()

    if __name__ == '__main__':
        # Criando a instância do objeto da classe Main
        app = Main()
          
        # Iniciando a aplicação
        app.run()
