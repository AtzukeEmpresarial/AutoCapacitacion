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
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4,weight=1)
        self.init_widgets()
    
    def set_login_frame(self):
            self.controller.show_frame(MenuLog)

    def init_widgets(self):
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
        lb_login = ctk.CTkButton(
            flogin_option,
            text = "lOG IN",
            **style.STYLELABELTITLES,
            hover =True,
            command= self.set_login_frame()
        )
        lb_login.grid(
            row = 0, 
            padx = 20,
            pady = 20
            )
        fprocesar_option = ctk.CTkFrame(self, corner_radius=0)
        fprocesar_option.grid(row = 3, column = 0, sticky = ctk.NSEW)
        lb_procesar = ctk.CTkLabel(
            fprocesar_option,
            text = "PROCESAR",
            justify = ctk.CENTER,
            **style.STYLELABELTITLES
        )
        lb_procesar.grid(
            row = 0, 
            padx = 20,
            pady = 20
            )     

class MenuLog(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color = style.BACKGROUND)
        self.controller = controller

class Process(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color = "#FFFFFF")
        self.controller = controller
     



