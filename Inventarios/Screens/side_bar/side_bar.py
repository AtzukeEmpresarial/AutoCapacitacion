#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk

#Se importan valores constantes de nuestra aplicación
from constants import style
from Screens.menu_login.menu_login import menu_login
from Screens.menu_process.menu_process import menu_process
from Screens.menu_parameters.menu_parameters import menu_parameters
from Screens.menu_principal.menu_principal import menu_principal
from Screens.menu_informes.menu_informes import menu_informes


class side_bar(ctk.CTkFrame):
    """
    Clase que se encarga crear la barra lateral izquierda 
    y contener los diferentes widgets.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        active_btn_process = "disabled" #Controla si el botón de proceso está activo, cambiar según convenga el desarrollo
        self.controller = controller
        self.configure(fg_color= style.GRAY)
        self.init_widgets(active_btn_process)
    
    
    def set_login_frame(self):
        """
        Trae al frente el frame de login, resalta el botón de login 
        y vuelve a la normalidad los demás botones.
        """
        #self.controller.show_frame(menu_login)

        self.frame_login = menu_login(self.controller.container,self.controller)
        self.frame_login.grid(row = 0, column = 1, sticky = ctk.NSEW)

        self.bt_login.configure(**style.ALTER_BUTTONSTYLE)
        self.bt_informes.configure(**style.BUTTONSTYLE)
        self.bt_informes.configure(font = style.FONTTITLES2)
        self.bt_procesar.configure(**style.BUTTONSTYLE)
        self.bt_procesar.configure(font = style.FONTTITLES2)
        self.bt_params.configure(**style.BUTTONSTYLE)
        self.bt_params.configure(font = style.FONTTITLES2)
            

    def set_process_frame(self):
        """
        Trae al frente el frame de alimentar inventarios, 
        resalta el botón de alimentar inventarios 
        y vuelve a la normalidad los demás botones.
        """
        #self.controller.show_frame(menu_process)

        if menu_parameters in self.controller.frames:
            self.frame_param.destroy()
            del self.controller.frames[menu_parameters]
        if menu_informes in self.controller.frames:
            self.frame_param.destroy()
            del self.controller.frames[menu_informes]

        self.frame_process = menu_process(self.controller.container,self.controller)
        self.frame_process.grid(row = 0, column = 1, sticky = ctk.NSEW)
        self.controller.frames[menu_process] = self.frame_process
        
        self.bt_procesar.configure(**style.ALTER_BUTTONSTYLE)
        self.bt_procesar.configure(font = style.FONTTITLES2)
        self.bt_informes.configure(**style.BUTTONSTYLE)
        self.bt_informes.configure(font = style.FONTTITLES2)
        self.bt_login.configure(**style.BUTTONSTYLE)
        self.bt_params.configure(**style.BUTTONSTYLE)
        self.bt_params.configure(font = style.FONTTITLES2)
    
    def set_param_frame(self):
        """
        Trae al frente el frame de parametros, 
        resalta el botón de alimentar inventarios 
        y vuelve a la normalidad los demás botones.
        """
        #self.controller.show_frame(menu_parameters)
        
        if menu_process in self.controller.frames:
            self.frame_process.destroy()
            del self.controller.frames[menu_process]
        if menu_informes in self.controller.frames:
            self.frame_param.destroy()
            del self.controller.frames[menu_informes]

        self.frame_param = menu_parameters(self.controller.container,self.controller)
        self.frame_param.grid(row = 0, column = 1, sticky = ctk.NSEW)
        self.controller.frames[menu_parameters] = self.frame_param
  
        self.bt_params.configure(**style.ALTER_BUTTONSTYLE)
        self.bt_params.configure(font = style.FONTTITLES2)
        self.bt_informes.configure(**style.BUTTONSTYLE)
        self.bt_informes.configure(font = style.FONTTITLES2)
        self.bt_login.configure(**style.BUTTONSTYLE)
        self.bt_procesar.configure(**style.BUTTONSTYLE)
        self.bt_procesar.configure(font = style.FONTTITLES2)
    
    def set_informes_frame(self):
        """
        Trae al frente el frame de informes, 
        resalta el botón de informes y vuelve a la normalidad los demás botones.
        """
        #self.controller.show_frame(menu_parameters)
        if menu_process in self.controller.frames:
            self.frame_process.destroy()
            del self.controller.frames[menu_process]
        if menu_parameters in self.controller.frames:
            self.frame_param.destroy()
            del self.controller.frames[menu_parameters]
        
        self.frame_param = menu_informes(self.controller.container,self.controller)
        self.frame_param.grid(row = 0, column = 1, sticky = ctk.NSEW)
        self.controller.frames[menu_informes] = self.frame_param

        self.bt_informes.configure(**style.ALTER_BUTTONSTYLE)
        self.bt_informes.configure(font = style.FONTTITLES2)
        self.bt_params.configure(**style.BUTTONSTYLE)
        self.bt_params.configure(font = style.FONTTITLES2)
        self.bt_login.configure(**style.BUTTONSTYLE)
        self.bt_procesar.configure(**style.BUTTONSTYLE)
        self.bt_procesar.configure(font = style.FONTTITLES2)

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
        if active_btn_process == "normal":
            state_bt_login = "diabled"
        else:
            state_bt_login = "normal"
        self.bt_login = ctk.CTkButton(
            self,
            text = "Ingresar",
            **style.BUTTONSTYLE,
            command= self.set_login_frame,
            corner_radius=0,
            state = state_bt_login
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
              expand = True
              )
        #botón definir parametros
        self.bt_params = ctk.CTkButton(
            self,
            text = "Parametros",
            **style.BUTTONSTYLE,
            command= self.set_param_frame,
            corner_radius=0,
            state = active_btn_process
            )
        self.bt_params.configure(font = style.FONTTITLES2)
        self.bt_params.pack(
              fill = ctk.BOTH, 
              expand = True,
              )
        #botón definir parametros
        self.bt_informes = ctk.CTkButton(
            self,
            text = "Informes",
            **style.BUTTONSTYLE,
            command= self.set_informes_frame,
            corner_radius=0,
            state = active_btn_process
        )
        self.bt_informes.configure(font = style.FONTTITLES2)
        self.bt_informes.pack(
              fill = ctk.BOTH, 
              expand = True,
              pady = (0,200)
        )  
    #Label que indica el usuario que está activo en el sistema   
    def init_user(self):
        self.lb_user = ctk.CTkLabel(
            self,
            **style.STYLELABEL,
            justify = ctk.CENTER,
            text = self.controller.user
        ).pack(
            anchor = ctk.S
        )