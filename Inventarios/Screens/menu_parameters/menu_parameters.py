#se importan las librerias que nos permiten generar una interfaz grafica
import customtkinter as ctk
import pandas as pd
import datetime as dt
import pyodbc

#Se importan valores constantes de nuestra aplicación
from constants import style
from Functions import DBC,validations
from Screens.menu_parameters.plasticos import plastico,insert,next, previous, clean, search_by_codinv

class menu_parameters(ctk.CTkFrame):
    fecha = dt.date.today()
    ids_plasticos = []
    """
    Clase que ejecuta el frame para la parametrización y creación de datos
    importantes para el sistema.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color = style.GRAYBLACK)
        self.controller = controller
        #conexión que usara esta pantalla
        self.cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID={};PWD={}'.format(controller.user, controller.password), autocommit=True )
        #Inicio de los widgets
        self.init_tabview()

    def insert_con(self):
        insert(self)
    def next_con(self):
        next(self)
    def previous_con(self):
        previous(self)
    def clean_con(self):
        clean(self)
    def search_by_codinv_con(self):
        search_by_codinv(self)
    

    def init_tabview(self):
        """
        Inicia el widget de pestañas, este contiene los diferentes
        procesos de parametrizacion.
        """
        self.tab_parametros = ctk.CTkTabview(
            self,
            segmented_button_selected_hover_color = style.BLUE,
            segmented_button_selected_color= style.DARKBLUE
        )
        self.tab_parametros.pack(
            anchor = ctk.N,
            padx=20, 
            pady=20, 
            fill = ctk.BOTH,
            expand = True
        )
        self.tab1 = "Plastico"
        self.tab2 = "Plantas"
        self.tab3 = "Por definir"
        self.tab_parametros.add(self.tab1)
        self.tab_parametros.add(self.tab2)
        self.tab_parametros.add(self.tab3)
        self.tab_parametros.set(self.tab1)
        plastico(self)

        #Label y entry del ID de la planta
        self.lb_id_planta = ctk.CTkLabel(
            self.tab_parametros.tab(self.tab2),
            **style.STYLELABEL,
            text= "ID:",
            fg_color="transparent"
        )
        self.lb_id_planta.place(
            relx = 0.03,
            rely = 0.05
        )
        self.et_id_planta = ctk.CTkEntry(
            self.tab_parametros.tab(self.tab2),
            placeholder_text = ""
        )
        self.et_id_planta.place(
            relx = 0.07,
            rely = 0.05,
            relwidth = 0.06
        )

        
        #Label y entry de la ubicación de la planta
        self.lb_ubicacion_planta = ctk.CTkLabel(
            self.tab_parametros.tab(self.tab2),
            **style.STYLELABEL,
            text= "ID:",
            fg_color="transparent"
        )
        self.lb_ubicacion_planta.place(
            relx = 0.20,
            rely = 0.05
        )
        self.et_ubicacion_planta = ctk.CTkEntry(
            self.tab_parametros.tab(self.tab2),
            placeholder_text = ""
        )
        self.et_ubicacion_planta.place(
            relx = 0.30,
            rely = 0.05,
            relwidth = 0.20
        )





        
        

