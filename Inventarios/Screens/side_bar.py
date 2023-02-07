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
        button1_color = style.BUTTONSTYLE
        button2_color = style.BUTTONSTYLE
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=3)
        self.grid_rowconfigure(2,weight=3)
        self.grid_rowconfigure(3,weight=10)
        self.configure(fg_color= style.GRAY)
        self.init_widgets(button1_color, button2_color)
    
    def set_login_frame(self):
            self.controller.show_frame(menu_login)
            self.init_widgets(style.ALTER_BUTTONSTYLE,style.BUTTONSTYLE)
            

    def set_process_frame(self):
            self.controller.show_frame(menu_process)
            self.init_widgets(style.BUTTONSTYLE,style.ALTER_BUTTONSTYLE)

    def init_widgets(self, button1_style,button2_style):
        lb_tittle = ctk.CTkLabel(
            self,
            text = "INVENTARIOS",
            justify = ctk.CENTER,
            **style.STYLELABELTITLES
        )
        lb_tittle.grid(
            row = 0, 
            padx = 10,
            pady =10
            )
        
        flogin_option = ctk.CTkFrame(
              self, 
              corner_radius=0
              )
        flogin_option.grid(
              row = 1,
              column = 0, 
              sticky = ctk.NSEW
              )
        bt_login = ctk.CTkButton(
            flogin_option,
            text = "LOG IN",
            **button1_style,
            command= self.set_login_frame,
            corner_radius=0
        )
        bt_login.grid(
            row = 0, 
            padx = 10,
            pady = 10
        )
        bt_login.pack(
              fill = ctk.BOTH, 
              expand = True
              )
        
        fprocesar_option = ctk.CTkFrame(
              self, 
              corner_radius=0
              )
        fprocesar_option.grid(
              row = 2, 
              column = 0, 
              sticky = ctk.NSEW
              )
        bt_procesar = ctk.CTkButton(
            fprocesar_option,
            text = "PROCESAR",
            **button2_style,
            command= self.set_process_frame,
            corner_radius=0
            )
        bt_procesar.grid(
            row = 0, 
            padx = 10,
            pady = 10
            ) 
        bt_procesar.pack(
              fill = ctk.BOTH, 
              expand = True
              )   