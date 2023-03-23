#se importan las librerias que nos permiten generar una interfaz grafica
import customtkinter as ctk
from constants import style

#Se importan valores constantes de nuestra aplicación
from constants import style

class login_message(ctk.CTkToplevel):
    '''Inicia un frame que se representa como una ventana emergente
    para indicar que el ingreso fue exitoso o que los datos ingresados son
    erroneos.'''
    def __init__(self, parent, controller,case):
        super().__init__(parent)
        self.geometry("500x60+800+300")
        self.configure(fg_color = style.GRAYBLACK)
        self.title("ADVERTENCIA")
        self.controller = controller
        if case:
            self.label = ctk.CTkLabel(
                self,
                text = "Ingreso exitoso",
                **style.STYLELABEL
            )
        else:
            self.label = ctk.CTkLabel(
                self,
                text = "Su contraseña y/o usuario son incorrectos \nrecuerde que si se equivoca más de una vez, su usuario será bloqueado",
                **style.STYLELABEL
            )
        self.label.pack(padx=20, pady=20)
        self.attributes("-topmost",True)
        self.focus()
class width_message(ctk.CTkToplevel):
    '''Inicia un frame que se representa como una ventana emergente
    para indicarle al usuario que el numero de caracteres que está ingresando
    es mayor al que es permitido'''
    def __init__(self, parent, controller,entry: str,width: int):
        super().__init__(parent)
        self.geometry("500x60+800+300")
        self.configure(fg_color = style.GRAYBLACK)
        self.title("ADVERTENCIA")
        self.controller = controller
        self.label = ctk.CTkLabel(
            self,
            text = "EL numero de caracteres maximos en {} es de {},\npor favor verifique".format(entry,width),
            **style.STYLELABEL
        )
        self.label.pack(padx=20, pady=20)
        self.attributes("-topmost",True)
        self.focus()

class alert_message(ctk.CTkToplevel):
    '''Inicia un frame que se representa como una ventana emergente
    para indicarle al usuario que el codigo de inventario ya existe'''
    def __init__(self, parent, controller, message: str):
        super().__init__(parent)
        self.geometry("600x120+800+300")
        self.configure(fg_color = style.GRAYBLACK)
        self.title("ADVERTENCIA")
        self.controller = controller
        self.label = ctk.CTkLabel(
            self,
            text = message,
            **style.STYLELABEL
        )
        self.label.pack(padx=20, pady=20)
        self.attributes("-topmost",True)
        self.focus()

class confirm_message(ctk.CTkToplevel):
    '''Inicia un frame que se representa como una ventana emergente
    para preguntarle al usuario si está seguro de continuar con la acción elegida'''
    def __init__(self, parent, controller, message: str):
        super().__init__(parent)
        self.geometry("700x100+450+400")
        self.configure(fg_color = style.GRAYBLACK)
        self.title("ADVERTENCIA")
        self.controller = controller
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0,weight=2)
        self.grid_rowconfigure(1,weight=1)            

        self.label = ctk.CTkLabel(
            self,
            text = message,
            **style.STYLELABEL
        )
        self.label.grid(
            row = 0, 
            column = 0, 
            columnspan = 2, 
            sticky = ctk.NSEW
        )
        self.attributes("-topmost",True)
        self.focus()
        #Botón Sí
        self.bt_search = ctk.CTkButton(
            self,
            **style.SMALLBUTTONSTYLE,
            text = "Sí",
            command = self.si,
            width= 90
        )
        self.bt_search.grid(
            row = 1,
            column = 0,
            sticky = ctk.NSEW
        )
        #Botón No
        self.bt_search = ctk.CTkButton(
            self,
            **style.SMALLBUTTONSTYLE,
            text = "NO",
            command = self.no,
            width= 90
        )
        self.bt_search.grid(
            row = 1,
            column = 1,
            sticky = ctk.NSEW
        )
        parent.wait_window(self)
    
    def si(self):
        """Cambia el estado de la variable continuar a True y cierra el mensaje"""
        self.parent.cfm = True
        self.destroy()
    def no(self):
        """Cambia el estado de la variable continuar a False y cierra el mensaje"""
        self.parent.cfm = False
        self.destroy()
