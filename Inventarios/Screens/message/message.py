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

class file_message(ctk.CTkToplevel):
    '''Inicia un frame que se representa como una ventana emergente
    para indicarle al usuario que la ruta que ingresada o el archvo 
    seleccionado no es correcto, se sobrepone a todos los demás frames'''
    def __init__(self, parent, self_find):
        super().__init__(parent)
        self.geometry("600x60+600+200")
        self.configure(fg_color = style.GRAYBLACK)
        self.title("ADVERTENCIA")
        self.controller = self_find.controller
        self.label = ctk.CTkLabel(
            self,
            text = "La ruta ingresada es incorrecta o el archivo no es compatiple",
            **style.STYLELABEL
        )
        self.label.pack(padx=20, pady=20)
        self.attributes("-topmost",True)
        self.focus()
        self.focus_set()

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

class used_codinv_message(ctk.CTkToplevel):
    '''Inicia un frame que se representa como una ventana emergente
    para indicarle al usuario que el numero de caracteres que está ingresando
    es mayor al que es permitido'''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.geometry("500x60+800+300")
        self.configure(fg_color = style.GRAYBLACK)
        self.title("ADVERTENCIA")
        self.controller = controller
        self.label = ctk.CTkLabel(
            self,
            text = "El codigo de inventario ingresado ya existe",
            **style.STYLELABEL
        )
        self.label.pack(padx=20, pady=20)
        self.attributes("-topmost",True)
        self.focus()