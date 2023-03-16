import customtkinter as ctk
import pandas as pd
from Screens.message.message import used_codinv_message

from constants import style
from Functions import validations, DBC

def search_by_codinv(self):
    ''' Función que carga los datos de un plastico según el ID'''
    plasticos_df = DBC.find_by_codinv(self.cnx_nac,int(self.et_codigo_inventario.get()),"PLASTICOS")
    load_in_widgets_codinv(self,plasticos_df)

def search_by_id(self):
    ''' Función que carga los datos de un plastico según el ID'''
    plasticos_df = DBC.find_by_id(self.cnx_nac,int(self.et_id.get()),"PLASTICOS")
    load_in_widgets(self,plasticos_df)

def next(self):
    ''' Función que se encarga de cargar los datos de un plastico en orden consecutivo
    basado en el ID'''
    
    if self.et_id.get() == "":
        self.ids_plasticos = DBC.find_ids(self.cnx_nac,"PLASTICOS").to_list()
        self.ids_plasticos.sort()
        self.et_id.delete(0, ctk.END)
        self.et_id.insert(0, str(self.ids_plasticos[0]))
        search_by_id(self) 
    elif int(self.et_id.get()) < self.ids_plasticos[-1]:
        id_plastico = int(self.et_id.get())
        index = self.ids_plasticos.index(id_plastico)
        self.et_id.delete(0, ctk.END)
        self.et_id.insert(0, str(self.ids_plasticos[index + 1]))
        search_by_id(self) 
        
def previous (self):
    ''' Función que se encarga de cargar los datos de un plastico en orden consecutivo
    inverso basado en el ID'''

    if int(self.et_id.get()) > self.ids_plasticos[0]:
        id_plastico = int(self.et_id.get())
        index = self.ids_plasticos.index(id_plastico)
        self.et_id.delete(0, ctk.END)
        self.et_id.insert(0, str(self.ids_plasticos[index - 1]))
        search_by_id(self)
        print(self.ids_plasticos)  

def clean (self):
    '''Limpia la información de los widgets de plasticos'''
    self.et_id.delete(0,ctk.END)
    self.et_codigo_inventario.delete(0,ctk.END)
    self.et_codigo_franquicia.delete(0,ctk.END)
    self.et_tipo_tarjeta.delete(0,ctk.END)
    self.et_bin.delete(0,ctk.END)
    self.et_logo.delete(0,ctk.END)
    self.et_tipo_producto.delete(0,ctk.END)
    self.et_clase.delete(0,ctk.END)
    self.et_nombre.delete(0,ctk.END)
    self.et_acumulacion.delete(0,ctk.END)
    self.et_realce.delete(0,ctk.END)
    self.tb_observaciones.delete(1.0,ctk.END)
    self.et_segmento.delete(0,ctk.END)
    self.et_cantidad.delete(0,ctk.END)
    self.descont_var.set(False)
    self.idemia_produc_cali_var.set(False)
    self.thales_produc_iztapalapa_var.set(False)
    self.thales_produc_asia_var.set(False)
    self.idemia_real_cali_var.set(False)
    self.idemia_real_bogo_var.set(False)
    self.idemia_real_mede_var.set(False)
    self.idemia_real_pere_var.set(False)
    self.idemia_real_buca_var.set(False)
    self.idemia_real_bquilla_var.set(False)
    self.thales_real_bogo_var.set(False)

def load_in_widgets(self, df: pd.DataFrame):
    '''Carga la información contenida en un dataframe en los widgets de plasticos,
    recibe:
    self = Frame padre
    df = Dataframe con los datos de los plasticos'''
    self.et_codigo_inventario.delete(0,ctk.END)
    self.et_codigo_franquicia.delete(0,ctk.END)
    self.et_tipo_tarjeta.delete(0,ctk.END)
    self.et_bin.delete(0,ctk.END)
    self.et_logo.delete(0,ctk.END)
    self.et_tipo_producto.delete(0,ctk.END)
    self.et_clase.delete(0,ctk.END)
    self.et_nombre.delete(0,ctk.END)
    self.et_acumulacion.delete(0,ctk.END)
    self.et_realce.delete(0,ctk.END)
    self.tb_observaciones.delete(1.0,ctk.END)
    self.et_segmento.delete(0,ctk.END)
    self.et_cantidad.delete(0,ctk.END)

    self.et_codigo_inventario.insert(0,str(df.loc[0,"CODINV"]))
    self.et_codigo_franquicia.insert(0,str(df.loc[0,"CODFRANQ"]))
    self.et_tipo_tarjeta.insert(0,df.loc[0,"TIPOTARJETA"])
    self.et_bin.insert(0,str(df.loc[0,"CODBIN"]))
    self.et_logo.insert(0,str(df.loc[0,"CODLOGO"]))
    self.et_tipo_producto.insert(0,df.loc[0,"TIPOPRODUC"])
    self.et_clase.insert(0,df.loc[0,"CLASE"])
    self.et_nombre.insert(0,df.loc[0,"NOMBRE"])
    self.et_acumulacion.insert(0,df.loc[0,"ACUMULACION"])
    self.et_realce.insert(0,df.loc[0,"TIPOREALCE"])
    self.tb_observaciones.insert(1.0,df.loc[0,"OBSERVACIONES"])
    self.et_segmento.insert(0,df.loc[0,"SEGMENTO"])
    self.descont_var.set(str(df.loc[0,"DESCONT"]))
    self.idemia_produc_cali_var.set(str(df.loc[0,"PIDEMIACALI"]))
    self.thales_produc_iztapalapa_var.set(str(df.loc[0,"PTHALESIZTA"]))
    self.thales_produc_asia_var.set(str(df.loc[0,"PTHALESASIA"]))
    self.idemia_real_cali_var.set(str(df.loc[0,"RIDEMIACALI"]))
    self.idemia_real_bogo_var.set(str(df.loc[0,"RIDEMIABOGO"]))
    self.idemia_real_mede_var.set(str(df.loc[0,"RIDEMIAMEDE"]))
    self.idemia_real_pere_var.set(str(df.loc[0,"RIDEMIAPERE"]))
    self.idemia_real_buca_var.set(str(df.loc[0,"RIDEMIABUCA"]))
    self.idemia_real_bquilla_var.set(str(df.loc[0,"RIDEMIABARRA"]))
    self.thales_real_bogo_var.set(str(df.loc[0,"RTHALESBOGO"]))
    self.et_cantidad.insert(0,str(df.loc[0,"CANTIDAD"]))

def load_in_widgets_codinv(self, df: pd.DataFrame):
    '''Carga la información contenida en un dataframe en los widgets de plasticos,
    recibe:
    self = Frame padre
    df = Dataframe con los datos de los plasticos'''
    self.et_id.delete(0,ctk.END)
    self.et_codigo_franquicia.delete(0,ctk.END)
    self.et_tipo_tarjeta.delete(0,ctk.END)
    self.et_bin.delete(0,ctk.END)
    self.et_logo.delete(0,ctk.END)
    self.et_tipo_producto.delete(0,ctk.END)
    self.et_clase.delete(0,ctk.END)
    self.et_nombre.delete(0,ctk.END)
    self.et_acumulacion.delete(0,ctk.END)
    self.et_realce.delete(0,ctk.END)
    self.tb_observaciones.delete(1.0,ctk.END)
    self.et_segmento.delete(0,ctk.END)
    self.et_cantidad.delete(0,ctk.END)

    self.et_id.insert(0,str(df.loc[0,"ID"]))
    self.et_codigo_franquicia.insert(0,str(df.loc[0,"CODFRANQ"]))
    self.et_tipo_tarjeta.insert(0,df.loc[0,"TIPOTARJETA"])
    self.et_bin.insert(0,str(df.loc[0,"CODBIN"]))
    self.et_logo.insert(0,str(df.loc[0,"CODLOGO"]))
    self.et_tipo_producto.insert(0,df.loc[0,"TIPOPRODUC"])
    self.et_clase.insert(0,df.loc[0,"CLASE"])
    self.et_nombre.insert(0,df.loc[0,"NOMBRE"])
    self.et_acumulacion.insert(0,df.loc[0,"ACUMULACION"])
    self.et_realce.insert(0,df.loc[0,"TIPOREALCE"])
    self.tb_observaciones.insert(1.0,df.loc[0,"OBSERVACIONES"])
    self.et_segmento.insert(0,df.loc[0,"SEGMENTO"])
    self.descont_var.set(str(df.loc[0,"DESCONT"]))
    self.idemia_produc_cali_var.set(str(df.loc[0,"PIDEMIACALI"]))
    self.thales_produc_iztapalapa_var.set(str(df.loc[0,"PTHALESIZTA"]))
    self.thales_produc_asia_var.set(str(df.loc[0,"PTHALESASIA"]))
    self.idemia_real_cali_var.set(str(df.loc[0,"RIDEMIACALI"]))
    self.idemia_real_bogo_var.set(str(df.loc[0,"RIDEMIABOGO"]))
    self.idemia_real_mede_var.set(str(df.loc[0,"RIDEMIAMEDE"]))
    self.idemia_real_pere_var.set(str(df.loc[0,"RIDEMIAPERE"]))
    self.idemia_real_buca_var.set(str(df.loc[0,"RIDEMIABUCA"]))
    self.idemia_real_bquilla_var.set(str(df.loc[0,"RIDEMIABARRA"]))
    self.thales_real_bogo_var.set(str(df.loc[0,"RTHALESBOGO"]))
    self.et_cantidad.insert(0,str(df.loc[0,"CANTIDAD"]))
      
def insert(self):
    ''' Función que se encarga de guardar los datos ingresados en los campos de
    creación de plasticos; guarda en un diccionario los datos en los entry
    para convertirlo en un DataFrame y posteriormente enviarlo a la función
    de la ODBC que guarda los plasticos.
    SE REVISA QUE EL CODIGO DE INVENTARIO NO EXISTA'''

    codinvs = DBC.find_codinvs(self.cnx_nac, "PLASTICOS")
    if int(self.et_codigo_inventario.get()) in codinvs:
        self.message = used_codinv_message(self, self.controller)
    else:
        plasticos_dic = {
            'CODINV' : [int(self.et_codigo_inventario.get())],
            'CODFRANQ' : [int(self.et_codigo_franquicia.get())],
            'TIPOTARJETA' : [self.et_tipo_tarjeta.get()],
            'CODBIN' : [int(self.et_bin.get())],
            'CODLOGO' : [int(self.et_logo.get())],
            'TIPOPRODUC' : [self.et_tipo_producto.get()],
            'CLASE' : [self.et_clase.get()],
            'NOMBRE' : [self.et_nombre.get()],
            'ACUMULACION' : [self.et_acumulacion.get()],
            'TIPOREALCE' : [self.et_realce.get()],
            'OBSERVACIONES' : [self.tb_observaciones.get("1.0","end-1c")],
            'SEGMENTO' : [self.et_segmento.get()],
            'DESCONT' : [int(self.chk_descontinuado.get())],
            'PIDEMIACALI':[int(self.chk_idemia_produc_cali.get())],
            'PTHALESIZTA':[int(self.chk_thales_produc_iztapalapa.get())],
            'PTHALESASIA':[int(self.chk_thales_produc_asia.get())],
            'RIDEMIACALI':[int(self.chk_idemia_real_cali.get())],
            'RIDEMIABOGO':[int(self.chk_idemia_real_bogo.get())],
            'RIDEMIAMEDE':[int(self.chk_idemia_real_mede.get())],
            'RIDEMIAPERE':[int(self.chk_idemia_real_pere.get())],
            'RIDEMIABUCA':[int(self.chk_idemia_real_buca.get())],
            'RIDEMIABARRA':[int(self.chk_idemia_real_bquilla.get())],
            'RTHALESBOGO':[int(self.chk_thales_real_bogo.get())],
            'CANTIDAD' : [int(self.et_cantidad.get())],
            'FECHA' : [self.fecha.strftime("%d-%m-%Y")],
        }
        plasticos_df = pd.DataFrame(plasticos_dic)
        DBC.insert(self.cnx_nac,plasticos_df,"PLASTICOS")
        self.ids_plasticos = DBC.find_ids(self.cnx_nac,"PLASTICOS").to_list()
        self.ids_plasticos.sort()

def plastico (self):
    #Label y entry (no activo) de la ID del plastico
    self.lb_id = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "ID:",
        fg_color="transparent"
    )
    self.lb_id.place(
        relx = 0.03,
        rely = 0.05
    )
    self.et_id = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = ""
    )
    self.et_id.place(
        relx = 0.07,
        rely = 0.05,
        relwidth = 0.06
    )
    #Label y entry del codigo de inventario del plastico
    self.lb_codigo_inventario = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Codigo de inventario:",
        fg_color="transparent"
    )
    self.lb_codigo_inventario.place(
        relx = 0.15,
        rely = 0.05
    )
    self.et_codigo_inventario = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "",
        validate = "key",
        validatecommand = (self.controller.register(validations.validate_input_numeric),"%P")
    )
    self.et_codigo_inventario.place(
        relx = 0.41,
        rely = 0.05,
        relwidth = 0.06
    )
    #Label y entry del codigo de franquicia
    self.lb_codigo_franquicia = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Codigo de franquicia:",
        fg_color="transparent"
    )
    self.lb_codigo_franquicia.place(
        relx = 0.49,
        rely = 0.05
    )
    self.et_codigo_franquicia = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "",
        validate = "key",
        validatecommand = (self.controller.register(validations.validate_input_numeric),"%P")
    )
    self.et_codigo_franquicia.place(
        relx = 0.745,
        rely = 0.05,
        relwidth = 0.06
    )
    #Label y entry del tipo de tarjeta
    self.lb_tipo_tarjeta = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Tipo de Tarjeta:",
        fg_color="transparent"
    )
    self.lb_tipo_tarjeta.place(
        relx = 0.03,
        rely = 0.13
    )
    self.et_tipo_tarjeta = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "Ingrese el tipo de tarjeta"
    )
    self.et_tipo_tarjeta.place(
        relx = 0.22,
        rely = 0.13,
        relwidth = 0.59
    )
    #Label y entry del Bin
    self.lb_bin = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "BIN:",
        fg_color="transparent"
    )
    self.lb_bin.place(
        relx = 0.03,
        rely = 0.21
    )
    self.et_bin = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "",
        validate = "key",
        validatecommand = (self.controller.register(validations.validate_input_numeric),"%P")
    )
    self.et_bin.place(
        relx = 0.088,
        rely = 0.21,
        relwidth = 0.09
    )
    #Label y entry del Logo
    self.lb_logo = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Logo:",
        fg_color="transparent"
    )
    self.lb_logo.place(
        relx = 0.29,
        rely = 0.21
    )
    self.et_logo = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "",
        validate = "key",
        validatecommand = (self.controller.register(validations.validate_input_numeric),"%P")
    )
    self.et_logo.place(
        relx = 0.36,
        rely = 0.21,
        relwidth = 0.09
    )
    #Label y entry del tipo producto
    self.lb_tipo_producto = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Tipo Producto:",
        fg_color="transparent"
    )
    self.lb_tipo_producto.place(
        relx = 0.57,
        rely = 0.21
    )
    self.et_tipo_producto = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = ""
    )
    self.et_tipo_producto.place(
        relx = 0.75,
        rely = 0.21,
        relwidth = 0.06
    )
    #Label y entry de la clase de producto
    self.lb_clase = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Clase:",
        fg_color="transparent"
    )
    self.lb_clase.place(
        relx = 0.03,
        rely = 0.29
    )
    self.et_clase = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "Ingrese la clase del plastico"
    )
    self.et_clase.place(
        relx = 0.11,
        rely = 0.29,
        relwidth = 0.26
    )
    #Label y entry del nombre
    self.lb_nombre = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Nombre:",
        fg_color="transparent"
    )
    self.lb_nombre.place(
        relx = 0.38,
        rely = 0.29
    )
    self.et_nombre = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "Ingrese el nombre del plastico"
    )
    self.et_nombre.place(
        relx = 0.495,
        rely = 0.29,
        relwidth = 0.31
    )
    #Label y entry de la acumulación
    self.lb_acumulacion = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Acumulación:",
        fg_color="transparent"
    )
    self.lb_acumulacion.place(
        relx = 0.03,
        rely = 0.37
    )
    self.et_acumulacion = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "Ingrese donde acumula el plastico"
    )
    self.et_acumulacion.place(
        relx = 0.20,
        rely = 0.37,
        relwidth = 0.33
    )
    #check box de descontinuado
    self.descont_var = ctk.StringVar()
    self.chk_descontinuado = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Descontinuado",
        **style.STYLELABEL,
        variable = self.descont_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_descontinuado.place(
        relx = 0.55,
        rely = 0.375
    )
    #Label y entry del tipo de realce
    self.lb_realce = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Tipo de realce:",
        fg_color="transparent"
    )
    self.lb_realce.place(
        relx = 0.03,
        rely = 0.45
    )
    self.et_realce = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "Ingrese el tipo de realce"
    )
    self.et_realce.place(
        relx = 0.21,
        rely = 0.45,
        relwidth = 0.32
    )
    #Label y entry cantidad minia de pedido
    self.lb_cantidad = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Cantidad min: ",
        fg_color="transparent"
    )
    self.lb_cantidad.place(
        relx = 0.54,
        rely = 0.45
    )
    self.et_cantidad = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "",
        validate = "key",
        validatecommand = (self.controller.register(validations.validate_input_numeric),"%P")
    )
    self.et_cantidad.place(
        relx = 0.71,
        rely = 0.45,
        relwidth = 0.1
    )
    #Label y entry del segmento
    self.lb_segmento = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Segmento:",
        fg_color="transparent"
    )
    self.lb_segmento.place(
        relx = 0.03,
        rely = 0.53
    )
    self.et_segmento = ctk.CTkEntry(
        self.tab_parametros.tab(self.tab1),
        placeholder_text = "Ingrese el segmento"
    )
    self.et_segmento.place(
        relx = 0.165,
        rely = 0.53,
        relwidth = 0.365
    )
    #Label y entry de la FECHA
    
    self.lb_fecha = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= self.fecha.strftime('%d/%m/%Y'),
        fg_color="transparent"
    )
    self.lb_fecha.place(
        relx = 0.60,
        rely = 0.53
    )





    #CheckBoxs y label plantas de producción
    #Label de autorizacion
    self.lb_autorizacion = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "PLANTAS AUTORIZADAS",
        fg_color="transparent"
    )
    self.lb_autorizacion.place(
        relx = 0.35,
        rely = 0.60
    )
    #Label de plantas de produccion IDEMIA
    self.lb_produccion = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Producción IDEMIA: ",
        fg_color="transparent"
    )
    self.lb_produccion.place(
        relx = 0.03,
        rely = 0.65
    )
    #Label de plantas de produccion THALES
    self.lb_produccion = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Producción THALES: ",
        fg_color="transparent"
    )
    self.lb_produccion.place(
        relx = 0.03,
        rely = 0.70
    )
    #Label de plantas de realce de IDEMIA
    self.lb_produccion = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Realce IDEMIA: ",
        fg_color="transparent"
    )
    self.lb_produccion.place(
        relx = 0.03,
        rely = 0.75
    )
    #Label de plantas de realce de THALES
    self.lb_produccion = ctk.CTkLabel(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        text= "Realce THALES: ",
        fg_color="transparent"
    )
    self.lb_produccion.place(
        relx = 0.03,
        rely = 0.80
    )
    #checkBox producción IDEMIA Cali
    self.idemia_produc_cali_var = ctk.StringVar()
    self.chk_idemia_produc_cali = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Cali",
        **style.STYLELABEL,
        variable = self.idemia_produc_cali_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_idemia_produc_cali.place(
        relx = 0.27,
        rely = 0.655
    )
    #checkBox producción THALES IZTAPALAPA
    self.thales_produc_iztapalapa_var = ctk.StringVar()
    self.chk_thales_produc_iztapalapa = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Iztapalapa",
        **style.STYLELABEL,
        variable = self.thales_produc_iztapalapa_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_thales_produc_iztapalapa.place(
        relx = 0.27,
        rely = 0.705
    )
    #checkBox producción THALES ASIA
    self.thales_produc_asia_var = ctk.StringVar()
    self.chk_thales_produc_asia = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Asia",
        **style.STYLELABEL,
        variable = self.thales_produc_asia_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_thales_produc_asia.place(
        relx = 0.44,
        rely = 0.705
    )
    #checkBox realce IDEMIA Cali
    self.idemia_real_cali_var = ctk.StringVar()
    self.chk_idemia_real_cali = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Cali",
        **style.STYLELABEL,
        variable = self.idemia_real_cali_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_idemia_real_cali.place(
        relx = 0.215,
        rely = 0.755
    )
    #checkBox realce IDEMIA BOGOTA
    self.idemia_real_bogo_var = ctk.StringVar()
    self.chk_idemia_real_bogo = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Bogotá",
        **style.STYLELABEL,
        variable = self.idemia_real_bogo_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_idemia_real_bogo.place(
        relx = 0.31,
        rely = 0.755
    )
    #checkBox realce IDEMIA MEDELLIN
    self.idemia_real_mede_var = ctk.StringVar()
    self.chk_idemia_real_mede = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Medellín",
        **style.STYLELABEL,
        variable = self.idemia_real_mede_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_idemia_real_mede.place(
        relx = 0.4425,
        rely = 0.755
    )
    #checkBox realce IDEMIA PEREIRA
    self.idemia_real_pere_var = ctk.StringVar()
    self.chk_idemia_real_pere = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Pereira",
        **style.STYLELABEL,
        variable = self.idemia_real_pere_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_idemia_real_pere.place(
        relx = 0.595,
        rely = 0.755
    )
    #checkBox realce IDEMIA BUCARAMANGA
    self.idemia_real_buca_var = ctk.StringVar()
    self.chk_idemia_real_buca = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Buca.",
        **style.STYLELABEL,
        variable = self.idemia_real_buca_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_idemia_real_buca.place(
        relx = 0.725,
        rely = 0.755
    )
    #checkBox realce IDEMIA BARRANQUILLA   
    self.idemia_real_bquilla_var = ctk.StringVar()
    self.chk_idemia_real_bquilla = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Bquilla.",
        **style.STYLELABEL,
        variable = self.idemia_real_bquilla_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_idemia_real_bquilla.place(
        relx = 0.835,
        rely = 0.755
    )
    #checkBox realce THALES BOGOTA   
    self.thales_real_bogo_var = ctk.StringVar()
    self.chk_thales_real_bogo = ctk.CTkCheckBox(
        self.tab_parametros.tab(self.tab1),
        text = "Bogotá",
        **style.STYLELABEL,
        variable = self.thales_real_bogo_var,
        onvalue= "1",
        offvalue= "0",
        checkbox_width = 20,
        checkbox_height = 20
    )
    self.chk_thales_real_bogo.place(
        relx = 0.215,
        rely = 0.805
    )

    #Textbox de las observaciones
    self.tb_observaciones = ctk.CTkTextbox(
        self.tab_parametros.tab(self.tab1),
        **style.STYLELABEL,
        height=65
    )
    self.tb_observaciones.configure(
        font = ("Calibri Bold", 14)
    ) 
    self.tb_observaciones.place(
        relx = 0.03,
        rely = 0.86,
        relwidth = 0.94
    )

#-------------------------------------------------------------------------
    #Botón que avanza entre los diferentes plasticos
    self.bt_next = ctk.CTkButton(
        self.tab_parametros.tab(self.tab1),
        **style.SMALLBUTTONSTYLE,
        text = ">>",
        command = self.next_con,
        width= 40
    )
    self.bt_next.place(
        relx = 0.905,
        rely = 0.05
    )
    #Botón que retrocede entre los diferentes plasticos
    self.bt_next = ctk.CTkButton(
        self.tab_parametros.tab(self.tab1),
        **style.SMALLBUTTONSTYLE,
        text = "<<",
        command = self.previous_con,
        width= 40
    )
    self.bt_next.place(
        relx = 0.83,
        rely = 0.05
    )
    #Botón que guardar el plastico a la base de datos
    self.bt_load = ctk.CTkButton(
        self.tab_parametros.tab(self.tab1),
        **style.SMALLBUTTONSTYLE,
        text = "Guardar",
        command = self.insert_con,
        width= 90
    )
    self.bt_load.place(
        relx = 0.83,
        rely = 0.19
    )
    #Botón que limpia los widgets
    self.bt_clean = ctk.CTkButton(
        self.tab_parametros.tab(self.tab1),
        **style.SMALLBUTTONSTYLE,
        text = "Limpiar",
        command = self.clean_con,
        width= 90
    )
    self.bt_clean.place(
        relx = 0.83,
        rely = 0.12
    )
    #Botón que busca según el ID en et_id
    self.bt_search = ctk.CTkButton(
        self.tab_parametros.tab(self.tab1),
        **style.SMALLBUTTONSTYLE,
        text = "Buscar",
        command = self.search_by_codinv_con,
        width= 90
    )
    self.bt_search.place(
        relx = 0.83,
        rely = 0.26
    )
    