import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tk_messagebox
from db.db_conection import start_connection, Habitacion


class cargar_referencias(tk.Toplevel):
    def _init_(self, parent):
        super()._init_(parent)
        
        self.title("Cargar Tipo y Costo de Habitaciones")

        self.session = start_connection()

        self.label = tk.Label(self, text="Cargar Tipo y Costo de Habitaciones")
        self.label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

        # Etiquetas
        self.label_tipo = tk.Label(self, text="Tipo: ")
        self.label_tipo.grid(row=1, column=0, padx=20, pady=10, sticky=tk.E)
        self.label_costo = tk.Label(self, text="Costo: ")
        self.label_costo.grid(row=2, column=0, padx=20, pady=10, sticky=tk.E)

        # Cajas de texto
        self.tipo_entry = tk.Entry(self)
        self.tipo_entry.grid(row=1, column=1, padx=10, pady=10)
        self.costo_entry = tk.Entry(self)
        self.costo_entry.grid(row=2, column=1, padx=10, pady=10)

        # Botones
        self.guardar_button = tk.Button(self, text="Guardar", command=self.guardar_referencia)
        self.guardar_button.grid(row=3, column=0, padx=10, pady=10)
        self.borrar_button = tk.Button(self, text="Borrar", command=self.borrar_referencia)
        self.borrar_button.grid(row=3, column=1, padx=10, pady=10)

        # Tabla
        self.tabla_referencias = ttk.Treeview(self, columns=("Tipo", "Costo"))
        self.tabla_referencias.heading("Tipo", text="Tipo")
        self.tabla_referencias.heading("Costo", text="Costo")
        self.tabla_referencias.grid(row=4, column=0, columnspan=3, padx=20, pady=10)

        self.cargar_referencias()

    def cargar_referencias(self):
        # Limpiar tabla
        for row in self.tabla_referencias.get_children():
            self.tabla_referencias.delete(row)

        # Cargar datos desde la base de datos
        referencias = self.session.query(Habitacion).all()
        for referencia in referencias:
            self.tabla_referencias.insert("", "end", values=(referencia.tipo, referencia.costo))

    def guardar_referencia(self):
        tipo = self.tipo_entry.get()
        costo = self.costo_entry.get()

        if tipo and costo:
            try:
                costo = int(costo)
                nueva_referencia = Habitacion(tipo=tipo, costo=costo, dias_total=0, recaudacion_total=0)
                self.session.add(nueva_referencia)
                self.session.commit()
                self.cargar_referencias()
                tk_messagebox.showinfo("Éxito", "Tipo y costo de habitación guardados correctamente.")
            except ValueError:
                tk_messagebox.showerror("Error", "Por favor ingrese un costo válido (número entero).")
        else:
            tk_messagebox.showerror("Error", "Por favor complete ambos campos (Tipo y Costo).")

    def borrar_referencia(self):
        seleccion = self.tabla_referencias.focus()
        if seleccion:
            confirmacion = tk_messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas borrar esta referencia?")
            if confirmacion:
                tipo_referencia = self.tabla_referencias.item(seleccion)['values'][0]
                referencia = self.session.query(Habitacion).filter_by(tipo=tipo_referencia).first()
                if referencia:
                    self.session.delete(referencia)
                    self.session.commit()
                    self.cargar_referencias()
                    tk_messagebox.showinfo("Éxito", "Referencia borrada correctamente.")
                else:
                    tk_messagebox.showerror("Error", "Referencia no encontrada.")
        else:
            tk_messagebox.showerror("Error", "Por favor seleccione una referencia para borrar.")