import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from db.db_conection import start_connection, Estadia, Habitacion
from ventanas.modificar_dias_estadia import ModificarDiasEstadia

class CargarEstadias(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        #! Establecer la conexión a la base de datos:
        self.session = start_connection() 

        self.title("Sistema de Hotel")

        #! Crear un frame para contener el formulario y la tabla
        self.frame_izquierdo = tk.Frame(self)
        self.frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_derecho = tk.Frame(self, bd=2, relief="solid")
        self.frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        #! Cargar Frames
        self.crear_frame_izquierdo()
        self.crear_frame_derecho()

        #!Carga de datos en tablas
        self.cargar_referencias()
        self.cargar_estadias_en_curso()

    def crear_frame_izquierdo(self):
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

        #! Layout de la tabla
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
        self.credito = tk.Radiobutton(self.frame_izquierdo, text="Credito", variable=self.forma_de_pago, value="credito")
        self.credito.grid(row=3, column=0, padx=5, pady=5)

        self.contado = tk.Radiobutton(self.frame_izquierdo, text="Contado", variable=self.forma_de_pago, value="contado")
        self.contado.grid(row=3, column=1, padx=5, pady=5)

        #! Crear el botón de cargar estadia:
        self.boton_cargar = tk.Button(self.frame_izquierdo, text="Cargar", command=self.cargar_estadia)
        self.boton_cargar.grid(row=4, column=0, padx=5, pady=5)

        #! Crear el botón de modificar:
        self.boton_modificar = tk.Button(self.frame_izquierdo, text="Modificar", command=self.abrir_ventana_edicion_dias)
        self.boton_modificar.grid(row=4, column=1, padx=5, pady=5)

        #! Crear el botón de Terminar:
        self.boton_terminar = tk.Button(self.frame_izquierdo, text="Terminar", command=self.terminar_estadia)
        self.boton_terminar.grid(row=4, column=2, padx=5, pady=5)

    def crear_frame_derecho(self):
        #! Configurar el grid para que la tabla ocupe todo el espacio:
        self.frame_derecho.grid_rowconfigure(0, weight=1)
        self.frame_derecho.grid_columnconfigure(0, weight=1)

        #! Crear la tabla y definir las columnas en el frame derecho:
        self.lista_estadias = ttk.Treeview(
            self.frame_derecho, columns=("id", "numero", "tipo", "costo", "dias", "sub_total", "descuento", "total"), show="headings"
        )

        #! Configurar las cabeceras de las columnas:
        columnas = ["id", "numero", "tipo", "costo", "dias", "sub_total", "descuento", "total"]
        cabeceras = ["Id", "Numero", "Tipo", "Costo", "Dias", "Sub-Total", "% Descuento", "Total"]

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

    def recuperar_estadia_seleccionada(self):
        seleccion = self.lista_estadias.focus()
        return self.lista_estadias.item(seleccion, "values")

    def finalizar_estadia(self, id_estadia):
        editar_estado = self.session.query(Estadia).filter_by(id_estadia=id_estadia).first()
        editar_estado.state = 'finalizado'
        self.session.commit()
        self.cargar_estadias_en_curso()

    def terminar_estadia(self):
        estadia_a_terminar = self.recuperar_estadia_seleccionada()
        self.finalizar_estadia(estadia_a_terminar[0])

    def cargar_referencias(self):
        #! Obtener referencias de la base de datos
        referencias = self.session.query(Habitacion).all()

        #! Insertar referencias en la tabla
        for referencia in referencias:
            self.tabla_de_referencias.insert("", "end", values=(referencia.tipo, referencia.costo))

    def buscar_estadia_repetida(self, numero_habitacion):
        habitacion_repetida = self.session.query(Estadia).filter(Estadia.state == "En_curso", Estadia.numero_habitacion == numero_habitacion).first()
        if habitacion_repetida:
            self.finalizar_estadia(habitacion_repetida.id_estadia)
        else:
            print("No existe estadias en curso para esta habitacion")

    def cargar_estadias_en_curso(self):
        estadias_en_curso = self.session.query(Estadia).filter(Estadia.state == "En_curso").all()
        self.lista_estadias.delete(*self.lista_estadias.get_children())

        if not estadias_en_curso:
            print("Sin Datos")
            return

        for estadia in estadias_en_curso:
            self.lista_estadias.insert("", "end", values=(
            estadia.id_estadia,
            estadia.numero_habitacion,
            estadia.tipo_habitacion,
            estadia.costo,
            estadia.dias_estadia,
            estadia.sub_total,
            estadia.descuento,
            estadia.total 
    )
)

    def modify_days(self, value):
        estadia_a_modificar = self.recuperar_estadia_seleccionada()
        id_estadia = estadia_a_modificar[0]

        #! Actualizar la estadia en la base de datos
        editar_dias = self.session.query(Estadia).filter_by(id_estadia=id_estadia).first()
        editar_dias.dias_estadia = value
        self.session.commit()
        
        self.cargar_estadias_en_curso()

    def abrir_ventana_edicion_dias(self):
        estadia_a_modificar = self.recuperar_estadia_seleccionada()
        dias_estadia = estadia_a_modificar[4]

        ventana_referencia = ModificarDiasEstadia(self, dias_estadia)
        ventana_referencia.transient(self)
        ventana_referencia.grab_set()
        self.wait_window(ventana_referencia)

    def descuento(self, dias_estadia, forma_de_pago):
        descuento = 0
        if forma_de_pago == "contado":
            descuento = 10
        elif forma_de_pago == "credito" and dias_estadia > 5:
            descuento = 5
        if dias_estadia > 10:
            descuento += 2
        return descuento

    def cargar_estadia(self):
        #! Recuperacion de datos del formulario:
        numero_habitacion = self.nro_habitacion.get()
        seleccion = self.tabla_de_referencias.focus()
        dias_estadia = self.dias_estadia.get()
        forma_de_pago = self.forma_de_pago.get()

        #! Finalizar estadia de habitacion seleccionada si esta en curso:
        self.buscar_estadia_repetida(numero_habitacion)

        #! Validacion de datos:
        if not numero_habitacion:
            messagebox.showerror("Error", "Ingrese un valor valido para Numero de la Habitacion")
            return

        if not seleccion:
            messagebox.showerror("Error", "Seleccione un Tipo de Habitacion")
            return

        if not dias_estadia:
            messagebox.showerror("Error", "Ingrese un valor valido para las dias de Estadia")
            return

        if not forma_de_pago:
            messagebox.showerror("Error", "Seleccione la Forma de Pago")
            return

        #! Conversion archivo seleccionado en una tupla:
        valores_fila = self.tabla_de_referencias.item(seleccion, "values")
        #! Hallar el descuento:
        descuento = self.descuento(dias_estadia=int(dias_estadia), forma_de_pago=forma_de_pago)
        #! Hallar el sub_total y el total:
        sub_total = int(valores_fila[1]) * int(dias_estadia)
        total = int(sub_total * (1 - (descuento / 100)))

        nueva_estadia = Estadia(
            numero_habitacion = numero_habitacion,
            tipo_habitacion =   valores_fila[0],
            costo =             int(valores_fila[1]),
            dias_estadia =      int(dias_estadia),
            descuento =         descuento,
            sub_total =         sub_total,
            total =             total,
            forma_de_pago =     forma_de_pago,
            state =             "En_curso"
        )

        self.session.add(nueva_estadia)
        self.session.commit()
        self.session.refresh(nueva_estadia)

        self.lista_estadias.insert("", "end", values=(
            nueva_estadia.id_estadia,
            numero_habitacion,
            valores_fila[0],
            valores_fila[1],
            dias_estadia,
            sub_total,
            descuento,
            total
        ))

if __name__ == "__main__":
    app = CargarEstadias(None)
    app.mainloop()
