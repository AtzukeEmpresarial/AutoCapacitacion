#se importan las librerias que nos permiten generar una interfaz grafica
import customtkinter as ctk
import pandas as pd
import datetime as dt
import pyodbc
from tksheet import Sheet

#Se importan valores constantes de nuestra aplicación
from constants import style
from Functions import DBC,validations
from Screens.message.message import confirm_message
from Screens.menu_parameters.plasticos import plastico,insert,next, previous, clean, search_by_codinv,delete_by_codinv, update, ver_plasticos, df_a_excel_plasticos
from Screens.menu_parameters.plantas import plantas,insert_planta,next_planta, previous_planta, clean_planta, search_by_id_planta,delete_by_id_planta, update_planta, ver_plantas, df_a_excel_plantas
from Screens.menu_parameters.proveedores import proveedores, insert_proveedor, next_proveedor, previous_proveedor, clean_proveedor, search_by_id_proveedor, delete_by_id_proveedor, update_proveedor, ver_provedores, df_a_excel_provedores
class menu_parameters(ctk.CTkFrame):
    fecha = dt.date.today()
    ids_plasticos = []
    ids_plantas = []
    ids_proveedores = []
    proveedores = []
    """
    Clase que ejecuta el frame para la parametrización y creación de datos
    importantes para el sistema.
    """
    def __init__(self, parent, controller):
        self.tabla_provedor = False
        self.tabla_planta = False
        self.tabla_plastico = False
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
    def ver_plasticos_con(self):
        """Conecta a la función ver_plasticos en plasticos.py"""
        ver_plasticos(self)
    def df_a_excel_plasticos_con(self):
        """Conecta a la función df_a_excel_plasticos en plasticos.py"""
        df_a_excel_plasticos(self)
#--------------------PLantas------------------------------------
    def insert_planta_con(self):
        """Conecta a la función insert en plantas.py"""
        insert_planta(self)
    def update_planta_con(self):
        """Conecta a la función update en plantas.py"""
        update_planta(self)
    def next_planta_con(self):
        """Conecta a la función next en plantas.py"""
        next_planta(self)
    def previous_planta_con(self):
        """Conecta a la función previous en plantas.py"""
        previous_planta(self)
    def clean_planta_con(self):
        """Conecta a la función clean en plantas.py"""
        clean_planta(self)
    def search_by_id_planta_con(self):
        """Conecta a la función search_by_codinv en plantas.py"""
        search_by_id_planta(self)
    def delete_by_id_planta_con(self):
        """Conecta a la función delete_by_codinv en plantas.py"""
        delete_by_id_planta(self)
    def ver_plantas_con(self):
        """Conecta a la función ver_plantas en plantas.py"""
        ver_plantas(self)
    def df_a_excel_plantas_con(self):
        """Conecta a la función df_a_excel_plantas en plantas.py"""
        df_a_excel_plantas(self)
    #--------------------Proveedores------------------------------------
    def insert_proveedor_con(self):
        """Conecta a la función insert en proveedor.py"""
        insert_proveedor(self)
    def update_proveedor_con(self):
        """Conecta a la función update en proveedor.py"""
        update_proveedor(self)
    def next_proveedor_con(self):
        """Conecta a la función next en proveedor.py"""
        next_proveedor(self)
    def previous_proveedor_con(self):
        """Conecta a la función previous en proveedor.py"""
        previous_proveedor(self)
    def clean_proveedor_con(self):
        """Conecta a la función clean en proveedor.py"""
        clean_proveedor(self)
    def search_by_id_proveedor_con(self):
        """Conecta a la función search_by_codinv en proveedor.py"""
        search_by_id_proveedor(self)
    def delete_by_id_proveedor_con(self):
        """Conecta a la función delete_by_codinv en proveedor.py"""
        delete_by_id_proveedor(self)
    def ver_provedores_con(self):
        """Conecta a la función ver_provedores en proveedor.py"""
        ver_provedores(self)
    def df_a_excel_provedores_con(self):
        """Conecta a la función df_a_excel_provedores en proveedor.py"""
        df_a_excel_provedores(self)

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
        self.tab3 = "Proveedores"
        self.tab4 = "Sucursales"
        self.tab_parametros.add(self.tab1)
        self.tab_parametros.add(self.tab2)
        self.tab_parametros.add(self.tab3)
        self.tab_parametros.add(self.tab4)
        self.tab_parametros.set(self.tab1)
        proveedores(self)
        plantas(self)
        plastico(self)
        self.sucursales()

    def import_file_sucursales(self):
        """
        Funcion encargada de importar el archivo con el las sucursales,
        transforma la fuente de datos de pandas en un dataframe y lo pone en pantalla
        en una tabla con tksheet, posteriormente lo sube a su tabla correspondiente en
        la base de datos (SUCURSALES).
        """
        self.path_sucursales = self.et_sucursales.get()
        self.temp_file_sucursales = DBC.import_from_excel(self, self.path_sucursales, "Sucursales")
        self.df_excel_sucursales = pd.DataFrame(self.temp_file_sucursales)
        #Tabla en la cual se colocan los datos
        self.sheet_sucursales = Sheet(
            self.tab_parametros.tab(self.tab4),
            data = self.df_excel_sucursales.values.tolist(),
            headers= self.df_excel_sucursales.columns.tolist(),
            show_x_scrollbar= True,
            font = style.FONT_NORMAL, 
            header_font = style.FONT_NORMAL
        )
        self.sheet_sucursales.place(
            relx = 0.03,
            rely = 0.3,
            relwidth = 0.95,
            relheight = 0.7
        )
        #Botón que carga las sucursales en la tabla SUCURSALES
        self.bt_reload_sucursales = ctk.CTkButton(
            self.tab_parametros.tab(self.tab4),
            **style.SMALLBUTTONSTYLE,
            text = "Subir",
            command = self.load_sucursales
        )
        self.bt_reload_sucursales.place(
            relx = 0.37,
            rely = 0.19
        )

    def load_sucursales(self):
        """Carga elas sucursales en la tabla correspondiente de la base de datos"""
        DBC.load_in_sucursales(self, self.cnx_nac, self.df_excel_sucursales)

    def find_file_sucurales(self):
        """
        Abre una nueva ventana de busqueda local para indicar la
        dirección del archivo deseado.
        """
        path_sucursales = ctk.filedialog.askopenfilename()
        self.et_sucursales.delete(0, ctk.END)
        self.et_sucursales.insert(0,path_sucursales)


    def sucursales(self):
        #Inicia el entri donde se colocará la dirección del archivo
        self.et_sucursales = ctk.CTkEntry(
            self.tab_parametros.tab(self.tab4),
            placeholder_text = "Ingrese la dirección del archivo o seleccionelo con el botón Explorar"
        )
        self.et_sucursales.place(
            relx = 0.2,
            rely = 0.01,
            relwidth = 0.6
        )
        #Label del entry de dirección de archivo
        self.lb_sucursales = ctk.CTkLabel(
            self.tab_parametros.tab(self.tab4),
            **style.STYLELABEL,
            text= "Sucursales:",
            fg_color="transparent"
        )
        self.lb_sucursales.place(
            relx = 0.03,
            rely = 0.01
        )
        #Botón que ejecuta el buscador de archivos.
        self.bt_sucursales = ctk.CTkButton(
            self.tab_parametros.tab(self.tab4),
            **style.SMALLBUTTONSTYLE,
            text = "Explorar",
            command = self.find_file_sucurales,
            width = 100,
            height= 26
        )
        self.bt_sucursales.place(
            relx = 0.82,
            rely = 0.0095
        )
        #Botón que carga el archivo indicado en la ruta.
        self.bt_load_sucursales = ctk.CTkButton(
            self.tab_parametros.tab(self.tab4),
            **style.SMALLBUTTONSTYLE,
            text = "Importar",
            command = self.import_file_sucursales
        )
        self.bt_load_sucursales.place(
            relx = 0.03,
            rely = 0.11
        )

        
        







        
        

