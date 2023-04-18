import tkinter as tk

class TelaInformacaoNivel2:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Informação (Nível 2)")
        self.janela.geometry("300x200")
        self.label = tk.Label(self.janela, text="Essa informação é restrita aos Supervisores (Nível 2).")
        self.label.pack(padx=10, pady=10)

