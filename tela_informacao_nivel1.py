import tkinter as tk

class TelaInformacaoNivel1:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Informação (Nível 1)")
        self.janela.geometry("300x200")
        self.label = tk.Label(self.janela, text="Essa informação é pública (Nível 1).")
        self.label.pack(padx=10, pady=10)
