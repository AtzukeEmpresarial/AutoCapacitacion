#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk


#Se importan valores constantes de nuestra aplicación
from constants import style
from Screens.menu_login import menu_login
from Screens.menu_process import menu_process



class side_bar(ctk.CTkFrame):
    """
    Clase que se encarga crear la barra lateral izquierda 
    y contener los diferentes widgets.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        active_btn_process = "normal" #CAMBIARLO AL FINALIZAR EL FRAME
        self.controller = controller
        self.configure(fg_color= style.GRAY)
        self.init_widgets(active_btn_process)
    
    def set_login_frame(self):
            """
            Trae al frente el frame de login, resalta el botón de login 
            y vuelve a la normalidad los demás botones.
            """
            self.controller.show_frame(menu_login)
            self.bt_login.configure(**style.ALTER_BUTTONSTYLE)
            self.bt_procesar.configure(**style.BUTTONSTYLE)
            self.bt_procesar.configure(font = style.FONTTITLES2)
            

    def set_process_frame(self):
            """
            Trae al frente el frame de alimentar inventarios, 
            resalta el botón de alimentar inventarios 
            y vuelve a la normalidad los demás botones.
            """
            self.controller.show_frame(menu_process)
            self.bt_procesar.configure(**style.ALTER_BUTTONSTYLE)
            self.bt_procesar.configure(font = style.FONTTITLES2)
            self.bt_login.configure(**style.BUTTONSTYLE)

    def init_widgets(self, active_btn_process):
        """
        Inicia todos los widgets y frames contenidos en la barra lateral y recibe:
        active_btn_process = define el estado de actividad de el botón de alimentar inventario.
        """
        #botón del titulo
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
        #botón de ingreso
        self.bt_login = ctk.CTkButton(
            self,
            text = "Ingresar",
            **style.BUTTONSTYLE,
            command= self.set_login_frame,
            corner_radius=0
        )
        self.bt_login.pack(
              fill = ctk.BOTH, 
              expand = True
        )
        #botón de alimentar inventario
        self.bt_procesar = ctk.CTkButton(
            self,
            text = "Alimentar Inventario",
            **style.BUTTONSTYLE,
            command= self.set_process_frame,
            corner_radius=0,
            state = active_btn_process
            )
        self.bt_procesar.configure(font = style.FONTTITLES2)
        self.bt_procesar.pack(
              fill = ctk.BOTH, 
              expand = True,
              pady = (0,300)
              )   