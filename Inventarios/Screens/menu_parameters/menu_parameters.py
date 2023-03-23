#se importan las librerias que nos permiten generar una interfaz grafica
import customtkinter as ctk
import pandas as pd
import datetime as dt
import pyodbc

#Se importan valores constantes de nuestra aplicación
from constants import style
from Functions import DBC,validations
from Screens.message.message import confirm_message
from Screens.menu_parameters.plasticos import plastico,insert,next, previous, clean, search_by_codinv,delete_by_codinv, update
from Screens.menu_parameters.plantas import plantas,insert_planta,next_planta, previous_planta, clean_planta, search_by_id_planta,delete_by_id_planta, update_planta
class menu_parameters(ctk.CTkFrame):
    fecha = dt.date.today()
    ids_plasticos = []
    ids_plantas = []
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
        #Variable que conserva el estado de confirmación 
        self.cfm = False
        #Inicio de los widgets
        self.init_tabview()

#----------------Plasticos------------------------------
    def insert_con(self):
        """Conecta a la función insert en plasticos.py"""
        insert(self)
    def update_con(self):
        """Conecta a la función update en plasticos.py"""
        update(self)
    def next_con(self):
        """Conecta a la función next en plasticos.py"""
        next(self)
    def previous_con(self):
        """Conecta a la función previous en plasticos.py"""
        previous(self)
    def clean_con(self):
        """Conecta a la función clean en plasticos.py"""
        clean(self)
    def search_by_codinv_con(self):
        """Conecta a la función search_by_codinv en plasticos.py"""
        search_by_codinv(self)
    def delete_by_codinv_con(self):
        """Conecta a la función delete_by_codinv en plasticos.py"""
        delete_by_codinv(self)

    def confirm_action(self, message):
        """Genera un cuadro de alerta donde se pide confirmar la acción para continuar,
        este cambia la variable cfm del frame principal"""
        self.message = confirm_message(self, self.controller, message)
#--------------------PLantas------------------------------------
    def insert_planta_con(self):
        """Conecta a la función insert en plasticos.py"""
        insert_planta(self)
    def update_planta_con(self):
        """Conecta a la función update en plasticos.py"""
        update_planta(self)
    def next_planta_con(self):
        """Conecta a la función next en plasticos.py"""
        next_planta(self)
    def previous_planta_con(self):
        """Conecta a la función previous en plasticos.py"""
        previous_planta(self)
    def clean_planta_con(self):
        """Conecta a la función clean en plasticos.py"""
        clean_planta(self)
    def search_by_id_planta_con(self):
        """Conecta a la función search_by_codinv en plasticos.py"""
        search_by_id_planta(self)
    def delete_by_id_planta_con(self):
        """Conecta a la función delete_by_codinv en plasticos.py"""
        delete_by_id_planta(self)

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
        plantas(self)

        






        
        

