#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk
#se importan las constantes que se usaran repetidamente en la creación del contenedor principal.
from constants import style
#Se importan las pantallas que se veran reflejeadas en el contenerdor.
from Screens.menu_login import menu_login
from Screens.menu_process import menu_process
from Screens.side_bar import side_bar
from Screens.menu_principal import menu_principal

class Manager(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Inventarios Tarjetas")
        container = ctk.CTkFrame(self)
        self.geometry("1100x580+125+80")
        container.pack(
            side = ctk.TOP,
            fill = ctk.BOTH,
            expand = True,
        )
        #color de fondo, numero y tamaño de las columnas
        container.grid_columnconfigure(0, weight=2)
        container.grid_columnconfigure(1, weight=10)
        container.grid_rowconfigure(0,weight=1)

        self.frames = {}
        for F in (side_bar, menu_login, menu_process,menu_principal):
            frame = F(container, self)
            if F == side_bar:    
                frame.grid(row = 0, column = 0, sticky = ctk.NSEW)
            else:
                frame.grid(row = 0, column = 1, sticky = ctk.NSEW)
            self.frames[F] = frame       
        self.show_frame(side_bar)

    def show_frame(self, window):
        frame = self.frames[window]
        frame.tkraise()