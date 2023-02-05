#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk

#Se importan valores constantes de nuestra aplicación
from constants import style


#Se crean las diferentes pantallas
class Login(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        #self.configure(background = style.BACKGROUND)
        self.controller = controller

class Menu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        #self.configure(background = style.BACKGROUND)
        self.controller = controller