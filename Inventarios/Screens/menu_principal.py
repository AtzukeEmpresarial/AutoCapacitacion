#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk
from PIL import Image
import os

#Se importan valores constantes de nuestra aplicación
from constants import style

class menu_principal(ctk.CTkFrame):
    """
    Frame de bienvenida, es el primero en enseñarce al iniciar el script.
    """
    def __init__(self, parent, controller):
        """
        Inicia el Frame de bievenida (Principal).
        """
        super().__init__(parent)
        self.configure(fg_color = style.GRAYBLACK)
        self.controller = controller
        self.init_text()
        self.init_bg_img()
    
    def init_text(self):
        """
        Inicia los widgets de texto.
        """
        lb_tittle = ctk.CTkLabel(
            self,
            text = "Bienvenido",
            justify = ctk.CENTER,
            **style.STYLELABELTITLES
        )
        lb_tittle.pack(
            anchor = ctk.N,
            pady = (30,15)
        )
        lb_subtext = ctk.CTkLabel(
            self,
            text = "Recuerde tener de manera local todos los documentos \nnecesarios para alimentar el inventario",
            justify = ctk.CENTER,
            **style.STYLELABEL
        )
        lb_subtext.pack(
            anchor = ctk.N
        )
    
    def init_bg_img(self):
        """
        Inicia el widget de la imagen.
        """
        bancolombia_trace1 = Image.open("Inventarios/Resources/Trazos.png")
        size = (400,400)
        ctk_img_bancolombia = ctk.CTkImage(bancolombia_trace1, size = size)
        lb_image = ctk.CTkLabel(
            self,
            image= ctk_img_bancolombia,
            text= ""
        )
        lb_image.pack(
            anchor = ctk.N
        )
        