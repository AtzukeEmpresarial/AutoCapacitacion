#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk

#Se importan valores constantes de nuestra aplicación
from constants import style


#Se crean las diferentes pantallas
class Login(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        #self.configure(fg_color = style.BACKGROUND)
        self.controller = controller
        self.init_widgets()
    
    def init_widgets(self):
        ctk.CTkLabel(
            self,
            text = "Login",
            justify = ctk.CENTER,
            **style.STYLE
        ).pack(
            side = ctk.CENTER,
            fill = ctk.BOTH,
            expand = True,
            padx = 22,
            pady = 11
        )

class Menu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        #self.configure(fg_color = style.BACKGROUND)
        self.controller = controller