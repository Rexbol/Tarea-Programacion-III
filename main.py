import tkinter as tk

from ventanas.cargar_referencias import CargarReferencias
from ventanas.cargar_estadias import CargarEstadias
from ventanas.visualizar_ingresos import visualizar_ingresos
from ventanas.formulario_registro_usuario import formulario_registro_usuario


import tkinter as tk

class MainApplication(tk.Tk):
    def __init__(self, user_role, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_role = user_role

        self.title("Sistema de Gestión")
        self.configure_geometry()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.create_buttons()

    def configure_geometry(self):
        if self.user_role == "admin":
            self.geometry("250x190")
        else:
            self.geometry("250x140")

    def create_buttons(self):
        button_texts = ["Cargar Referencias", "Cargar Estadías", "Visualizar Ingresos"]
        commands = [self.open_reference_form, self.open_stay_form, self.open_income_form]
        
        if self.user_role == "admin":
            button_texts.append("Registrar Usuario")
            commands.append(self.open_registration_form)

        for i, (text, command) in enumerate(zip(button_texts, commands)):
            button = tk.Button(self, text=text, command=command)
            button.grid(row=i, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

    def open_window(self, window):
        window.transient(self)
        window.grab_set()
        self.wait_window(window)

    def open_reference_form(self):
        reference_window = CargarReferencias(self)
        self.open_window(reference_window)

    def open_stay_form(self):
        stay_window = CargarEstadias(self)
        self.open_window(stay_window)

    def open_income_form(self):
        income_window = visualizar_ingresos(self)
        self.open_window(income_window)

    def open_registration_form(self):
        registration_window = formulario_registro_usuario(self)
        self.open_window(registration_window)

if __name__ == "__main__":
    app = MainApplication(user_role="default")
    app.mainloop()
