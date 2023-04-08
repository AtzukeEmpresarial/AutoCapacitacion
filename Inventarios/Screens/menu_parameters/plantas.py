import customtkinter as ctk
import pandas as pd
from Screens.message.message import alert_message

from constants import style
from Functions import validations, DBC

def next_planta(self):
    ''' Función que se encarga de cargar los datos de una planta en orden consecutivo
    basado en el ID'''
    
    if self.et_id_planta.get() == "":
        self.ids_plantas = DBC.find_indexes(self.cnx_nac,"ID","PLANTAS").to_list()
        self.ids_plantas.sort()
        self.et_id_planta.delete(0, ctk.END)
        self.et_id_planta.insert(0, str(self.ids_plantas[0]))
        search_by_id_planta(self) 
    elif int(self.et_id_planta.get()) < self.ids_plantas[-1]:
        id_planta = int(self.et_id_planta.get())
        index = self.ids_plantas.index(id_planta)
        self.et_id_planta.delete(0, ctk.END)
        self.et_id_planta.insert(0, str(self.ids_plantas[index + 1]))
        search_by_id_planta(self) 
        
def previous_planta (self):
    ''' Función que se encarga de cargar los datos de una planta en orden consecutivo
    inverso basado en el ID'''

    if int(self.et_id_planta.get()) > self.ids_plantas[0]:
        id_plastico = int(self.et_id_planta.get())
        index = self.ids_plantas.index(id_plastico)
        self.et_id_planta.delete(0, ctk.END)
        self.et_id_planta.insert(0, str(self.ids_plantas[index - 1]))
        search_by_id_planta(self)

def search_by_id_planta(self):
    ''' Función que carga los datos de una planta según el ID'''
    plasticos_df = DBC.find_by(self.cnx_nac, "ID", int(self.et_id_planta.get()), "PLANTAS")
    load_in_widgets_planta(self,plasticos_df)

def insert_planta(self):
    ''' Función que se encarga de guardar los datos ingresados en los campos de
    creación de plantas; guarda en un diccionario los datos en los entry
    para convertirlo en un DataFrame y posteriormente enviarlo a la función
    de la ODBC que guarda las plantas.'''

    self.confirm_action("¿Seguro que desea crear este registro?")
    self.confirm_action("¿Seguro que desea crearlo?")

    if self.cfm:
        plantas_dic = {
            'UBICACION' : [self.cb_ubicacion_planta.get()],
            'DESCRIPCION' : [self.tb_descripcion_planta.get("1.0","end-1c")],
            'OPERADOR' : [self.cb_proveedor_planta.get()],
            'LT' : [int(self.et_lt_planta.get())],
            'ACTIVA' : [int(self.chk_planta_inactiva.get())],
            'PRODUCCION' : [int(self.chk_planta_produccion.get())]
        }
        plantas_df = pd.DataFrame(plantas_dic)
        DBC.insert(self, self.cnx_nac,plantas_df,"PLANTAS")
        self.ids_plantas = DBC.find_indexes(self.cnx_nac, "ID","PLANTAS").to_list()
        self.ids_plantas.sort()
        self.cfm = False

def clean_planta (self):
    '''Limpia la información de los widgets de plasticos'''
    self.ubicacion_planta_var.set("")
    self.tb_descripcion_planta.delete(1.0, ctk.END)
    self.proveedor_planta_var.set("")
    self.et_lt_planta.delete(0, ctk.END)
    self.planta_inactiva_var.set(False)
    self.planta_produccion_var.set(False)

def load_in_widgets_planta(self, df: pd.DataFrame):
    '''Carga la información contenida en un dataframe en los widgets de planta,
    recibe:
    self = Frame padre
    df = Dataframe con los datos de la planta'''
    self.ubicacion_planta_var.set("")
    self.tb_descripcion_planta.delete(1.0, ctk.END)
    self.proveedor_planta_var.set("")
    self.et_lt_planta.delete(0, ctk.END)
    self.planta_inactiva_var.set(False)
    self.planta_produccion_var.set(False)

    self.ubicacion_planta_var.set(df.loc[0,"UBICACION"])
    self.tb_descripcion_planta.insert(1.0,df.loc[0,"DESCRIPCION"])
    self.proveedor_planta_var.set(df.loc[0,"OPERADOR"])
    self.et_lt_planta.insert(0, df.loc[0,"LT"])
    self.planta_inactiva_var.set(str(df.loc[0,"ACTIVA"]))
    self.planta_produccion_var.set(str(df.loc[0,"PRODUCCION"]))

def delete_by_id_planta(self):
    '''Función que se encarga de eliminar una planta según su ID'''
    self.confirm_action("¿Está seguro que desea Eliminar este registro de Forma permanente?")
    self.confirm_action("¿Seguro que desea eliminarlo?")

    if self.cfm:
        DBC.delete(self, self.cnx_nac,"ID", int(self.et_id_planta.get()), "PLANTAS")
        self.et_id_planta.delete(0,ctk.END)
        self.ids_plantas = DBC.find_indexes(self.cnx_nac, "ID","PLANTAS").to_list()
        self.ids_plantas.sort()
        clean_planta(self)

def update_planta(self):
    ''' Función que se encarga de guardar los datos ingresados en los campos de
    creación de plantas; guarda en un diccionario los datos en los entry
    para convertirlo en un DataFrame y posteriormente enviarlo a la función
    de la ODBC que guarda los plantas.'''

    self.confirm_action("¿Seguro que desea actualizar este registro?")
    self.confirm_action("¿Seguro que desea actualizarlo?")

    if self.cfm:
        ids = DBC.find_indexes(self.cnx_nac, "ID", "PLANTAS").to_list()
        print(ids)
        print(int(self.et_id_planta.get()))
        if int(self.et_id_planta.get()) not in ids:
            self.message = alert_message(self, self.controller, "No existe ese ID \n Por favor verificalo")
        else:
            plantas_dic = {
            'UBICACION' : [self.cb_ubicacion_planta.get()],
            'DESCRIPCION' : [self.tb_descripcion_planta.get("1.0","end-1c")],
            'OPERADOR' : [self.cb_proveedor_planta.get()],
            'LT' : [int(self.et_lt_planta.get())],
            'ACTIVA' : [int(self.chk_planta_inactiva.get())],
            'PRODUCCION' : [int(self.chk_planta_produccion.get())]
            }
            plantas_df = pd.DataFrame(plantas_dic)
            DBC.update(self, self.cnx_nac,plantas_df,int(self.et_id_planta.get()),"PLANTAS")
            self.cfm = False

def plantas (self):
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
        placeholder_text = "ID",
        validate = "key",
        validatecommand = (self.controller.register(validations.validate_input_numeric),"%P")
    )
    self.et_id_planta.place(
        relx = 0.07,
        rely = 0.05,
        relwidth = 0.06
    )
    #Label y Combobox de la ubicación de la planta
    self.lb_ubicacion_planta = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab2),
        **style.STYLELABEL,
        text= "Ubicación:",
        fg_color="transparent"
    )
    self.lb_ubicacion_planta.place(
        relx = 0.27,
        rely = 0.05
    )
    self.ubicacion_planta_var = ctk.StringVar()
    self.cb_ubicacion_planta = ctk.CTkComboBox(
        self.tab_parametros.tab(self.tab2),
        values = ["Cali", "Medellín", "Bogóta", "Bucaramanga", "Pereira", "Barranquilla"],
        variable = self.ubicacion_planta_var
    )
    self.cb_ubicacion_planta.place(
        relx = 0.40,
        rely = 0.05,
        relwidth = 0.20
    )
    #Label y entry del LT correspondiente a la planta
    self.lb_lt_planta = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab2),
        **style.STYLELABEL,
        text= "LT:",
        fg_color="transparent"
    )
    self.lb_lt_planta.place(
        relx = 0.72,
        rely = 0.05
    )
    self.et_lt_planta = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab2),
        placeholder_text = "",
        validate = "key",
        validatecommand = (self.controller.register(validations.validate_input_numeric),"%P")
    )
    self.et_lt_planta.place(
        relx = 0.76,
        rely = 0.05,
        relwidth = 0.05
    )
    #Label y Combobox del proveedor de la planta
    self.lb_proveedor_planta = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab2),
        **style.STYLELABEL,
        text= "Proveedor:",
        fg_color="transparent"
    )
    self.lb_proveedor_planta.place(
        relx = 0.03,
        rely = 0.13
    )
    self.proveedor_planta_var = ctk.StringVar()
    self.cb_proveedor_planta = ctk.CTkComboBox(
        self.tab_parametros.tab(self.tab2),
        values = self.proveedores,
        variable = self.proveedor_planta_var
    )
    self.cb_proveedor_planta.place(
        relx = 0.17,
        rely = 0.13,
        relwidth = 0.20
    )
    #checkBox si planta inactiva
    self.planta_inactiva_var = ctk.StringVar()
    self.chk_planta_inactiva = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab2),
        text = "Panta Inactiva", 
        **style.STYLELABEL,
        variable = self.planta_inactiva_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_planta_inactiva.place(
        relx = 0.58,
        rely = 0.135
    )
    #Textbox de las observaciones
    self.tb_descripcion_planta = ctk.CTkTextbox(
        self.tab_parametros.tab(self.tab2),
        **style.STYLELABEL,
        height=65
    )
    self.tb_descripcion_planta.configure(
        font = ("Calibri Bold", 14)
    ) 
    self.tb_descripcion_planta.place(
        relx = 0.03,
        rely = 0.21,
        relwidth = 0.77
    )
    #checkBox si planta es de producción
    self.planta_produccion_var = ctk.StringVar()
    self.chk_planta_produccion = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab2),
        text = "Planta de producción",
        **style.STYLELABEL,
        variable = self.planta_produccion_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_planta_produccion.place(
        relx = 0.3,
        rely = 0.38
    )
    #----------------------BOTONES----------------------------------------
        #Botón que avanza entre las diferentes plantas
    self.bt_next_planta = ctk.CTkButton(
        self.tab_parametros.tab(self.tab2),
        **style.SMALLBUTTONSTYLE,
        text = ">>",
        command = self.next_planta_con,
        width= 40
    )
    self.bt_next_planta.place(
        relx = 0.905,
        rely = 0.05
    )
    #Botón que retrocede entre las diferentes plantas
    self.bt_previous_planta = ctk.CTkButton(
        self.tab_parametros.tab(self.tab2),
        **style.SMALLBUTTONSTYLE,
        text = "<<",
        command = self.previous_planta_con,
        width= 40
    )
    self.bt_previous_planta.place(
        relx = 0.83,
        rely = 0.05
    )
    #Botón que guarda la planta en la base de datos
    self.bt_load_planta = ctk.CTkButton(
        self.tab_parametros.tab(self.tab2),
        **style.SMALLBUTTONSTYLE,
        text = "Guardar",
        command = self.insert_planta_con,
        width= 90
    )
    self.bt_load_planta.place(
        relx = 0.83,
        rely = 0.19
    )
    #Botón que limpia los widgets
    self.bt_clean_planta = ctk.CTkButton(
        self.tab_parametros.tab(self.tab2),
        **style.SMALLBUTTONSTYLE,
        text = "Limpiar",
        command = self.clean_planta_con,
        width= 90
    )
    self.bt_clean_planta.place(
        relx = 0.83,
        rely = 0.12
    )
    #Botón que busca según el ID de la planta en PLANTAS
    self.bt_search_planta = ctk.CTkButton(
        self.tab_parametros.tab(self.tab2),
        **style.SMALLBUTTONSTYLE,
        text = "Buscar",
        command = self.search_by_id_planta_con,
        width= 90
    )
    self.bt_search_planta.place(
        relx = 0.83,
        rely = 0.26
    )
    #Botón eliminar que elimina una planta según su ID
    self.bt_delete_planta = ctk.CTkButton(
        self.tab_parametros.tab(self.tab2),
        **style.SMALLBUTTONSTYLE,
        text = "Eliminar",
        command = self.delete_by_id_planta_con,
        width= 90
    )
    self.bt_delete_planta.place(
        relx = 0.83,
        rely = 0.33
    )
    #Botón actualizar que actualiza una planta según su ID
    self.bt_edit_planta = ctk.CTkButton(
        self.tab_parametros.tab(self.tab2),
        **style.SMALLBUTTONSTYLE,
        text = "Editar",
        command = self.update_planta_con,
        width= 90
    )
    self.bt_edit_planta.place(
        relx = 0.83,
        rely = 0.40
    )