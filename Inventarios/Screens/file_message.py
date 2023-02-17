#se importan las librerias que nos permiten generar una interfaz grafica
import customtkinter as ctk
from constants import style

#Se importan valores constantes de nuestra aplicación
from constants import style

class file_message(ctk.CTkToplevel):
    def __init__(self, parent, self_find):
        super().__init__(parent)
        self.geometry("500x60+800+300")
        self.configure(fg_color = style.GRAYBLACK)
        self.title("ADVERTENCIA")
        self.controller = self_find.controller
        self.label = ctk.CTkLabel(
            self,
            text = "La ruta ingresada es incorrecta o el archivo no es compatiple",
            **style.STYLELABEL
        )
        self.label.pack(padx=20, pady=20)
        self.attributes("-topmost",True)
        self.focus()