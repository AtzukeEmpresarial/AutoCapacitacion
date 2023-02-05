#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk
#se importan las constantes que se usaran repetidamente en la creación del contenedor principal.
from constants import style
#Se importan las pantallas que se veran reflejeadas en el contenerdor.
from screen import Login, Menu

class Manager(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Inventarios Tarjetas")
        container = ctk.CTkFrame(self)
        container.pack(
            side = ctk.TOP,
            fill = ctk.BOTH,
            expand = True,
        )
        #color de fondo, numero y tamaño de las columnas
        container.configure(background= style.BACKGROUND)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0,weight=1)

        self.frames = {}
        for F in (Login, Menu):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = ctk.NSEW)
        self.show_frame(Login)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise