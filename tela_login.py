import tkinter as tk
from tkinter import messagebox

class TelaLogin:
    def __init__(self, reconhecimento_facial, pessoas_autorizadas):
        self.reconhecimento_facial = reconhecimento_facial
        self.pessoas_autorizadas = pessoas_autorizadas
        self.janela = tk.Tk()
        self.janela.title("Login")
        self.janela.geometry("300x200")
        self.criar_componentes()

    def criar_componentes(self):
        # Criar campos de entrada de ID e senha
        self.label_id = tk.Label(self.janela, text="ID:")
        self.label_id.grid(column=0, row=0, padx=10, pady=10)
        self.entry_id = tk.Entry(self.janela)
        self.entry_id.grid(column=1, row=0, padx=10, pady=10)

        self.label_senha = tk.Label(self.janela, text="Senha:")
        self.label_senha.grid(column=0, row=1, padx=10, pady=10)
        self.entry_senha = tk.Entry(self.janela, show="*")
        self.entry_senha.grid(column=1, row=1, padx=10, pady=10)

        # Criar botões de login e sair
        self.botao_login = tk.Button(self.janela, text="Login", command=self.fazer_login)
        self.botao_login.grid(column=0, row=2, padx=10, pady=10)

        self.botao_sair = tk.Button(self.janela, text="Sair", command=self.janela.quit)
        self.botao_sair.grid(column=1, row=2, padx=10, pady=10)

    def fazer_login(self):
        # Verificar se as informações de ID e senha estão corretas
        id = self.entry_id.get()
        senha = self.entry_senha.get()
        pessoa = None
        for p in self.pessoas_autorizadas:
            if p.get_id() == id and p.get_senha() == senha:
                pessoa = p
                break
        if pessoa is None:
            messagebox.showerror("Erro", "ID ou senha incorretos.")
            return

        # Realizar o reconhecimento facial
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        nome_reconhecido = self.reconhecimento_facial.reconhecer_pessoa(frame)
        video_capture.release()

        # Verificar se a pessoa está autorizada
        if nome_reconhecido != pessoa.get_nome():
            messagebox.showerror("Erro", "Reconhecimento facial falhou.")
            return
        if pessoa.get_nivel() == 1:
            messagebox.showinfo("Sucesso", "Login bem-sucedido (Nível 1).")
        elif pessoa.get_nivel() == 2:
            messagebox.showinfo("Sucesso", "Login bem-sucedido (Nível 2).")
        elif pessoa.get_nivel() == 3:
            messagebox.showinfo("Sucesso", "Login bem-sucedido (Nível 3).")
