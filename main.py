import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tk_messagebox

from db_conection import start_connection, Estadia

class RegistrosHotel(tk.Tk):
    def _init_(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #! Establecer la conexión a la base de datos:
        self.session = start_connection() 

        self.title("Sistema de Hotel")

        #! Crear un frame para contener el formulario y la tabla
        self.frame_izquierdo = tk.Frame(self)
        self.frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_derecho = tk.Frame(self)
        self.frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

#?=====================================================================================================================================================================
        #? Frame Izquierdo
#?=====================================================================================================================================================================
        #! Etiquetas:
        tk.Label(self.frame_izquierdo, text="Nro. de Habitacion:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.frame_izquierdo, text="Dias de Estadia:").grid(row=2, column=0, padx=10, pady=10)

        #! Entrada del Numero de la habitacion:
        self.nro_habitacion = tk.Entry(self.frame_izquierdo)
        self.nro_habitacion.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        #! Crear la tabla y definir las columnas
        self.tabla_de_referencias = ttk.Treeview(
            self.frame_izquierdo, columns=("tipo", "costo",), show="headings"
        )

        #! Poner titulo a las columnas
        self.tabla_de_referencias.heading("tipo", text="Tipo")
        self.tabla_de_referencias.heading("costo", text="Costo")

        #! Layoud de la tabla
        self.tabla_de_referencias.grid(
            row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=10
        )

        #! Entrada de los dias de Estadia:
        self.dias_estadia = tk.Entry(self.frame_izquierdo)
        self.dias_estadia.grid(row=2, column=1, sticky="nsew", padx=10, pady=5)

        #! Definir variable para radio button:
        self.forma_de_pago = tk.StringVar()
        self.forma_de_pago.set("credito")

        #! Definir radio buttons:
        self.credito = tk.Radiobutton(self.frame_izquierdo, text="Credito", variable=self.forma_de_pago, value = "credito")
        self.credito.grid(row=3, column=0, padx=5, pady=5)

        self.contado = tk.Radiobutton(self.frame_izquierdo, text="Contado", variable=self.forma_de_pago, value="contado")
        self.contado.grid(row=3, column=1, padx=5, pady=5)

        #! Crear el botónes:
        self.boton_cargar = tk.Button(self.frame_izquierdo, text="Cargar", command=self.cargar_estadia)
        self.boton_cargar.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        self.cargar_referencias()

#?=====================================================================================================================================================================
        #? Tabla del Frame Derecho
#?=====================================================================================================================================================================
        #! Crear la tabla y definir las columnas en el frame derecho
        self.lista_estadias = ttk.Treeview(
            self.frame_derecho, columns=("numero", "tipo", "costo", "dias", "sub_total", "descuento", "total"), show="headings"
        )

        #! Configurar las cabeceras de las columnas
        columnas = ["numero", "tipo", "costo", "dias", "sub_total", "descuento", "total"]
        cabeceras = ["Numero", "Tipo", "Costo", "Dias", "Sub-Total", "% Descuento", "Total"]

        for col, header in zip(columnas, cabeceras):
            self.lista_estadias.heading(col, text=header)

        #! Calcular el ancho total disponible
        #* ancho_disponible = self.winfo_screenwidth() - self.frame_derecho.winfo_rootx()

        #! Distribuir el ancho entre las columnas de manera proporcional
        ancho_columna = 129#*(ancho_disponible//3// len(columnas))
        for col in columnas:
            self.lista_estadias.column(col, width=ancho_columna, minwidth=ancho_columna, anchor=tk.CENTER)

        #! Layout de la tabla
        self.lista_estadias.grid(
            row=0, column=0, sticky="nsew"
        )

        self.cargar_Estadias_En_curso()

    def cargar_referencias(self):
        tipos = ["Simple", "Doble", "Triple", "Cuadruple"]
        costos = [50000, 80000, 120000, 150000]

        for tipo, costo in zip(tipos, costos):
            self.tabla_de_referencias.insert("", "end", values=(tipo, costo,))

    def finalizar_estadia(self, id_estadia):
        ciudad_editar = (
            self.session.query(Estadia).filter_by(id_estadia = id_estadia).first()
        )

        ciudad_editar.estado = "finalizado"
        self.session.commit()

        self.cargar_Estadias_En_curso() #! Cambiar a una modificacion de la tabla

    def vuscar_estadia_repetida(self, nur_habitacion):
        abitacion_repetida = self.session.query(Estadia).filter(Estadia.estado == "En_curso", Estadia.numero == nur_habitacion).first()

        if abitacion_repetida:
            self.finalizar_estadia(abitacion_repetida.id_estadia)
        else: print("No existe estadias en curso para esta abitacion")

    def cargar_Estadias_En_curso(self):
        estadias_en_curso = self.session.query(Estadia).filter(Estadia.estado == "En_curso").all()
        self.lista_estadias.delete(*self.lista_estadias.get_children())
        
        if not estadias_en_curso: 
            print("Sin Datos")
            return

        for estadia in estadias_en_curso:
            self.lista_estadias.insert("", "end", values=(estadia.numero, estadia.tipo, estadia.costo, estadia.dias_estadia, estadia.forma_de_pago))

    def cargar_estadia(self):
        #! Recuperacion de datos:
        nur_habitacion = self.nro_habitacion.get()
        seleccion = self.tabla_de_referencias.focus()
        dias_estadia = self.dias_estadia.get()
        forma_de_pago = self.forma_de_pago.get()

        #! Finalizar estadia de abitacion seleccionada si esta en curso:
        self.vuscar_estadia_repetida(nur_habitacion)

        #! Validacion de datos: 
        if not nur_habitacion:
            tk_messagebox.showerror("Error", "Ingrese un valor valido para Numero de la Habitacion")
            return

        if not seleccion:
            tk_messagebox.showerror("Error", "Seleccione un Tipo de Habitacion")
            return

        if not dias_estadia:
            tk_messagebox.showerror("Error", "Ingrese un valor valido para las dia de Estadia")
            return

        if not forma_de_pago:
            tk_messagebox.showerror("Error", "Seleccione la Forma de Pago")
            return

        #! Combercion archivo seleccionado en una tupla:
        valores_fila = self.tabla_de_referencias.item(seleccion, "values")

        #! Instanciacion de Objeto estadia:
        nueva_estadia = Estadia(
            numero= nur_habitacion,
            tipo= valores_fila[0],
            costo= valores_fila[1],
            dias_estadia= dias_estadia,
            forma_de_pago= forma_de_pago,
            estado= "En_curso")

        self.session.add(nueva_estadia)
        self.session.commit()

        self.lista_estadias.insert("", "end", values=(nur_habitacion, valores_fila[0], valores_fila[1], dias_estadia, forma_de_pago))

if __name__ == "__main__":
    app = RegistrosHotel()
    app.mainloop()

#===========================================================================================================================================================
#! Notas:
#* Iteracion simultanes de arreglos:
#? En la linea  for tipo, costo in zip(tipos, costos):
#? Usamos la funcion zip() para Tomar elementos de cada iterable y los empareja en tuplas. Luego, puedes iterar sobre esas tuplas utilizando un bucle for. 
#? Esto te permite tratar los elementos de los arreglos tipos y costos como si estuvieran en un solo arreglo.