#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
from tkcalendar import Calendar
import customtkinter as ctk
from tksheet import Sheet
import pandas as pd
import pyodbc
import datetime as dt
from Screens.message.message import alert_message
from Screens.message.message import confirm_message
#Se importan valores constantes de nuestra aplicación
from constants import style
from Functions import DBC

class menu_informes(ctk.CTkFrame):
    """
    Clase encargada de la alimentación y proceso de datos,
    este contiene diferentes pestañas para los distintos pasos del
    proceso
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color = style.GRAYBLACK)
        self.controller = controller
        self.count = 0
        #conexión que usara esta pantalla
        self.cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID={};PWD={}'.format(controller.user, controller.password), autocommit=True )
        #cargamos listas
        self.ls_plasticos = DBC.find_indexes(self.cnx_nac,"NOMBRE", "PLASTICOS").to_list()
        self.ls_plasticos.sort()
        self.ls_plantas = DBC.find_indexes_where_int(self.cnx_nac,"UBICACION","PLANTAS","PRODUCCION",0).to_list()
        self.ls_plantas.sort()
        self.ls_plantas = list(set(self.ls_plantas))
        self.ls_proveedores = DBC.find_indexes(self.cnx_nac,"NOMBRE","PROVEEDORES").to_list()
        self.ls_proveedores.sort()
        self.ls_proveedores = list(set(self.ls_proveedores))
        self.init_tabview()
        self.comportamiento_plastico()




#__________________________Tabview general______________________________________________
    def init_tabview(self):
        """
        Inicia el widget de pestañas, este contiene los diferentes procesos de informes
        """
        self.tab_informes = ctk.CTkTabview(
            self,
            segmented_button_selected_hover_color = style.BLUE,
            segmented_button_selected_color= style.DARKBLUE
        )
        self.tab_informes.pack(
            anchor = ctk.N,
            padx=20, 
            pady=20, 
            fill = ctk.BOTH,
            expand = True
        )
        self.tab1 = "Comportamiento por plastico"
        self.tab2 = "Comportamiento por planta"
        self.tab3 = "Comportamiento por provedor"
        self.tab_informes.add(self.tab1)
        self.tab_informes.add(self.tab2)
        self.tab_informes.add(self.tab3)
        






#_________________________Comportamiento por plastico_____________________________________
    def comportamiento_plastico(self):
        #label y Calendario para seleccionar la fecha inicial del rango
        self.lb_rango_fecha_plastico_inicial = ctk.CTkLabel(
            self.tab_informes.tab(self.tab1),
            **style.STYLELABEL,
            text= "Fecha inicial",
            fg_color="transparent"
        )
        self.lb_rango_fecha_plastico_inicial.place(
            relx = 0.07,
            rely = 0
        )
        self.calendario_plastico_inicial = Calendar(
            self.tab_informes.tab(self.tab1), 
            selectmode='day', 
            font=style.FONT_LINT,
            showweeknumbers=False, 
            cursor="hand2", 
            date_pattern= 'ymmdd',
            borderwidth=0, 
            bordercolor='white',
            locale='es_ES'
        )
        self.calendario_plastico_inicial.place_configure(
            relx = 0,
            rely = 0.06
        )
        #label y Calendario para seleccionar la fecha final del rango
        self.lb_rango_fecha_plastico_final = ctk.CTkLabel(
            self.tab_informes.tab(self.tab1),
            **style.STYLELABEL,
            text= "Fecha final",
            fg_color="transparent"
        )
        self.lb_rango_fecha_plastico_final.place(
            relx = 0.79,
            rely = 0
        )
        self.calendario_plastico_final = Calendar(
            self.tab_informes.tab(self.tab1), 
            selectmode='day', 
            font=style.FONT_LINT,
            showweeknumbers=False, 
            cursor="hand2", 
            date_pattern= 'ymmdd',
            borderwidth=0, 
            bordercolor='white',
            locale='es_ES'
        )
        self.calendario_plastico_final.place_configure(
            relx = 0.70,
            rely = 0.06
        )
        #Label y Combobox del plastico
        self.lb_plastico = ctk.CTkLabel(
            self.tab_informes.tab(self.tab1),
            **style.STYLELABEL,
            text= "Plastico",
            fg_color="transparent"
        )
        self.lb_plastico.place(
            relx = 0.44,
            rely = 0
        )
        self.plastico_var = ctk.StringVar()
        self.cb_plastico = ctk.CTkComboBox(
            self.tab_informes.tab(self.tab1),
            values = self.ls_plasticos,
            variable = self.plastico_var
        )
        self.cb_plastico.place(
            relx = 0.39,
            rely = 0.06,
            relwidth = 0.20
        )
        #Label y Combobox del planta
        self.lb_planta = ctk.CTkLabel(
            self.tab_informes.tab(self.tab1),
            **style.STYLELABEL,
            text= "Planta",
            fg_color="transparent"
        )
        self.lb_planta.place(
            relx = 0.45,
            rely = 0.13
        )
        self.planta_var = ctk.StringVar()
        self.cb_planta = ctk.CTkComboBox(
            self.tab_informes.tab(self.tab1),
            values = self.ls_plantas,
            variable = self.planta_var
        )
        self.cb_planta.place(
            relx = 0.39,
            rely = 0.19,
            relwidth = 0.20
        )
        #Label y Combobox del provedor
        self.lb_provedor = ctk.CTkLabel(
            self.tab_informes.tab(self.tab1),
            **style.STYLELABEL,
            text= "Provedor",
            fg_color="transparent"
        )
        self.lb_provedor.place(
            relx = 0.44,
            rely = 0.26
        )
        self.provedor_var = ctk.StringVar()
        self.cb_provedor = ctk.CTkComboBox(
            self.tab_informes.tab(self.tab1),
            values = self.ls_proveedores,
            variable = self.provedor_var
        )
        self.cb_provedor.place(
            relx = 0.39,
            rely = 0.32,
            relwidth = 0.20
        )
        #Botón generar informe
        self.bt_delete_traslado = ctk.CTkButton(
            self.tab_informes.tab(self.tab1),
            **style.SMALLBUTTONSTYLE,
            text = "Completar",
            command = self.generar_por_plastico,
            width= 90
        )
        self.bt_delete_traslado.place(
            relx = 0.43,
            rely = 0.40
        )

    def generar_por_plastico(self):
        str_fecha_inicial = self.calendario_plastico_inicial.get_date()
        str_fecha_final = self.calendario_plastico_final.get_date()
        