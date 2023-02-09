#se importan las librerias que nos permiten generar una interfaz grafica
import customtkinter as ctk
from constants import style

#Se importan valores constantes de nuestra aplicación
from constants import style

class login_message(ctk.CTkToplevel):
    def __init__(self, parent, controller,case):
        super().__init__(parent)
        self.geometry("500x60+800+300")
        self.configure(fg_color = style.GRAYBLACK)
        self.title("ADVERTENCIA")
        self.controller = controller
        if case:
            self.label = ctk.CTkLabel(
                self,
                text= "Ingreso exitoso",
                **style.STYLELABEL
            )
        else:
            self.label = ctk.CTkLabel(
                self,
                text= "Su contraseña y/o usuario son incorrectos",
                **style.STYLELABEL
            )
        self.label.pack(padx=20, pady=20)
        self.attributes("-topmost",True)
        self.focus()