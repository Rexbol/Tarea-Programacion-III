import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import bcrypt
import os
from main import main
from db.db_conection import start_connection, User

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inicializar conexión a la base de datos
        self.session = start_connection()

        # Diseño de la GUI
        self.title("Sistema de Inicio de Sesión")
        self.geometry("300x200")

        tk.Label(self, text="Usuario").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Contraseña").grid(row=1, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self, show="*")

        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.register_button = tk.Button(self, text="Registrar", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def create_user(self, username, password):
        try:
            salt = bcrypt.gensalt()
            pepper = os.environ.get("PEPPER")
            if not pepper:
                raise ValueError("La variable de entorno PEPPER no está configurada")
            hashed_password = bcrypt.hashpw(password.encode() + pepper.encode(), salt)
            new_user = User(username=username, password=hashed_password.decode(), salt=salt.decode())
            self.session.add(new_user)
            self.session.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el usuario: {e}")

    def verify_login(self, username, password):
        try:
            user = self.session.query(User).filter_by(username=username).first()
            if user:
                pepper = os.environ.get("PEPPER")
                if not pepper:
                    raise ValueError("La variable de entorno PEPPER no está configurada")
                if bcrypt.checkpw(password.encode() + pepper.encode(), user.password.encode()):
                    return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar el inicio de sesión: {e}")
            return False

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.verify_login(username, password):
            messagebox.showinfo("Login", "¡Inicio de sesión exitoso!")
            self.cargar_main()
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            self.create_user(username, password)
            messagebox.showinfo("Registro", "¡Usuario creado exitosamente!")
        else:
            messagebox.showerror("Error", "Por favor, complete ambos campos")

    def config_ventana(self, subventana):
        subventana.transient(self)
        subventana.grab_set()
        self.wait_window(subventana)

    def cargar_main(self):
        main_window = main(self)
        self.config_ventana(main_window)

if __name__ == "__main__":
    app = App()
    app.mainloop()
