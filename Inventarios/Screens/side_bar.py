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
        active_btn_process = "disabled"
        self.controller = controller
        self.configure(fg_color= style.GRAY)
        self.init_widgets(active_btn_process)
    
    def set_login_frame(self):
            self.controller.show_frame(menu_login)
            self.bt_login.configure(**style.ALTER_BUTTONSTYLE)
            self.bt_procesar.configure(**style.BUTTONSTYLE)
            

    def set_process_frame(self):
            self.controller.show_frame(menu_process)
            self.bt_procesar.configure(**style.ALTER_BUTTONSTYLE)
            self.bt_login.configure(**style.BUTTONSTYLE)

    def init_widgets(self, active_btn_process):
        self.lb_tittle = ctk.CTkLabel(
            self,
            text = "INVENTARIOS",
            justify = ctk.CENTER,
            **style.STYLELABELTITLES
        )
        self.lb_tittle.pack(
            anchor = ctk.N,
            pady = 30
        )
        self.bt_login = ctk.CTkButton(
            self,
            text = "LOG IN",
            **style.BUTTONSTYLE,
            command= self.set_login_frame,
            corner_radius=0
        )
        self.bt_login.pack(
              fill = ctk.BOTH, 
              expand = True
        )
        self.bt_procesar = ctk.CTkButton(
            self,
            text = "PROCESAR",
            **style.BUTTONSTYLE,
            command= self.set_process_frame,
            corner_radius=0,
            state = active_btn_process
            )
        self.bt_procesar.pack(
              fill = ctk.BOTH, 
              expand = True,
              pady = (0,300)
              )   