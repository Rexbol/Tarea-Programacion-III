import tkinter as tk


class visualizar_ingresos(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Visualizar los Ingresos")

        self.label = tk.Label(self, text="Visualizar los Ingresos")
        self.label.grid(row=0, column=0, padx=20, pady=20)