import tkinter as tk

from ventanas.cargar_estadías import cargar_estadías
from ventanas.cargar_referencias import cargar_referencias
from ventanas.visualizar_ingresos import visualizar_ingresos
from ventanas.formulario_regiestro_user import registrar_user

class MainApp(tk.Tk):
    def __init__(self, user_role, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_role = user_role

        self.title("Sistema de Gestión")
        self.geometry_config()

        # Configurar las columnas para que se expandan
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Crear botones para abrir diferentes formularios
        self.boton_cargar_referencias = tk.Button(
            self, text="Cargar Referencias", command=self.abrir_formulario_referencias
        )
        self.boton_cargar_referencias.grid(
            row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10
        )

        self.boton_cargar_estadias = tk.Button(
            self, text="Cargar Estadías", command=self.abrir_formulario_estadias
        )
        self.boton_cargar_estadias.grid(
            row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10
        )

        self.boton_visualizar_ingresos = tk.Button(
            self, text="Visualizar Ingresos", command=self.abrir_formulario_ingresos
        )
        self.boton_visualizar_ingresos.grid(
            row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=10
        )

        #! Mostrar el botón "Registrar Usuarios" solo si el rol del usuario es "admin"
        if self.user_role == "admin":
            self.boton_registrar_usuario = tk.Button(
                self, text="Registrar Usuarios", command=self.abrir_formulario_registro
            )
            self.boton_registrar_usuario.grid(
                row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=10
            )

    def configurar_ventana(self, ventana):
        ventana.transient(self)
        ventana.grab_set()
        self.wait_window(ventana)

    def geometry_config(self):
        if self.user_role == "admin":
            self.geometry("250x190")
            return
        self.geometry("250x140")

    def abrir_formulario_referencias(self):
        ventana_referencias = cargar_referencias(self)
        self.configurar_ventana(ventana_referencias)

    def abrir_formulario_estadias(self):
        ventana_estadias = cargar_estadías(self)
        self.configurar_ventana(ventana_estadias)

    def abrir_formulario_ingresos(self):
        ventana_ingresos = visualizar_ingresos(self)
        self.configurar_ventana(ventana_ingresos)

    def abrir_formulario_registro(self):
        ventana_registro = registrar_user(self)
        self.configurar_ventana(ventana_registro)

if __name__ == "__main__":
    app = MainApp(user_role="default")  # Este valor solo es un ejemplo
    app.mainloop()
