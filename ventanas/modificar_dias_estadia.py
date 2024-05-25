import tkinter as tk
from tkinter import ttk
from db.db_conection import start_connection, Estadia

class modificar_dias(tk.Toplevel):
    def __init__(self, parent, id_estadia):
        super().__init__(parent)
        self.parent = parent  # Guardar la referencia del padre
        self.id_estadia = id_estadia
        self.title("Modificar Días de Estadia")

        #! Establecer la conexión a la base de datos:
        self.session = start_connection()

        self.label = tk.Label(self, text="Nueva Estadia:")
        self.label.grid(row=0, column=0, padx=20, pady=20)

        #! Crear entrada de días de estadia
        self.nueva_estadia = tk.Entry(self)
        self.nueva_estadia.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        #! Boton para modificar los días de estadia:
        self.boton_modificar = tk.Button(self, text="Modificar", command=self.modificar_dias_estadias)
        self.boton_modificar.grid(row=1, column=0, padx=5, pady=5)

    def modificar_dias_estadias(self):
        #! Recuperar el valor ingresado
        nuevos_dias = int(self.nueva_estadia.get())

        #! Actualizar la estadia en la base de datos
        editar_dias = self.session.query(Estadia).filter_by(id_estadia=self.id_estadia).first()
        editar_dias.dias_estadia = nuevos_dias
        self.session.commit()

