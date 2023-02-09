#se importan las librerias que nos permiten generar una interfaz grafica
import customtkinter as ctk
from constants import style

#Se importan valores constantes de nuestra aplicación
from constants import style

#se importan otras clases necesarias
from Functions import check_credentials
from Screens.login_message import login_message

class menu_login(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color = style.GRAYBLACK)
        self.controller = controller
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for j in range(3):
            self.grid_rowconfigure(j,weight=1)
        self.init_log()

    def check (self):
        connection_state = check_credentials.check_credentials(self.et_user.get(), self.et_pass.get())
        self.login_message = login_message(self, self.controller,connection_state)
   
    def init_log (self):
        flog = ctk.CTkFrame(
            self,
            fg_color = style.LIGHTGRAY
        )
        flog.grid_columnconfigure(0,weight=1)
        flog.grid_rowconfigure(0,weight=1)
        flog.grid(
            row = 1,
            column = 1,
            sticky = ctk.NSEW,
            padx = 200,
            pady = 20
        )
        self.lb_user = ctk.CTkLabel(
            flog,
            text = "USUARIO",
            **style.STYLELABELTITLES2
        )
        self.lb_user.grid(
            padx= 0,
            pady =0
        )
        self.et_user = ctk.CTkEntry(
            flog,
            placeholder_text = "USUARIO"  
        )
        self.et_user.grid(
            padx = 10,
            pady = (0,15),
            sticky = ctk.EW
        )
        self.et_pass = ctk.CTkEntry(
            flog,
            placeholder_text = "CONTRASEÑA"  
        )
        self.et_pass.grid(
            padx = 10,
            pady = (0,0),
            sticky = ctk.EW
        )            
        self.bt_log = ctk.CTkButton(
            flog,
            text = "INGRESAR",
            **style.REALBUTTONSTYLE,
            command= self.check,
        )
        self.bt_log.grid(
            padx = 0,
            pady = (30,10)
        )
        

        

        
        
