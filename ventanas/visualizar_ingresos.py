import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from db.db_conection import get_total_finalizado, start_connection, Estadia
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
        
    def crear_frame_izquierdo(self):
        #! Crear lista desplegable y asignar la opcion inicial
        self.lista_dias = ttk.Combobox(self.frame_izquierdo, values=["Habitaciones","Simple", "Doble", "Triple", "Cuadruple"])
        self.lista_dias.grid(row=0, column=0, padx=5, pady=5)
        self.lista_dias.current(0)

        #! Boton para traer los totales de ingresos:
        self.boton_calcular = tk.Button(self.frame_izquierdo, text="Calcular", command=self.cargar_info_Habitaciones)
        self.boton_calcular.grid(row=1, column=0, padx=5, pady=5)
        
    def crear_frame_derecho(self):
        #! Configurar el grid para que la tabla ocupe todo el espacio:
        self.frame_derecho.grid_rowconfigure(0, weight=1)
        self.frame_derecho.grid_columnconfigure(0, weight=1)

        #! Crear la tabla y definir las columnas en el frame derecho:
        self.tabla_ingresos = ttk.Treeview(
            self.frame_derecho, columns=("tipo", "dias", "recaudacion_total"), show="headings"
        )

        #! Configurar las cabeceras de las columnas:
        columnas = ["tipo", "dias", "recaudacion_total"]
        cabeceras = ["Tipo", "Dias de Estadias", " Recaudacion Total"]

        for col, header in zip(columnas, cabeceras):
            self.tabla_ingresos.heading(col, text=header)

        #! Establecer ancho de columna:
        ancho_columna = 122
        for col in columnas:
            self.tabla_ingresos.column(col, width=ancho_columna, minwidth=ancho_columna, anchor=tk.CENTER)

        #! Layout de la tabla:
        self.tabla_ingresos.grid(row=0, column=0, sticky="nsew")
                
    def cargar_info_Habitaciones(self):
        tipo_habitacion = self.lista_dias.get()
        self.tabla_ingresos.delete(*self.tabla_ingresos.get_children())
        total = get_total_finalizado(tipo_habitacion)
        print(total)
        self.tabla_ingresos.insert("", "end", values=(tipo_habitacion, total[0], total[1]))

#! Forma de uso de la funcion get_total_finalizado
# import tkinter as tk
# from db.db_conection import get_total_finalizado

# class visualizar_ingresos(tk.Toplevel):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.title("Visualizar los Ingresos")

#         #! Etiquetas:
#         tk.Label(self, text="Ingresos").grid(row=0, column=0, padx=10, pady=10)

#         #! Entrada de Ingresos:
#         self.ingresos = tk.Entry(self, state='readonly')
#         self.ingresos.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

#         #! Crear el botón de cargar ingresos:
#         self.boton_cargar = tk.Button(self, text="Cargar", command=self.cargar_ingresos)
#         self.boton_cargar.grid(row=4, column=0, padx=5, pady=5)

#         self.cargar_ingresos()

#     def cargar_ingresos(self):

#         ingresos_octenidos = get_total_finalizado("Simple")

#         self.ingresos.config(state='normal')

#         self.ingresos.delete(0, tk.END)
#         self.ingresos.insert(0, ingresos_octenidos)

#         self.ingresos.config(state='readonly')
