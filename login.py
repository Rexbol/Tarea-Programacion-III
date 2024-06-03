import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import bcrypt
import os
from dotenv import load_dotenv
from main import MainApp
from db.db_conection import start_connection, User

#! Cargar variables de entorno desde el archivo .env
load_dotenv()
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #! Inicializar conexión a la base de datos
        self.session = start_connection()

        #! Diseño de la GUI
        self.title("Sistema de Inicio de Sesión")
        self.geometry("400x300")  #? Aumentar el tamaño de la ventana para acomodar los widgets más grandes

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        tk.Label(self, text="Usuario").grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipady=10, sticky="ew")  # Aumentar la altura de la entrada

        tk.Label(self, text="Contraseña").grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipady=10, sticky="ew")  # Aumentar la altura de la entrada

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, ipady=10, sticky="ew")  # Aumentar la altura del botón

    def verify_login(self, username, password):
        try:
            user = self.session.query(User).filter_by(username=username).first()
            if user:
                pepper = os.environ.get("PEPPER")
                if not pepper:
                    raise ValueError("La variable de entorno PEPPER no está configurada")
                if bcrypt.checkpw(password.encode() + pepper.encode(), user.password.encode()):
                    return user.role
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar el inicio de sesión: {e}")
            return False

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_role = self.verify_login(username, password)
        if user_role:
            messagebox.showinfo("Login", "¡Inicio de sesión exitoso!")
            self.destroy()  #! Cerrar la ventana de inicio de sesión
            self.cargar_main(user_role)
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

    def cargar_main(self, user_role):
        print(user_role)
        main_window = MainApp(user_role=user_role)  # Pasar user_role al constructor
        main_window.mainloop()  # Iniciar el bucle principal de la nueva ventana

if __name__ == "__main__":
    app = App()
    app.mainloop()
