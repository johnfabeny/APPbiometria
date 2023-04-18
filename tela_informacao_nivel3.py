import tkinter as tk

class TelaInformacaoNivel3:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Informação (Nível 3)")
        self.janela.geometry("300x200")
        self.label = tk.Label(self.janela, text="Essa informação é restrita aos Coordenadores (Nível 3).")
        self.label.pack(padx=10, pady=10)
