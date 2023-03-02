#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk
from tksheet import Sheet
import pandas as pd

#Se importan valores constantes de nuestra aplicación
from constants import style
from Functions import ODBC

class menu_parameters(ctk.CTkFrame):
    """
    Clase encargada de la alimentación y proceso de datos,
    este contiene diferentes pestañas para los distintos pasos del
    proceso
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color = style.GRAYBLACK)
        self.controller = controller
        self.init_tabview()

    def init_tabview(self):
        """
        Inicia el widget de pestañas, este contiene los diferentes procesos de datos
        """
        self.tab_parametros = ctk.CTkTabview(
            self,
            segmented_button_selected_hover_color = style.BLUE,
            segmented_button_selected_color= style.DARKBLUE
        )
        self.tab_parametros.pack(
            anchor = ctk.N,
            padx=20, 
            pady=20, 
            fill = ctk.BOTH,
            expand = True
        )
        self.tab1 = "Creación de plastico"
        self.tab2 = "Por definir"
        self.tab_parametros.add(self.tab1)
        self.tab_parametros.add(self.tab2)
        self.tab_parametros.set(self.tab1)