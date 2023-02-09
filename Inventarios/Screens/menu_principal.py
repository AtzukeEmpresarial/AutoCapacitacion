#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk
from PIL import Image
import os

#Se importan valores constantes de nuestra aplicación
from constants import style

class menu_principal(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color = style.GRAYBLACK)
        self.controller = controller
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for j in range(3):
            self.grid_rowconfigure(j,weight=1)
        self.init_text()
        self.init_bg_img()
    
    def init_bg_img(self):
        bancolombia_trace1 = Image.open("Inventarios/Resources/Trazos.png")
        size = (400,400)
        ctk_img_bancolombia = ctk.CTkImage(bancolombia_trace1, size = size)
        lb_image = ctk.CTkLabel(
            self,
            image= ctk_img_bancolombia,
            text= ""
        )
        lb_image.grid(
            column =   1,
            row = 2, 
            columnspan = 3,
            padx = 0,
            pady =(0,60)
        )
    
    def init_text(self):
        lb_tittle = ctk.CTkLabel(
            self,
            text = "Bienvenido",
            justify = ctk.CENTER,
            **style.STYLELABELTITLES
        )
        lb_tittle.grid(
            column = 1,
            row = 1, 
            padx = 10,
            pady =10
            )
        lb_subtext = ctk.CTkLabel(
            self,
            text = "Recuerde tener de manera local todos los documentos necesarios para alimentar el inventario",
            justify = ctk.CENTER,
            **style.STYLELABEL
        )
        lb_subtext.grid(
            column = 1,
            row = 1, 
            padx = 10,
            pady =(60,0)
            )
        