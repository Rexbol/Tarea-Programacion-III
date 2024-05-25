import tkinter as tk
import customtkinter as ctk

from ventanas.cargar_referencias import cargar_referencias
from ventanas.cargar_estadías import cargar_estadías
from ventanas.visualizar_ingresos import visualizar_ingresos
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Ventanas")

        #! Crear el botón del Primer Formulario:
        self.mostrar_primer_formulario = tk.Button(
            self, text="Cargar Referencias", command=self.primer_formulario
        )
        self.mostrar_primer_formulario.grid(
            row=0, column=0, columnspan=3, padx=10, pady=10
        )

        #! Crear el botón del Segundo Formulario:
        self.mostrar_segundo_formulario = tk.Button(
            self, text="Cargar Estadias", command=self.segundo_formulario
        )
        self.mostrar_segundo_formulario.grid(
            row=1, column=0, columnspan=3, padx=10, pady=10
        )

        #! Crear el botón del Tercer Formulario:
        self.mostrar_tercer_formulario = tk.Button(
            self, text="Visualizar Ingresos", command=self.tercer_formulario
        )
        self.mostrar_tercer_formulario.grid(
            row=2, column=0, columnspan=3, padx=10, pady=10
        )

    def config_ventana(self, subventana):
        subventana.transient(self)
        subventana.grab_set()
        self.wait_window(subventana)

    def primer_formulario(self):
        ventana_referencia = cargar_referencias(self) 
        self.config_ventana(ventana_referencia)

    def segundo_formulario(self):
        ventana_estadias = cargar_estadías(self) 
        self.config_ventana(ventana_estadias)

    def tercer_formulario(self):
        ventana_ingresos = visualizar_ingresos(self) 
        self.config_ventana(ventana_ingresos)



if __name__ == "__main__":
    app = App()
    app.mainloop()