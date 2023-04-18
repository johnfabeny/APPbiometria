import tkinter as tk

class Botao:
    def __init__(self, janela, text, command):
        self.botao = tk.Button(janela, text=text, command=command)
        self.botao.pack(padx=10, pady=10)
