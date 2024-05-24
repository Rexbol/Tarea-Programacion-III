import tkinter as tk
from db.db_conection import get_total_finalizado

class visualizar_ingresos(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Visualizar los Ingresos")

        #! Etiquetas:
        tk.Label(self, text="Ingresos").grid(row=0, column=0, padx=10, pady=10)

        #! Entrada de Ingresos:
        self.ingresos = tk.Entry(self, state='readonly')
        self.ingresos.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        #! Crear el botón de cargar ingresos:
        self.boton_cargar = tk.Button(self, text="Cargar", command=self.cargar_ingresos)
        self.boton_cargar.grid(row=4, column=0, padx=5, pady=5)

        self.cargar_ingresos()

    def cargar_ingresos(self):

        ingresos_octenidos = get_total_finalizado("Simple")

        self.ingresos.config(state='normal')

        self.ingresos.delete(0, tk.END)
        self.ingresos.insert(0, ingresos_octenidos)

        self.ingresos.config(state='readonly')

