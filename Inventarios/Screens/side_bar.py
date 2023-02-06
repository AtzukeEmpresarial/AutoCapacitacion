#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk

#Se importan valores constantes de nuestra aplicación
from constants import style
from Screens.menu_login import menu_login
from Screens.menu_process import menu_process


#Se crean las diferentes pantallas
class side_bar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        #self.configure(fg_color = style.BACKGROUND)
        side_bar_color = style.SIDE_BAR_COLOR
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4,weight=1)
        self.init_widgets(side_bar_color)
    
    def set_login_frame(self):
            self.controller.show_frame(menu_login)
            style.SIDE_BAR_COLOR = "#FFFFFF"

    def set_process_frame(self):
            self.controller.show_frame(menu_process)

    def init_widgets(self, side_bar_color):
        lb_tittle = ctk.CTkLabel(
            self,
            text = "INVENTARIOS",
            justify = ctk.CENTER,
            **style.STYLELABELTITLES
        )
        lb_tittle.grid(
            row = 0, 
            padx = 20,
            pady =(20,10)
            )
        flogin_option = ctk.CTkFrame(self, corner_radius=0)
        flogin_option.grid(row = 2, column = 0, sticky = ctk.NSEW)
        bt_login = ctk.CTkButton(
            flogin_option,
            text = "LOG IN",
            **style.STYLELABELTITLES,
            fg_color = side_bar_color,
            hover =True,
            command= self.set_login_frame,
        )
        bt_login.grid(
            row = 0, 
            padx = 20,
            pady = 20
        )
        bt_login.pack(fill = ctk.BOTH, expand = True)
        fprocesar_option = ctk.CTkFrame(self, corner_radius=0)
        fprocesar_option.grid(row = 3, column = 0, sticky = ctk.NSEW)
        bt_procesar = ctk.CTkButton(
            fprocesar_option,
            text = "PROCESAR",
            **style.STYLELABELTITLES,
            hover =True,
            command= self.set_process_frame
        )
        bt_procesar.grid(
            row = 0, 
            padx = 20,
            pady = 20
        ) 
        bt_procesar.pack(fill = ctk.BOTH, expand = True)   