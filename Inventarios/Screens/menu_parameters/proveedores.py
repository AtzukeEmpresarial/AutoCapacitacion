import customtkinter as ctk
import pandas as pd
from Screens.message.message import alert_message

from constants import style
from Functions import validations, DBC

def next_proveedor(self):
    ''' Función que se encarga de cargar los datos de los proveedores en orden consecutivo
    basado en el ID'''
    
    if self.et_id_proveedor.get() == "":
        self.ids_proveedores = DBC.find_indexes(self.cnx_nac,"ID","PROVEEDORES").to_list()
        self.ids_proveedores.sort()
        self.et_id_proveedor.delete(0, ctk.END)
        self.et_id_proveedor.insert(0, str(self.ids_proveedores[0]))
        search_by_id_proveedor(self) 
    elif int(self.et_id_proveedor.get()) < self.ids_proveedores[-1]:
        id_proveedor = int(self.et_id_proveedor.get())
        index = self.ids_proveedores.index(id_proveedor)
        self.et_id_proveedor.delete(0, ctk.END)
        self.et_id_proveedor.insert(0, str(self.ids_proveedores[index + 1]))
        search_by_id_proveedor(self) 
        
def previous_proveedor (self):
    ''' Función que se encarga de cargar los datos de los proveedores en orden consecutivo
    inverso basado en el ID'''

    if int(self.et_id_proveedor.get()) > self.ids_proveedores[0]:
        id_proveedor = int(self.et_id_proveedor.get())
        index = self.ids_proveedores.index(id_proveedor)
        self.et_id_proveedor.delete(0, ctk.END)
        self.et_id_proveedor.insert(0, str(self.ids_proveedores[index - 1]))
        search_by_id_proveedor(self)

def search_by_id_proveedor(self):
    ''' Función que carga los datos de un proveedor según el ID'''
    proveedor_df = DBC.find_by(self.cnx_nac, "ID", int(self.et_id_proveedor.get()), "PROVEEDORES")
    load_in_widgets_proveedor(self,proveedor_df)

def load_in_widgets_proveedor(self, df: pd.DataFrame):
    '''Carga la información contenida en un dataframe en los widgets del proveedor,
    recibe:
    self = Frame padre
    df = Dataframe con los datos del proveedor'''
    self.et_nombre_proveedor.delete(0, ctk.END)
    self.proveedor_inactivo_var.set(False)
    self.et_tarifa_proveedor.delete(0, ctk.END)
    self.tb_descripcion_proveedor.delete(1.0, ctk.END)

    self.et_nombre_proveedor.insert(0, df.loc[0,"NOMBRE"])
    self.proveedor_inactivo_var.set(str(df.loc[0,"ACTIVO"]))
    self.et_tarifa_proveedor.insert(0, df.loc[0,"TARIFA"])
    self.tb_descripcion_proveedor.insert(1.0, df.loc[0,"DESCRIPCION"])

def insert_proveedor(self):
    ''' Función que se encarga de guardar los datos ingresados en los campos de
    creación de plantas; guarda en un diccionario los datos en los entry
    para convertirlo en un DataFrame y posteriormente enviarlo a la función
    de la ODBC que guarda un proveedor.'''

    self.confirm_action("¿Seguro que desea crear este registro?")
    self.confirm_action("¿Seguro que desea crearlo?")
    if self.cfm:
        proveedores_dic = {
            'NOMBRE' : [self.et_nombre_proveedor.get()],
            'ACTIVO' : [int(self.chk_proveedor_inactivo.get())],
            'TARIFA' : [float(self.et_tarifa_proveedor.get())],
            'DESCRIPCION' : [self.tb_descripcion_proveedor.get("1.0","end-1c")] 
        }
        proveedores_df = pd.DataFrame(proveedores_dic)
        DBC.insert(self, self.cnx_nac,proveedores_df,"PROVEEDORES")
        self.ids_proveedores = DBC.find_indexes(self.cnx_nac, "ID","PROVEEDORES").to_list()
        self.ids_proveedores.sort()
        self.proveedores = DBC.find_indexes(self.cnx_nac,"NOMBRE","PROVEEDORES").to_list()
        self.proveedores.sort()
        self.cfm = False

def update_proveedor(self):
    ''' Función que se encarga de guardar los datos ingresados en los campos de
    creación de plantas; guarda en un diccionario los datos en los entry
    para convertirlo en un DataFrame y posteriormente enviarlo a la función
    de la ODBC que guarda un proveedor.'''

    self.confirm_action("¿Seguro que desea actualizar este registro?")
    self.confirm_action("¿Seguro que desea actualizarlo?")

    if self.cfm:
        ids = DBC.find_indexes(self.cnx_nac, "ID", "PROVEEDORES").to_list()
        if int(self.et_id_proveedor.get()) not in ids:
            self.message = alert_message(self, self.controller, "No existe ese ID \n Por favor verificalo")
        else:
            proveedores_dic = {
            'NOMBRE' : [self.et_nombre_proveedor.get()],
            'ACTIVO' : [int(self.chk_proveedor_inactivo.get())],
            'TARIFA' : [float(self.et_tarifa_proveedor.get())],
            'DESCRIPCION' : [self.tb_descripcion_proveedor.get("1.0","end-1c")] 
            }
            proveedores_df = pd.DataFrame(proveedores_dic)
            DBC.update(self, self.cnx_nac,proveedores_df, int(self.et_id_proveedor.get()),"PROVEEDORES")
            self.cfm = False

def clean_proveedor (self):
    '''Limpia la información de los widgets de proveedores'''

    self.et_id_proveedor.delete(0, ctk.END)
    self.et_nombre_proveedor.delete(0, ctk.END)
    self.proveedor_inactivo_var.set(False)
    self.et_tarifa_proveedor.delete(0, ctk.END)
    self.tb_descripcion_proveedor.delete(1.0, ctk.END)

def delete_by_id_proveedor(self):
    '''Función que se encarga de eliminar un proveedor según su ID'''
    self.confirm_action("¿Está seguro que desea Eliminar este registro de Forma permanente?")
    self.confirm_action("¿Seguro que desea eliminarlo?")

    if self.cfm:
        DBC.delete(self, self.cnx_nac,"ID", int(self.et_id_proveedor.get()), "PROVEEDORES")
        self.et_id_proveedor.delete(0,ctk.END)
        self.ids_proveedores = DBC.find_indexes(self.cnx_nac, "ID","PROVEEDORES").to_list()
        self.ids_proveedores.sort()
        self.proveedores = DBC.find_indexes(self.cnx_nac,"NOMBRE","PROVEEDORES").to_list()
        self.proveedores.sort()
        clean_proveedor(self)

def proveedores (self):
    #Carga inicial de proveedores
    self.proveedores = DBC.find_indexes(self.cnx_nac,"NOMBRE","PROVEEDORES").to_list()
    self.proveedores.sort()
    #Label y entry del ID del proveedor
    self.lb_id_proveedor = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab3),
        **style.STYLELABEL,
        text= "ID:",
        fg_color="transparent"
    )
    self.lb_id_proveedor.place(
        relx = 0.03,
        rely = 0.05
    )
    self.et_id_proveedor = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab3),
        placeholder_text = "ID",
        validate = "key",
        validatecommand = (self.controller.register(validations.validate_input_numeric),"%P")
    )
    self.et_id_proveedor.place(
        relx = 0.07,
        rely = 0.05,
        relwidth = 0.06
    )
    #Label y entry del nombre del proveedor
    self.lb_nombre_proveedor = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab3),
        **style.STYLELABEL,
        text= "Nombre:",
        fg_color="transparent"
    )
    self.lb_nombre_proveedor.place(
        relx = 0.14,
        rely = 0.05
    )
    self.et_nombre_proveedor = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab3),
        placeholder_text = "Nombre"
    )
    self.et_nombre_proveedor.place(
        relx = 0.25,
        rely = 0.05,
        relwidth = 0.30
    )
    #checkBox si el proveedor está inactivo
    self.proveedor_inactivo_var = ctk.StringVar()
    self.chk_proveedor_inactivo = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab3),
        text = "Proveedor Inactivo",
        **style.STYLELABEL,
        variable = self.proveedor_inactivo_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_proveedor_inactivo.place(
        relx = 0.03,
        rely = 0.135
    )
    #Label y entry de la tarifa del proveedor
    self.lb_tarifa_proveedor = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab3),
        **style.STYLELABEL,
        text= "Tarifa:",
        fg_color="transparent"
    )
    self.lb_tarifa_proveedor.place(
        relx = 0.30,
        rely = 0.13
    )
    self.et_tarifa_proveedor = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab3),
        placeholder_text = "Tarifa"
        )
    self.et_tarifa_proveedor.place(
        relx = 0.38,
        rely = 0.13,
        relwidth = 0.30
    )
    #Textbox de las observaciones
    self.tb_descripcion_proveedor = ctk.CTkTextbox(
        self.tab_parametros.tab(self.tab3),
        **style.STYLELABEL,
        height=65
    )
    self.tb_descripcion_proveedor.configure(
        font = ("Calibri Bold", 14)
    ) 
    self.tb_descripcion_proveedor.place(
        relx = 0.03,
        rely = 0.21,
        relwidth = 0.77
    )
    #----------------------------BOTONES----------------------------------
        #Botón que avanza entre los diferentes proveedores
    self.bt_next_proveedor = ctk.CTkButton(
        self.tab_parametros.tab(self.tab3),
        **style.SMALLBUTTONSTYLE,
        text = ">>",
        command = self.next_proveedor_con,
        width= 40
    )
    self.bt_next_proveedor.place(
        relx = 0.905,
        rely = 0.05
    )
    #Botón que retrocede entre los diferentes proveedores
    self.bt_previous_proveedor = ctk.CTkButton(
        self.tab_parametros.tab(self.tab3),
        **style.SMALLBUTTONSTYLE,
        text = "<<",
        command = self.previous_proveedor_con,
        width= 40
    )
    self.bt_previous_proveedor.place(
        relx = 0.83,
        rely = 0.05
    )
    #Botón que guardar el proveedor en la tabla PROVEEDORES
    self.bt_load_proveedor = ctk.CTkButton(
        self.tab_parametros.tab(self.tab3),
        **style.SMALLBUTTONSTYLE,
        text = "Guardar",
        command = self.insert_proveedor_con,
        width= 90
    )
    self.bt_load_proveedor.place(
        relx = 0.83,
        rely = 0.19
    )
    #Botón que limpia los widgets
    self.bt_clean_proveedor = ctk.CTkButton(
        self.tab_parametros.tab(self.tab3),
        **style.SMALLBUTTONSTYLE,
        text = "Limpiar",
        command = self.clean_proveedor_con,
        width= 90
    )
    self.bt_clean_proveedor.place(
        relx = 0.83,
        rely = 0.12
    )
    #Botón que busca según el ID
    self.bt_search_proveedor = ctk.CTkButton(
        self.tab_parametros.tab(self.tab3),
        **style.SMALLBUTTONSTYLE,
        text = "Buscar",
        command = self.search_by_id_proveedor_con,
        width= 90
    )
    self.bt_search_proveedor.place(
        relx = 0.83,
        rely = 0.26
    )
    #Botón eliminar el proveedor según su ID
    self.bt_delete_proveedor = ctk.CTkButton(
        self.tab_parametros.tab(self.tab3),
        **style.SMALLBUTTONSTYLE,
        text = "Eliminar",
        command = self.delete_by_id_proveedor_con,
        width= 90
    )
    self.bt_delete_proveedor.place(
        relx = 0.83,
        rely = 0.33
    )
    #Botón actualizar el proveedor según su ID
    self.bt_edit_proveedor = ctk.CTkButton(
        self.tab_parametros.tab(self.tab3),
        **style.SMALLBUTTONSTYLE,
        text = "Editar",
        command = self.update_proveedor_con,
        width= 90
    )
    self.bt_edit_proveedor.place(
        relx = 0.83,
        rely = 0.40
    )