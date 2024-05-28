import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import bcrypt
import os

from main import main

engine = create_engine('mysql+pymysql://root@localhost/ejemplo')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    salt = Column(String(64), nullable=False)
    
Base.metadata.create_all(engine)

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tk.Label(self, text="Usuario").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Contraseña").grid(row=1, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self, show="*")

        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = tk.Button(self, text="Login", command=login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.register_button = tk.Button(self, text="Registrar", command=register)
        self.register_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def create_user(username, password):
        salt = bcrypt.gensalt()
        pepper = os.environ.get("PEPPER", "default_pepper")
        hashed_password = bcrypt.hashpw(password.encode() + pepper.encode(), salt)
        new_user = User(username=username, password=hashed_password.decode(), salt=salt.decode())
        session.add(new_user)
        session.commit()

    def verify_login(username, password):
        user = session.query(User).filter_by(username=username).first()
        if user:
            pepper = os.environ.get("PEPPER", "default_pepper")
            if bcrypt.checkpw(password.encode() + pepper.encode(), user.password.encode()):
                return True
        return False

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.verify_login(username, password):
            messagebox.showinfo("Login", "Login exitoso!")
            self.cargar_main()
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            self.create_user(username, password)
            messagebox.showinfo("Registro", "Usuario creado exitosamente!")
        else:
            messagebox.showerror("Error", "Por favor, complete ambos campos")
            
    def config_ventana(self, subventana):
        subventana.transient(self)
        subventana.grab_set()
        self.wait_window(subventana)
        
    def cargar_main(self):
        cargar_main = main(self) 
        self.config_ventana(cargar_main)
    

if __name__ == "__login__":
    app = App()
    app.mainloop()