import tkinter as tk


class cargar_referencias(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cargar Tipo y Costo de Habitaciones")

        self.label = tk.Label(self, text="Cargar Tipo y Costo de Habitaciones")
        self.label.grid(row=0, column=0, padx=20, pady=20)