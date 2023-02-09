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
        self.init_log()

    def check (self):
        connection_state = check_credentials.check_credentials(self.et_user.get(), self.et_pass.get())
        self.login_message = login_message(self, self.controller,connection_state)
   
    def init_log (self):
        flog = ctk.CTkFrame(
            self,
            fg_color = style.GRAY,
            border_width = 2,
            border_color=style.WHITE
        )
        flog.place(
            relx=0.29,
            rely=0.23,
            relwidth = 0.4,
            relheight = 0.5
        )
        self.lb_user = ctk.CTkLabel(
            flog,
            text = "Imagen.png",
            **style.STYLELABELTITLES2,
            justify = ctk.CENTER
        )
        self.lb_user.pack(
            anchor = ctk.N,
            pady = 30
        )
        self.et_user = ctk.CTkEntry(
            flog,
            placeholder_text = "USUARIO"  
        )
        self.et_user.pack(
            anchor = ctk.N,
            pady = 20,
            fill = "x",
            padx = (20,20)
        )
        self.et_pass = ctk.CTkEntry(
            flog,
            placeholder_text = "CONTRASEÑA"  
        )
        self.et_pass.pack(
            anchor = ctk.N,
            fill = "x",
            pady = 10,
            padx = (20,20)
        )         
        self.bt_log = ctk.CTkButton(
            flog,
            text = "INGRESAR",
            **style.REALBUTTONSTYLE,
            command= self.check,
        )
        self.bt_log.pack(
            anchor = ctk.N,
            pady = 15
        )
        

        

        
        
