import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from db.db_conection import start_connection, Habitacion
class visualizar_ingresos(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        #! Establecer la conexión a la base de datos:
        self.session = start_connection() 
        
        self.title("Visualizar los Ingresos")

        #! Crear un frame para contener la lista y la tabla
        self.frame_izquierdo = tk.Frame(self, bd=2)
        self.frame_izquierdo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.frame_derecho = tk.Frame(self, bd=2, relief="solid")
        self.frame_derecho.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        self.crear_frame_izquierdo()
        self.crear_frame_derecho()
        
        self.cargar_info_Habitaciones()
        
    def crear_frame_izquierdo(self):
        #! Crear lista desplegable y asignar la opcion inicial
        self.lista_dias = ttk.Combobox(self.frame_izquierdo, values=["Habitaciones","Simple", "Doble", "Triple", "Cuadruple"])
        self.lista_dias.grid(column=0, row=0)
        self.lista_dias.current(0)
        
    def crear_frame_derecho(self):
        #! Configurar el grid para que la tabla ocupe todo el espacio:
        self.frame_derecho.grid_rowconfigure(0, weight=1)
        self.frame_derecho.grid_columnconfigure(0, weight=1)

        #! Crear la tabla y definir las columnas en el frame derecho:
        self.lista_estadias = ttk.Treeview(
            self.frame_derecho, columns=("id", "tipo", "dias_total", "recaudacion_total"), show="headings"
        )

        #! Configurar las cabeceras de las columnas:
        columnas = ["id", "tipo", "dias_total", "recaudacion_total"]
        cabeceras = ["Id", "Tipo", "Dias Estadia Totales", " Recaudacion Total"]

        for col, header in zip(columnas, cabeceras):
            self.lista_estadias.heading(col, text=header)

        #! Establecer ancho de columna, ocultar columna id:
        self.lista_estadias.column("id", width=40, minwidth=40, anchor=tk.CENTER)
        ancho_columna = 122
        for col in columnas[1:]:
            self.lista_estadias.column(col, width=ancho_columna, minwidth=ancho_columna, anchor=tk.CENTER)

        #! Crear un scrollbar vertical:
        scrollbar_vertical = ttk.Scrollbar(self.frame_derecho, orient="vertical", command=self.lista_estadias.yview)
        self.lista_estadias.configure(yscrollcommand=scrollbar_vertical.set)
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")

        #! Layout de la tabla:
        self.lista_estadias.grid(row=0, column=0, sticky="nsew")    
        
    def cargar_info_Habitaciones(self):
        tipo_habitacion = self.lista_dias.get()
        info_habitacion = self.session.query(Habitacion).filter(Habitacion.tipo == tipo_habitacion).all()
        self.lista_estadias.delete(*self.lista_estadias.get_children())

        if not info_habitacion:
            print("Sin Datos")
            return
        
        for Habitacion in info_habitacion:
            self.lista_estadias.insert("", "end", values=(
                Habitacion.id_habitacion,
                Habitacion.tipo,
                Habitacion.dias_total,
                Habitacion.recaudacion_total 
                )
            )