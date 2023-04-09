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

class menu_process(ctk.CTkFrame):
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
        #Lista que contiene los consecutivos
        self.ls_pedidos = []
        self.ls_pedidos_idemia = []
        self.ls_proveedores = []
        self.ls_plantas = []
        self.ls_plantas_produccion = []
        #cargamos las listas
        self.ls_plasticos = DBC.find_indexes(self.cnx_nac,"NOMBRE", "PLASTICOS").to_list()
        self.ls_plasticos.sort()
        #self.ls_plasticos = list(set(self.ls_plasticos))
        self.ls_plantas = DBC.find_indexes_where_int(self.cnx_nac,"UBICACION","PLANTAS","PRODUCCION",0).to_list()
        self.ls_plantas.sort()
        self.ls_plantas = list(set(self.ls_plantas))
        self.ls_plantas_produccion = DBC.find_indexes_where_int(self.cnx_nac,"UBICACION","PLANTAS","PRODUCCION", 1).to_list()
        self.ls_plantas_produccion.sort()
        self.ls_plantas_produccion = list(set(self.ls_plantas_produccion))
        self.ls_proveedores = DBC.find_indexes(self.cnx_nac,"NOMBRE","PROVEEDORES").to_list()
        self.ls_proveedores.sort()
        self.ls_proveedores = list(set(self.ls_proveedores))
        #variable de confirmaciín
        self.cfm = False
        #Variable que guarda el estado de la tabla de pendientes
        self.tabla = False
        self.init_tabview()
        self.entrada_semanal()
        self.descarga_diaria()
        self.inventario_0()
        self.traslados()
        self.pedidos()
        self.inventarios()
        self.anadir()

#_______________________Tabview________________________________________________________

    def init_tabview(self):
        """
        Inicia el widget de pestañas, este contiene los diferentes procesos de datos
        """
        self.tab_alimentar = ctk.CTkTabview(
            self,
            segmented_button_selected_hover_color = style.BLUE,
            segmented_button_selected_color= style.DARKBLUE
        )
        self.tab_alimentar.pack(
            anchor = ctk.N,
            padx=20, 
            pady=20, 
            fill = ctk.BOTH,
            expand = True
        )
        self.tab1 = "Carga diaria"
        self.tab2 = "Reporte semanal"
        self.tab3 = "Inventario 0"
        self.tab4 = "Traslados"
        self.tab5 = "Pedidos"
        self.tab6 = "Items de inventario"
        self.tab7 = "Inventarios"
        self.tab_alimentar.add(self.tab6)
        self.tab_alimentar.add(self.tab1)
        self.tab_alimentar.add(self.tab2)
        self.tab_alimentar.add(self.tab3)
        self.tab_alimentar.add(self.tab4)
        self.tab_alimentar.add(self.tab5)
        self.tab_alimentar.add(self.tab7)
        self.tab_alimentar.set(self.tab6)



#______________________Alimentar inventario diario_________________________________
    def descargaGNPLA (self):
        """Descarga y organiza toda la informaciíon del GNPLA correspondiente a los
        realces del día seleccionado, requiere:
        user: nombre de usuario del operador que ingresó al programa
        password: contraseña que ingresó el operador al acceder al programa
        date: fecha de la cual desea obtener el realce.
        """
        #reseteamos la hoja de calculo
        if self.count == 1:
            self.tab_plantas.destroy()
        self.count = 1
        #creamos los dataframes que contendrán la info del día realce
        self.df_thales_agrupado = pd.DataFrame()
        self.df_idemia_agrupado = pd.DataFrame()
        #Creamos una lista con los pedidos de hoy
        self.ls_pedidos_idemia[:] = []
        if len(self.et_pedido_thales.get()) != 0:
            self.pedido_thales = int(self.et_pedido_thales.get())
        else:
            self.pedido_thales = self.ls_pedidos[0]+1
        if len(self.et_pedido_idemia.get()) != 0:
            for i in range(1, int(self.et_numero_pedidos.get())+1):
                if i == 1:
                    self.ls_pedidos_idemia.append(int(self.et_pedido_idemia.get()))
                else:
                    self.ls_pedidos_idemia.append(int(self.et_pedido_idemia.get())+i-1)
        else:
            for i in range(1, int(self.et_numero_pedidos.get())+1):
                self.ls_pedidos_idemia.append(self.ls_pedidos[1]+i)
        print(self.ls_pedidos)
        print(self.pedido_thales)
        print(self.ls_pedidos_idemia)

        self.alerta = DBC.daily(self, self.cnx_nac,self.calendario.get_date(), self.pedido_thales, self.ls_pedidos_idemia)
        #Se crea un tabView para las dos tablas (thales e idemia)
        self.tab_plantas = ctk.CTkTabview(
            self.tab_alimentar.tab(self.tab1),
            segmented_button_selected_hover_color = style.BLUE,
            segmented_button_selected_color= style.DARKBLUE
        )
        self.tab_plantas.pack(
            anchor = ctk.N,
            padx=20, 
            pady=[280,10], 
            fill = ctk.BOTH,
            expand = True
        )
        self.tab11 = "Thales"
        self.tab22 = "Idemia"
        self.tab_plantas.add(self.tab11)
        self.tab_plantas.add(self.tab22)
        self.tab_plantas.set(self.tab11)
        #Tabla en la cual se colocan los datos de thales
        self.sheet_daily = Sheet(
            self.tab_plantas.tab(self.tab11),
            data = self.df_thales_agrupado.values.tolist(),
            headers = self.df_thales_agrupado.columns.tolist(),
            show_x_scrollbar= True,
            show_y_scrollbar= True, 
            font = style.FONT_NORMAL,
            header_font = style.FONT_NORMAL
        )
        self.sheet_daily.place(
            relx = 0.03,
            rely = 0.05,
            relwidth = 0.95,
            relheight = 0.95
        )

        #Tabla en la cual se colocan los datos de Idemia
        self.sheet_daily = Sheet(
            self.tab_plantas.tab(self.tab22),
            data = self.df_idemia_agrupado.values.tolist(),
            headers = self.df_idemia_agrupado.columns.tolist(),
            show_x_scrollbar= True,
            show_y_scrollbar= True, 
            font = style.FONT_NORMAL, 
            header_font = style.FONT_NORMAL
        )
        self.sheet_daily.place(
            relx = 0.03,
            rely = 0.05,
            relwidth = 0.95,
            relheight = 0.95
        )
        if self.alerta:
            #Label que alerta de la existencia de manillas y/o stickers en IDEMIA
            self.lb_alerta = ctk.CTkLabel(
                self.tab_alimentar.tab(self.tab1),
                **style.STYLELABEL,
                text= "CUIDADO, HAY MANILLAS \nY STICKERS EN IDEMIA",
                fg_color="transparent"
            )
            self.lb_alerta.place(
                relx = 0.62,
                rely = 0.23
            )
        #Botón que ejecuta la alimentación de inventario
        self.bt_file = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab1),
            **style.SMALLBUTTONSTYLE,
            text = "Cargar",
            command = self.cargar,
            width = 100,
            height= 26
        )
        self.bt_file.place(
            relx = 0.7,
            rely = 0.4
        )
    
    def cargar (self):
        DBC.alimentar_inventario(self, self.cnx_nac, self.df_thales_agrupado, self.df_idemia_agrupado, self.calendario.get_date())
        DBC.actualizar_ultimo_pedido_thales_idemia(self, self.cnx_nac, self.pedido_thales, self.ls_pedidos_idemia[-1])
        self.lb_ultimo_thales_codigo.configure(text = str(self.pedido_thales))
        self.lb_ultimo_idemia_codigo.configure(text = str(self.ls_pedidos_idemia[-1]))


    def descarga_diaria (self):
        """Se cargan los widgets necesarios en la pestaña 1 del tab view"""
        #Label de la fecha
        self.lb_cargar = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab1),
            **style.STYLELABEL,
            text= "Selecciona la fecha que se desea cargar:",
            fg_color="transparent"
        )
        self.lb_cargar.pack(
            anchor = ctk.N,
            pady = [10,0]
        )
        #actualiza la lista que contiene los ultimos consecutivos
        DBC.consultar_ultimo_pedido_thales_idemia(self, self.cnx_nac)
        #Labels y entry del ultimo consecutivo de Thales
        self.lb_ultimo_thales = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab1),
            **style.STYLELABEL,
            text= "Ultimo pedido\nTHALES",
            fg_color="transparent"
        )
        self.lb_ultimo_thales.place(
            relx = 0,
            rely = 0.02
        )
        self.lb_ultimo_thales_codigo = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab1),
            **style.STYLELABEL,
            text= str(self.ls_pedidos[0]),
            fg_color="transparent"
        )
        self.lb_ultimo_thales_codigo.place(
            relx = 0.065,
            rely = 0.12
        )
        self.et_pedido_thales = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab1),
            placeholder_text = "Pedido inicial T"
        )
        self.et_pedido_thales.place(
            relx = 0,
            rely = 0.17,
            relwidth = 0.17,
            relheight = 0.05
        )
        #Labels y entry del ultimo consecutivo de IDEMIA
        self.lb_ultimo_idemia = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab1),
            **style.STYLELABEL,
            text= "Ultimo pedido\nIDEMIA",
            fg_color="transparent"
        )
        self.lb_ultimo_idemia.place(
            relx = 0,
            rely = 0.22
        )
        self.lb_ultimo_idemia_codigo = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab1),
            **style.STYLELABEL,
            text= str(self.ls_pedidos[1]),
            fg_color="transparent"
        )
        self.lb_ultimo_idemia_codigo.place(
            relx = 0.055,
            rely = 0.32
        )
        self.et_pedido_idemia = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab1),
            placeholder_text = "Pedido inicial I"
        )
        self.et_pedido_idemia.place(
            relx = 0,
            rely = 0.37,
            relwidth = 0.17,
            relheight = 0.05
        )
        #Label y entry de pedido a consultar
        self.lb_numero_pedidos = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab1),
            **style.STYLELABEL,
            text= "# Pedidos\na consultar",
            fg_color="transparent"
        )
        self.lb_numero_pedidos.place(
            relx = 0.52,
            rely = 0.1
        )
        self.et_numero_pedidos = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab1),
            placeholder_text = "#"
        )
        self.et_numero_pedidos.delete(0, ctk.END)
        self.et_numero_pedidos.insert(0, str(4))
        self.et_numero_pedidos.place(
            relx = 0.57,
            rely = 0.2,
            relwidth = 0.03,
            relheight = 0.06
        )

        #Calendario para seleccionar la fecha
        self.calendario = Calendar(
            self.tab_alimentar.tab(self.tab1), 
            selectmode='day', 
            font=style.FONT_LINT,
            showweeknumbers=False, 
            cursor="hand2", 
            date_pattern= 'ymmdd',
            borderwidth=0, 
            bordercolor='white',
            locale='es_ES'
        )
        self.calendario.place_configure(
            relx = 0.20,
            rely = 0.1
        )
        #Botón que ejecuta la Consulta de datos para la carga
        self.bt_file = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab1),
            **style.SMALLBUTTONSTYLE,
            text = "Consultar",
            command = self.descargaGNPLA,
            width = 100,
            height= 26
        )
        self.bt_file.place(
            relx = 0.70,
            rely = 0.11
        )





#___________________Entrada semanal____________________________________________________________
    def import_file(self):
        """
        Funcion encargada de importar la alimentación del inventario,
        transforma la fuente de datos de pandas en un dataframe y lo pone en pantalla
        en una tabla con tksheet.
        """
        self.path = self.et_file.get()
        self.temp_file = DBC.import_from_excel(self, self.path, "Feb 06")
        self.df_excel = pd.DataFrame(self.temp_file)
        self.df_excel["SEMANAS INVENTARIO"] = pd.Series([round(val,2) for val in self.df_excel["SEMANAS INVENTARIO"]]) 
        #Tabla en la cual se colocan los datos
        self.sheet = Sheet(
            self.tab_alimentar.tab(self.tab2),
            data = self.df_excel.values.tolist(),
            headers= self.df_excel.columns.tolist(),
            show_x_scrollbar= True,
            font = style.FONT_NORMAL, 
            header_font = style.FONT_NORMAL
        )
        self.sheet.place(
            relx = 0.03,
            rely = 0.3,
            relwidth = 0.95,
            relheight = 0.7
        )

    def find_file(self):
        """Abre una nueva ventana de busqueda local para indicar la
        dirección del archivo deseado.
        """
        path = ctk.filedialog.askopenfilename()
        self.et_file.delete(0, ctk.END)
        self.et_file.insert(0,path)
    
    def load_inventarios(self):
        """Carga el inventario 0 en la tabla correspondiente de la base de datos"""
        DBC.load_in_inventariostj(self, self.cnx_nac, self.df_excel_0)


    def entrada_semanal(self):
        #Inicia el entri donde se colocará la dirección del archivo
        self.et_file = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab2),
            placeholder_text = "Ingrese la dirección del archivo o seleccionelo con el botón Explorar"
        )
        self.et_file.place(
            relx = 0.15,
            rely = 0.01,
            relwidth = 0.65
        )
        #Label del entry de dirección de archivo
        self.lb_file = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab2),
            **style.STYLELABEL,
            text= "Archivo:",
            fg_color="transparent"
        )
        self.lb_file.place(
            relx = 0.03,
            rely = 0.01
        )
        #Botón que ejecuta el buscador de archivos.
        self.bt_file = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab2),
            **style.SMALLBUTTONSTYLE,
            text = "Explorar",
            command = self.find_file,
            width = 100,
            height= 26
        )
        self.bt_file.place(
            relx = 0.82,
            rely = 0.0095
        )
        #Botón que carga el archivo indicado en la ruta.
        self.bt_load = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab2),
            **style.SMALLBUTTONSTYLE,
            text = "Importar",
            command = self.import_file
        )
        self.bt_load.place(
            relx = 0.03,
            rely = 0.11
        )




#___________________Inventario 0____________________________________________________________
    def import_file_0(self):
        """
        Funcion encargada de importar el archivo con el inventario 0,
        transforma la fuente de datos de pandas en un dataframe y lo pone en pantalla
        en una tabla con tksheet, posteriormente lo sube a su tabla correspondiente en
        la base de datos (INVENTARIOTJ).
        """
        self.path_0 = self.et_file_0.get()
        self.temp_file_0 = DBC.import_from_excel(self, self.path_0, self.et_hoja.get())
        self.df_excel_0 = pd.DataFrame(self.temp_file_0)
        #Tabla en la cual se colocan los datos
        self.sheet_0 = Sheet(
            self.tab_alimentar.tab(self.tab3),
            data = self.df_excel_0.values.tolist(),
            headers= self.df_excel_0.columns.tolist(),
            show_x_scrollbar= True,
            font = style.FONT_NORMAL, 
            header_font = style.FONT_NORMAL
        )
        self.sheet_0.place(
            relx = 0.03,
            rely = 0.3,
            relwidth = 0.95,
            relheight = 0.7
        )
        #Botón que carga el inventario 0 en la tabla INVENTARIOTJ
        self.bt_reload_0 = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab3),
            **style.SMALLBUTTONSTYLE,
            text = "Subir",
            command = self.load_inventarios
        )
        self.bt_reload_0.place(
            relx = 0.37,
            rely = 0.19
        )

    def find_file_0(self):
        """
        Abre una nueva ventana de busqueda local para indicar la
        dirección del archivo deseado.
        """
        path_0 = ctk.filedialog.askopenfilename()
        self.et_file_0.delete(0, ctk.END)
        self.et_file_0.insert(0,path_0)


    def inventario_0(self):
        #Inicia el entri donde se colocará la dirección del archivo
        self.et_file_0 = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab3),
            placeholder_text = "Ingrese la dirección del archivo o seleccionelo con el botón Explorar"
        )
        self.et_file_0.place(
            relx = 0.15,
            rely = 0.01,
            relwidth = 0.65
        )
        #Label del entry de dirección de archivo
        self.lb_file_0 = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab3),
            **style.STYLELABEL,
            text= "Archivo:",
            fg_color="transparent"
        )
        self.lb_file_0.place(
            relx = 0.03,
            rely = 0.01
        )
        #Botón que ejecuta el buscador de archivos.
        self.bt_file_0 = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab3),
            **style.SMALLBUTTONSTYLE,
            text = "Explorar",
            command = self.find_file_0,
            width = 100,
            height= 26
        )
        self.bt_file_0.place(
            relx = 0.82,
            rely = 0.0095
        )
        #Botón que carga el archivo indicado en la ruta.
        self.bt_load_0 = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab3),
            **style.SMALLBUTTONSTYLE,
            text = "Importar",
            command = self.import_file_0
        )
        self.bt_load_0.place(
            relx = 0.03,
            rely = 0.11
        )
        #Label del entry de hoja
        self.lb_hoja = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab3),
            **style.STYLELABEL,
            text= "Nombre de Hoja(Fecha): ",
            fg_color="transparent"
        )
        self.lb_hoja.place(
            relx = 0.30,
            rely = 0.115
        )
        #Entry de la hoja
        self.et_hoja = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab3),
            placeholder_text = "yyyymmdd"
        )
        self.et_hoja.place(
            relx = 0.62,
            rely = 0.115,
            relwidth = 0.20
        )




#________________________Traslados_________________________________________________________
    def traslados(self):
        #Label y Combobox de la planta de salida
        self.lb_planta_salida = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab4),
            **style.STYLELABEL,
            text= "Planta de salida",
            fg_color="transparent"
        )
        self.lb_planta_salida.place(
            relx = 0.08,
            rely = 0
        )
        self.planta_salida_var = ctk.StringVar()
        self.cb_planta_salida = ctk.CTkComboBox(
            self.tab_alimentar.tab(self.tab4),
            values = self.ls_plantas,
            variable = self.planta_salida_var
        )
        self.cb_planta_salida.place(
            relx = 0.075,
            rely = 0.08,
            relwidth = 0.20
        )
        #label y Calendario para seleccionar la fecha de salida
        self.lb_fecha_salida = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab4),
            **style.STYLELABEL,
            text= "Fecha de salida",
            fg_color="transparent"
        )
        self.lb_fecha_salida.place(
            relx = 0.09,
            rely = 0.17
        )
        self.calendario_salida = Calendar(
            self.tab_alimentar.tab(self.tab4), 
            selectmode='day', 
            font=style.FONT_LINT,
            showweeknumbers=False, 
            cursor="hand2", 
            date_pattern= 'ymmdd',
            borderwidth=0, 
            bordercolor='white',
            locale='es_ES'
            
        )
        self.calendario_salida.place_configure(
            relx = 0.03,
            rely = 0.25
        )
        #Label y Combobox de la planta final
        self.lb_planta_final = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab4),
            **style.STYLELABEL,
            text= "Planta final",
            fg_color="transparent"
        )
        self.lb_planta_final.place(
            relx = 0.73,
            rely = 0
        )
        self.planta_final_var = ctk.StringVar()
        self.cb_planta_final = ctk.CTkComboBox(
            self.tab_alimentar.tab(self.tab4),
            values = self.ls_plantas,
            variable = self.planta_final_var
        )
        self.cb_planta_final.place(
            relx = 0.70,
            rely = 0.08,
            relwidth = 0.20
        )
        #label y Calendario para seleccionar la fecha de llegada
        self.lb_fecha_llegada = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab4),
            **style.STYLELABEL,
            text= "Fecha de llegada",
            fg_color="transparent"
        )
        self.lb_fecha_llegada.place(
            relx = 0.715,
            rely = 0.17
        )
        self.calendario_llegada = Calendar(
            self.tab_alimentar.tab(self.tab4), 
            selectmode='day', 
            font=style.FONT_LINT,
            showweeknumbers=False, 
            cursor="hand2", 
            date_pattern= 'ymmdd',
            borderwidth=0, 
            bordercolor='white',
            locale='es_ES'
        )
        self.calendario_llegada.place_configure(
            relx = 0.65,
            rely = 0.25
        )
        #Label y Combobox del provedor
        self.lb_operador_traslado = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab4),
            **style.STYLELABEL,
            text= "Provedor",
            fg_color="transparent"
        )
        self.lb_operador_traslado.place(
            relx = 0.44,
            rely = 0
        )
        self.operador_traslado_var = ctk.StringVar()
        self.cb_operador_traslado = ctk.CTkComboBox(
            self.tab_alimentar.tab(self.tab4),
            values = self.ls_proveedores,
            variable = self.operador_traslado_var
        )
        self.cb_operador_traslado.place(
            relx = 0.40,
            rely = 0.08,
            relwidth = 0.20
        )
        #Label y entry (no activo) de la ID del traslado
        self.lb_id_traslado = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab4),
            **style.STYLELABEL,
            text= "ID traslado",
            fg_color="transparent"
        )
        self.lb_id_traslado.place(
            relx = 0.43,
            rely = 0.17
        )
        self.et_id_traslado = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab4),
            placeholder_text = "ID"
        )
        self.et_id_traslado.place(
            relx = 0.46,
            rely = 0.23,
            relwidth = 0.06
        )
        #Label y entry del CODINV del plastico a hacer traspaso
        self.lb_CODINV_traslado = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab4),
            **style.STYLELABEL,
            text= "CODINV",
            fg_color="transparent"
        )
        self.lb_CODINV_traslado.place(
            relx = 0.44,
            rely = 0.31
        )
        self.et_CODINV_traslado = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab4),
            placeholder_text = ""
        )
        self.et_CODINV_traslado.place(
            relx = 0.46,
            rely = 0.37,
            relwidth = 0.06
        )
        #Label y entry de la cantidad del plastico a hacer traspaso
        self.lb_cantidad_traslado = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab4),
            **style.STYLELABEL,
            text= "Cantidad",
            fg_color="transparent"
        )
        self.lb_cantidad_traslado.place(
            relx = 0.445,
            rely = 0.45
        )
        self.et_cantidad_traslado = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab4),
            placeholder_text = ""
        )
        self.et_cantidad_traslado.place(
            relx = 0.4,
            rely = 0.50,
            relwidth = 0.2
        )
        #Botón que busca según el ID de la planta en PLANTAS
        self.bt_search_traslado = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab4),
            **style.SMALLBUTTONSTYLE,
            text = "Buscar",
            command = self.search_by_id_traslado ,
            width= 90
        )
        self.bt_search_traslado.place(
            relx = 0,
            rely = 0.8
        )
        #Botón que registra el traslado y lo deja como incompleto.
        self.bt_insert_traslado = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab4),
            **style.SMALLBUTTONSTYLE,
            text = "Registrar",
            command = self.insert_traslado ,
            width= 90
        )
        self.bt_insert_traslado.place(
            relx = 0.15,
            rely = 0.8
        )
        #Botón que limpia los widgets de traslado
        self.bt_clean_traslado = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab4),
            **style.SMALLBUTTONSTYLE,
            text = "Limpiar",
            command = self.clean_traslado ,
            width= 90
        )
        self.bt_clean_traslado.place(
            relx = 0.30,
            rely = 0.8
        )
        #Botón que elimina un traslado
        self.bt_delete_traslado = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab4),
            **style.SMALLBUTTONSTYLE,
            text = "Eliminar",
            command = self.eliminar_traslado,
            width= 90
        )
        self.bt_delete_traslado.place(
            relx = 0.45,
            rely = 0.8
        )
        #Botón que completa un traslado
        self.bt_delete_traslado = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab4),
            **style.SMALLBUTTONSTYLE,
            text = "Completar",
            command = self.completar_traslado,
            width= 90
        )
        self.bt_delete_traslado.place(
            relx = 0.60,
            rely = 0.8
        )
        #Botón que muestra los traslados pendientes
        self.bt_pendiente_traslado = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab4),
            **style.SMALLBUTTONSTYLE,
            text = "Pendientes",
            command = self.traslados_pendientes,
            width= 90
        )
        self.bt_pendiente_traslado.place(
            relx = 0.775,
            rely = 0.8
        )

    def search_by_id_traslado(self):
        ''' Función que carga los datos de una traslado según el ID'''
        traslados_df = DBC.find_by_id_traslados(self, self.cnx_nac, int(self.et_id_traslado.get()))
        try:
            self.load_in_widgets_planta(traslados_df)# type: ignore
        except Exception:
            self.login_message = alert_message(self,self, "No existe el registro asociado a esa ID\npor favor verifique su conexión y el ID solicitado")

    def load_in_widgets_planta(self, df: pd.DataFrame):
        '''Carga la información contenida en un dataframe en los widgets de traslados,
        recibe:
        self = Frame padre
        df = Dataframe con los datos de la planta'''
        self.planta_salida_var.set("")
        self.planta_final_var.set("")
        self.operador_traslado_var.set("")
        self.et_id_traslado.delete(0, ctk.END)
        self.et_CODINV_traslado.delete(0, ctk.END)
        self.et_cantidad_traslado.delete(0, ctk.END)
        self.calendario_salida.selection_clear()
        self.calendario_llegada.selection_clear()

        self.planta_salida_var.set(str(df.loc[0,"PLANTA"]))
        self.planta_final_var.set(str(df.loc[0,"PLANTAFINAL"]))
        self.operador_traslado_var.set(str(df.loc[0,"PROVEEDOR"]))
        self.et_id_traslado.insert(0, str(df.loc[0,"ID"]))
        self.et_CODINV_traslado.insert(0, str(df.loc[0,"CODINV"]))
        self.et_cantidad_traslado.insert(0, str(df.loc[0,"CANTIDAD"]))
        fecha = df.loc[0,"FECHA"]
        self.calendario_salida.selection_set(dt.datetime.strptime(fecha, "%Y%m%d")) # type: ignore
        fecha_llegada = df.loc[0,"FECHALLEGADA"]
        self.calendario_llegada.selection_set(dt.datetime.strptime(fecha_llegada, "%Y%m%d")) # type: ignore

    def insert_traslado(self):
        ''' Función que se encarga de guardar los datos ingresados en los campos de
        creación de plantas; guarda en un diccionario los datos en los entry
        para convertirlo en un DataFrame y posteriormente enviarlo a la función
        de la ODBC que guarda las plantas.'''

        self.confirm_action("¿Seguro que desea crear este registro?")

        cantidad = DBC.consultar_cantidad(self, self.cnx_nac, int(self.et_CODINV_traslado.get()), self.cb_planta_salida.get(),self.cb_operador_traslado.get())

        if int(self.et_cantidad_traslado.get()) <= cantidad: # type: ignore
            if self.cfm:
                traslados_dic = {
                    'CODINV' : [int(self.et_CODINV_traslado.get())],
                    'PROVEEDOR' : [self.cb_operador_traslado.get()],
                    'PLANTA' : [self.cb_planta_salida.get()],
                    'PLANTAFINAL' : [self.cb_planta_final.get()],
                    'IDTIPOMOV' : [2],
                    'FECHA' : [self.calendario_salida.get_date()],
                    'FECHALLEGADA' : [self.calendario_llegada.get_date()],
                    'CANTIDAD' : [int(self.et_cantidad_traslado.get())],
                    'COMPLETO' : [0]
                }
                traslados_df = pd.DataFrame(traslados_dic)
                DBC.insert(self, self.cnx_nac,traslados_df,"MOVIMIENTOS")
                DBC.traslado_salida(self, self.cnx_nac, int(self.et_CODINV_traslado.get()), self.cb_planta_salida.get(), self.cb_operador_traslado.get(),int(self.et_cantidad_traslado.get()))
                self.clean_traslado()
                self.cfm = False
        else: 
            self.login_message = alert_message(self,self, "La cantidad de plasticos supera el numero de plasticos actuales\n en la planta de salida, por favor verifique el traslado.")

    def confirm_action(self, message):
        """Genera un cuadro de alerta donde se pide confirmar la acción para continuar,
        este cambia la variable cfm del frame principal"""
        self.message = confirm_message(self, self.controller, message)  
    
    def clean_traslado (self):
        '''Limpia la información de los widgets de plasticos'''
        self.planta_salida_var.set("")
        self.planta_final_var.set("")
        self.operador_traslado_var.set("")
        self.et_id_traslado.delete(0, ctk.END)
        self.et_CODINV_traslado.delete(0, ctk.END)
        self.et_cantidad_traslado.delete(0, ctk.END)
        self.calendario_salida.selection_clear()
        self.calendario_llegada.selection_clear()
    
    def eliminar_traslado(self):
        '''Función que se encarga de eliminar un traslado según su ID 
        y revertir sus modificaciones al inventario'''
        self.confirm_action("¿Está seguro que desea Eliminar este registro de Forma permanente?")


        if self.cfm:
            DBC.deshacer_traslado_salida(self, self.cnx_nac, int(self.et_CODINV_traslado.get()), self.cb_planta_salida.get(), self.cb_operador_traslado.get(),int(self.et_cantidad_traslado.get()))
            DBC.delete(self, self.cnx_nac,"ID", int(self.et_id_traslado.get()), "MOVIMIENTOS")
            self.clean_traslado()
    
    def completar_traslado(self):
        """Función que se encarga de completar el traslado una vez sea correctamente
        efectuado, esto volverá el registro invisible para el usuario y se añadirán
        los plasticos al inventario de la planta final"""
        self.confirm_action("¿Está seguro que desea marcar como COMPLETO este traslado?")
        if self.cfm:
            DBC.marcar_traslado_completo(self, self.cnx_nac, int(self.et_id_traslado.get()), self.calendario_llegada.get_date())
            DBC.deshacer_traslado_salida(self, self.cnx_nac, int(self.et_CODINV_traslado.get()), self.cb_planta_final.get(), self.cb_operador_traslado.get(),int(self.et_cantidad_traslado.get()))
            self.login_message = alert_message(self,self, "Se completó el traslado con exito.")
            self.clean_traslado()
    
    def traslados_pendientes(self):
        """Genera una hoja de calculo sobre los demás widgets que nos muestras
        todos los traslados pendientes"""
        if not self.tabla:
            self.df_pendientes = DBC.Traslados_pendientes(self, self.cnx_nac)
            #Tabla en la cual se colocan los datos
            self.sheet_traslados_pendientes = Sheet(
                self.tab_alimentar.tab(self.tab4),
                data = self.df_pendientes.values.tolist(),# type: ignore
                headers= self.df_pendientes.columns.tolist(),# type: ignore
                show_x_scrollbar= True,
                font = style.FONT_NORMAL, 
                header_font = style.FONT_NORMAL
            )
            self.sheet_traslados_pendientes.place(
                relx = 0,
                rely = 0,
                relwidth = 1,
                relheight = 0.75
            )
            self.tabla = True
        else:
            self.sheet_traslados_pendientes.destroy()
            self.tabla = False






#________________________PEDIDOS_________________________________________________________
    def pedidos(self):
        #Label y entry del ID del pedido
        self.lb_id_pedido = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "ID pedido",
            fg_color="transparent"
        )
        self.lb_id_pedido.place(
            relx = 0.055,
            rely = 0
        )
        self.et_id_pedido = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab5),
            placeholder_text = "ID"
        )
        self.et_id_pedido.place(
            relx = 0.075,
            rely = 0.08,
            relwidth = 0.06
        )
        #Label y Combobox del provedor
        self.lb_operador_pedido = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Provedor",
            fg_color="transparent"
        )
        self.lb_operador_pedido.place(
            relx = 0.20,
            rely = 0
        )
        self.operador_pedido_var = ctk.StringVar()
        self.cb_operador_pedido = ctk.CTkComboBox(
            self.tab_alimentar.tab(self.tab5),
            values = self.ls_proveedores,
            variable = self.operador_pedido_var
        )
        self.cb_operador_pedido.place(
            relx = 0.16,
            rely = 0.08,
            relwidth = 0.20
        )
        #Label y Combobox de la planta final pedido
        self.lb_planta_final_pedido = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Planta final",
            fg_color="transparent"
        )
        self.lb_planta_final_pedido.place(
            relx = 0.40,
            rely = 0
        )
        self.planta_final_pedido_var = ctk.StringVar()
        self.cb_planta_final_pedido = ctk.CTkComboBox(
            self.tab_alimentar.tab(self.tab5),
            values = self.ls_plantas,
            variable = self.planta_final_pedido_var
        )
        self.cb_planta_final_pedido.place(
            relx = 0.37,
            rely = 0.08,
            relwidth = 0.20
        )
        #Label y Combobox de la planta de producción pedido
        self.lb_planta_produc_pedido = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Planta produc.",
            fg_color="transparent"
        )
        self.lb_planta_produc_pedido.place(
            relx = 0.59,
            rely = 0
        )
        self.planta_produc_pedido_var = ctk.StringVar()
        self.cb_planta_produc_pedido = ctk.CTkComboBox(
            self.tab_alimentar.tab(self.tab5),
            values = self.ls_plantas_produccion,
            variable = self.planta_produc_pedido_var
        )
        self.cb_planta_produc_pedido.place(
            relx = 0.58,
            rely = 0.08,
            relwidth = 0.20
        )
        #Label y entry del CODINV del plastico del cual se hace el pedido
        self.lb_CODINV_pedido = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "CODINV",
            fg_color="transparent"
        )
        self.lb_CODINV_pedido.place(
            relx = 0.77,
            rely = 0
        )
        self.et_CODINV_pedido = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab5),
            placeholder_text = ""
        )
        self.et_CODINV_pedido.place(
            relx = 0.79,
            rely = 0.08,
            relwidth = 0.06
        )
        #label y Calendario para seleccionar la fecha de pedido
        self.lb_fecha_pedido = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Fecha de pedido",
            fg_color="transparent"
        )
        self.lb_fecha_pedido.place(
            relx = 0.09,
            rely = 0.15
        )
        self.calendario_pedido = Calendar(
            self.tab_alimentar.tab(self.tab5), 
            selectmode='day', 
            font=style.FONT_LINT,
            showweeknumbers=False, 
            cursor="hand2", 
            date_pattern= 'ymmdd',
            borderwidth=0, 
            bordercolor='white',
            locale='es_ES'
            
        )
        self.calendario_pedido.place_configure(
            relx = 0.03,
            rely = 0.205
        )
        #Label con el TRM
        self.trm = DBC.TRM(self)
        self.lb_trm_pedido = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "TRM\n" + str(self.trm),
            fg_color="transparent"
        )
        self.lb_trm_pedido.place(
            relx = 0.40,
            rely = 0.17
        )
        #label y Calendario para seleccionar la fecha estimada de llegada
        self.lb_fecha_estimada = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Fecha estimada",
            fg_color="transparent"
        )
        self.lb_fecha_estimada.place(
            relx = 0.625,
            rely = 0.15
        )
        self.calendario_estimada = Calendar(
            self.tab_alimentar.tab(self.tab5), 
            selectmode='day', 
            font=style.FONT_LINT,
            showweeknumbers=False, 
            cursor="hand2", 
            date_pattern= 'ymmdd',
            borderwidth=0, 
            bordercolor='white',
            locale='es_ES'
        )
        self.calendario_estimada.place_configure(
            relx = 0.56,
            rely = 0.205
        )
        #label y Calendario para seleccionar la fecha de soporte
        self.lb_fecha_sopo = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Fecha de soporte",
            fg_color="transparent"
        )
        self.lb_fecha_sopo.place(
            relx = 0.09,
            rely = 0.57
        )
        self.calendario_sopo = Calendar(
            self.tab_alimentar.tab(self.tab5), 
            selectmode='day', 
            font=style.FONT_LINT,
            showweeknumbers=False, 
            cursor="hand2", 
            date_pattern= 'ymmdd',
            borderwidth=0, 
            bordercolor='white',
            locale='es_ES'
        )
        self.calendario_sopo.place_configure(
            relx = 0.03,
            rely = 0.625
        )
        #Label y entry de la cantidad del plastico a hacer pedido
        self.lb_cantidad_pedido = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Cantidad",
            fg_color="transparent"
        )
        self.lb_cantidad_pedido.place(
            relx = 0.39,
            rely = 0.28
        )
        self.et_cantidad_pedido = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab5),
            placeholder_text = ""
        )
        self.et_cantidad_pedido.place(
            relx = 0.35,
            rely = 0.35,
            relwidth = 0.2
        )
        #Label y entry del precio del pedido
        self.lb_precio_pedido = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Precio",
            fg_color="transparent"
        )
        self.lb_precio_pedido.place(
            relx = 0.41,
            rely = 0.43
        )
        self.et_precio_pedido = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab5),
            placeholder_text = "Ejem: 100.27"
        )
        self.et_precio_pedido.place(
            relx = 0.35,
            rely = 0.49,
            relwidth = 0.2
        )
        #Label y entry de la cantidad del plastico despachada
        self.lb_cantidad_despachada = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Cantidad desp.",
            fg_color="transparent"
        )
        self.lb_cantidad_despachada.place(
            relx = 0.36,
            rely = 0.58
        )
        self.et_cantidad_despachada = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab5),
            placeholder_text = "3000"
        )
        self.et_cantidad_despachada.place(
            relx = 0.35,
            rely = 0.64,
            relwidth = 0.2
        )
        #Label y Combobox del provedor
        self.lb_estado_pedido = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Estado",
            fg_color="transparent"
        )
        self.lb_estado_pedido.place(
            relx = 0.41,
            rely = 0.72
        )
        self.estado_pedido_var = ctk.StringVar()
        self.cb_estado_pedido = ctk.CTkComboBox(
            self.tab_alimentar.tab(self.tab5),
            values = ["Abierto", "Cerrado"],
            variable = self.estado_pedido_var
        )
        self.cb_estado_pedido.place(
            relx = 0.35,
            rely = 0.78,
            relwidth = 0.20
        )
        #Label y entry del valor a pagar por el pedido
        self.lb_valor_a_pagar = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Valor a pagar",
            fg_color="transparent"
        )
        self.lb_valor_a_pagar.place(
            relx = 0.38,
            rely = 0.86
        )
        self.et_valor_a_pagar = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab5),
            placeholder_text = "Ejem: 1000000.89"
        )
        self.et_valor_a_pagar.place(
            relx = 0.35,
            rely = 0.915,
            relwidth = 0.2
        )
        #label y Calendario para seleccionar la fecha de pago
        self.lb_fecha_pago = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab5),
            **style.STYLELABEL,
            text= "Fecha de pago",
            fg_color="transparent"
        )
        self.lb_fecha_pago.place(
            relx = 0.625,
            rely = 0.57
        )
        self.calendario_pago = Calendar(
            self.tab_alimentar.tab(self.tab5), 
            selectmode='day', 
            font=style.FONT_LINT,
            showweeknumbers=False, 
            cursor="hand2", 
            date_pattern= 'ymmdd',
            borderwidth=0, 
            bordercolor='white',
            locale='es_ES'
        )
        self.calendario_pago.place_configure(
            relx = 0.56,
            rely = 0.625
        )
        #Botón que busca según el ID del pedido
        self.bt_search_pedido = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab5),
            **style.SMALLBUTTONSTYLE,
            text = "Buscar",
            command = self.search_by_id_pedido ,
            width= 85
        )
        self.bt_search_pedido.place(
            relx = 0.87,
            rely = 0
        )
        #Botón que registra el pedido y lo deja como incompleto.
        self.bt_insert_pedido = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab5),
            **style.SMALLBUTTONSTYLE,
            text = "Regist.",
            command = self.insert_pedido ,
            width= 85
        )
        self.bt_insert_pedido.place(
            relx = 0.87,
            rely = 0.08
        )
        #Botón que limpia los widgets de pedidos
        self.bt_clean_pedido = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab5),
            **style.SMALLBUTTONSTYLE,
            text = "Limpiar",
            command = self.clean_pedido ,
            width= 85
        )
        self.bt_clean_pedido.place(
            relx = 0.87,
            rely = 0.16
        )
        #Botón que elimina un pedido
        self.bt_eliminar_pedido = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab5),
            **style.SMALLBUTTONSTYLE,
            text = "Eliminar",
            command = self.eliminar_pedido ,
            width= 85
        )
        self.bt_eliminar_pedido.place(
            relx = 0.87,
            rely = 0.24
        )
        #Botón de entrega parcial
        self.bt_entrega_parcial_pedido = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab5),
            **style.SMALLBUTTONSTYLE,
            text = "Entrega\nparcial",
            command = self.entrega ,
            width= 85
        )
        self.bt_entrega_parcial_pedido.place(
            relx = 0.87,
            rely = 0.32
        )
        #Botón de completar pedido
        self.bt_completar_pedido = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab5),
            **style.SMALLBUTTONSTYLE,
            text = "Cerrar",
            command = self.completar_pedido,
            width= 85
        )
        self.bt_completar_pedido.place(
            relx = 0.87,
            rely = 0.46
        )
        #Botón de que muestra los pedidos activos
        self.bt_completar_pedido = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab5),
            **style.SMALLBUTTONSTYLE,
            text = "Activos",
            command = self.pedidos_pendientes,
            width= 85
        )
        self.bt_completar_pedido.place(
            relx = 0.87,
            rely = 0.54
        )
    
    def search_by_id_pedido(self):
        ''' Función que carga los datos de un pedido según el ID'''
        try:
            pedido_df = DBC.find_by(self.cnx_nac, "ID", int(self.et_id_pedido.get()), "PEDIDOSTJ")
            self.load_in_widgets_pedidos(pedido_df)# type: ignore
        except pyodbc.InterfaceError:
            self.login_message = alert_message(self,self, "No se pudo conectar a Nacional\npor favor verifique su conexión y el ID solicitado")

    def load_in_widgets_pedidos(self, df: pd.DataFrame):
        '''Carga la información contenida en un dataframe en los widgets de pedidos,
        recibe:
        self = Frame padre
        df = Dataframe con los datos del pedido'''
        self.et_id_pedido.delete(0, ctk.END)
        self.operador_pedido_var.set("")
        self.planta_final_pedido_var.set("")
        self.planta_produc_pedido_var.set("")
        self.et_CODINV_pedido.delete(0, ctk.END)
        self.calendario_pedido.selection_clear()
        self.calendario_estimada.selection_clear()
        self.calendario_pago.selection_clear()
        self.calendario_sopo.selection_clear()
        #self.lb_trm_pedido.configure(text = "  TRM") este se deja libre hasta que se cargue otro registro
        self.et_cantidad_pedido.delete(0, ctk.END)
        self.et_precio_pedido.delete(0, ctk.END)
        self.et_cantidad_despachada.delete(0, ctk.END)
        self.estado_pedido_var.set("")
        self.et_valor_a_pagar.delete(0, ctk.END)

        self.et_id_pedido.insert(0, str(df.loc[0,"ID"]))
        self.operador_pedido_var.set(str(df.loc[0,"OPERADOR"]))
        self.planta_final_pedido_var.set(str(df.loc[0,"PLANTAFINAL"]))
        self.planta_produc_pedido_var.set(str(df.loc[0,"PLANTAPRODUC"]))
        self.et_CODINV_pedido.insert(0, str(df.loc[0,"CODINV"]))
        fecha_pedido = df.loc[0,"FECHA"]
        self.calendario_pedido.selection_set(dt.datetime.strptime(fecha_pedido, "%Y%m%d"))# type: ignore
        fecha_estimada = df.loc[0,"FECHAESTIMADA"]
        self.calendario_estimada.selection_set(dt.datetime.strptime(fecha_estimada, "%Y%m%d"))# type: ignore
        fecha_pago = df.loc[0,"FECHAPAGO"]
        self.calendario_pago.selection_set(dt.datetime.strptime(fecha_pago, "%Y%m%d"))# type: ignore
        fecha_sopo = df.loc[0,"FECHASOPO"]
        self.calendario_sopo.selection_set(dt.datetime.strptime(fecha_sopo, "%Y%m%d"))# type: ignore
        self.trm = str(df.loc[0, "TRM"])
        self.lb_trm_pedido.configure(text = "TRM\n" + str(df.loc[0, "TRM"])) 
        self.et_cantidad_pedido.insert(0, str(df.loc[0,"CANTIDAD"]))
        self.et_precio_pedido.insert(0, str(df.loc[0,"PRECIO"]))
        self.et_cantidad_despachada.insert(0, str(df.loc[0,"CANTIDADDESP"]))
        self.estado_pedido_var.set(str(df.loc[0,"ESTADO"]))
        self.et_valor_a_pagar.insert(0, str(df.loc[0,"VALORAPAGAR"]))
    
    def insert_pedido(self):
        ''' Función que se encarga de guardar los datos ingresados en los campos de
        creación de pedidos; guarda en un diccionario los datos en los entry
        para convertirlo en un DataFrame y posteriormente enviarlo a la función
        de la ODBC que guarda los pedidos.'''

        self.confirm_action("¿Seguro que desea crear este registro?")

        if self.cfm:
            pedido_dic = {
                'OPERADOR' : [self.cb_operador_pedido.get()],
                'PLANTAFINAL' : [self.cb_planta_final_pedido.get()],
                'PLANTAPRODUC' : [self.cb_planta_produc_pedido.get()],
                'CODINV' : [int(self.et_CODINV_pedido.get())],
                'FECHA' : [self.calendario_pedido.get_date()],
                'FECHAESTIMADA' : [self.calendario_estimada.get_date()],
                'FECHAPAGO' : [self.calendario_pago.get_date()],
                'FECHASOPO' : [self.calendario_sopo.get_date()],
                'TRM' : [self.trm],
                'CANTIDAD' : [int(self.et_cantidad_pedido.get())],
                'PRECIO' : [float(self.et_precio_pedido.get())],
                'CANTIDADDESP' : [int(self.et_cantidad_despachada.get())],
                'ESTADO' : [self.cb_estado_pedido.get()],
                'VALORAPAGAR' : [float(self.et_valor_a_pagar.get())]
            }
            pedido_df = pd.DataFrame(pedido_dic)
            DBC.insert(self, self.cnx_nac,pedido_df,"PEDIDOSTJ")
            self.clean_pedido()
            self.cfm = False
    
    def clean_pedido(self):
        '''Limpia la información de los widgets de pedidos'''
        self.et_id_pedido.delete(0, ctk.END)
        self.operador_pedido_var.set("")
        self.planta_final_pedido_var.set("")
        self.planta_produc_pedido_var.set("")
        self.et_CODINV_pedido.delete(0, ctk.END)
        self.calendario_pedido.selection_clear()
        self.calendario_estimada.selection_clear()
        self.calendario_pago.selection_clear()
        self.calendario_sopo.selection_clear()
        self.trm = DBC.TRM(self)
        self.lb_trm_pedido.configure(text = "TRM\n" + str(self.trm))
        self.et_cantidad_pedido.delete(0, ctk.END)
        self.et_precio_pedido.delete(0, ctk.END)
        self.et_cantidad_despachada.delete(0, ctk.END)
        self.estado_pedido_var.set("")
        self.et_valor_a_pagar.delete(0, ctk.END)

    def eliminar_pedido(self):
        '''Función que se encarga de eliminar un pedido según su ID'''
        self.confirm_action("¿Está seguro que desea Eliminar este registro de Forma permanente?")

        if self.cfm:
            if int(self.et_cantidad_despachada.get()) > 0:
                self.login_message = alert_message(self,self, "No puedes eliminar un pedido que ya recibió una entrega parcial\npor favor consulte con un superior")
            else:
                DBC.delete(self, self.cnx_nac,"ID", int(self.et_id_pedido.get()), "PEDIDOSTJ")
                self.clean_pedido()

    def entrega(self):
        """Función que se encarga de actualizar la cantidad de plasticos entregados
        de forma parcial a la planta final, no completa el pedido"""
        self.confirm_action(f"¿Está seguro que desea hacer la entrega parcial de {str(self.et_cantidad_despachada.get())} plasticos\na este pedido?")
        if self.cfm:
            DBC.pedidos_parciales(self, self.cnx_nac,int(self.et_id_pedido.get()), int(self.et_cantidad_despachada.get()), int(self.et_CODINV_pedido.get()), self.cb_planta_final_pedido.get(), self.cb_operador_pedido.get())
            self.login_message = alert_message(self,self, "Se completó el traslado con exito.")
            self.search_by_id_pedido()

    def completar_pedido(self):
        """Función que se encarga de marcar como completo el pedido"""
        self.confirm_action("¿Está seguro que desea marcar como COMPLETO este pedido?")
        porciento = int(self.et_cantidad_pedido.get()) * 0.10
        min = int(self.et_cantidad_pedido.get()) - porciento
        if self.cfm:
            if int(self.et_cantidad_despachada.get()) < min:
                self.login_message = alert_message(self,self, "No se puede completar el pedido, el total de entregas parciales\n debe superar como minimo el (total - diez prociento) de lo acordado")
            else:
                DBC.completar_pedido(self, self.cnx_nac, int(self.et_id_pedido.get()))
                self.login_message = alert_message(self,self, "Se completó el pedido con exito.")
                self.clean_traslado()

    def pedidos_pendientes(self):
        """Genera una hoja de calculo sobre los demás widgets que nos muestras
        todos los pedidos pendientes"""
        if not self.tabla:
            self.df_pedidos_pendientes = DBC.pedidos_pendientes(self, self.cnx_nac)
            #Tabla en la cual se colocan los datos
            self.sheet_pedidos_pendientes = Sheet(
                self.tab_alimentar.tab(self.tab5),
                data = self.df_pedidos_pendientes.values.tolist(),# type: ignore
                headers= self.df_pedidos_pendientes.columns.tolist(),# type: ignore
                show_x_scrollbar= True,
                font = style.FONT_NORMAL, 
                header_font = style.FONT_NORMAL
            )
            self.sheet_pedidos_pendientes.place(
                relx = 0,
                rely = 0,
                relwidth = 0.85,
                relheight = 1
            )
            self.tabla = True
        else:
            self.sheet_pedidos_pendientes.destroy()
            self.tabla = False





#____________________________añadir item a inventario____________________________________
    def anadir(self):
        #Label y entry del ID del item
        self.lb_id_item = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab6),
            **style.STYLELABEL,
            text= "ID Item",
            fg_color="transparent"
        )
        self.lb_id_item.place(
            relx = 0.055,
            rely = 0
        )
        self.et_id_item = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab6),
            placeholder_text = "ID"
        )
        self.et_id_item.place(
            relx = 0.075,
            rely = 0.08,
            relwidth = 0.06
        )  
        #Label y Combobox del nombre plastico
        self.lb_nombre_item = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab6),
            **style.STYLELABEL,
            text= "Nombre plastico",
            fg_color="transparent"
        )
        self.lb_nombre_item.place(
            relx = 0.21,
            rely = 0
        )
        self.nombre_item_var = ctk.StringVar()
        self.cb_nombre_item = ctk.CTkComboBox(
            self.tab_alimentar.tab(self.tab6),
            values = self.ls_plasticos,
            variable = self.nombre_item_var
        )
        self.cb_nombre_item.place(
            relx = 0.155,
            rely = 0.08,
            relwidth = 0.30
        )
        #Label y entry del CODINV del item
        self.lb_codinv_item = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab6),
            **style.STYLELABEL,
            text= "CODINV",
            fg_color="transparent"
        )
        self.lb_codinv_item.place(
            relx = 0.48,
            rely = 0
        )
        self.et_codinv_item = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab6),
            placeholder_text = "CODINV"
        )
        self.et_codinv_item.place(
            relx = 0.48,
            rely = 0.08,
            relwidth = 0.1
        )
        #Label y Combobox de los provedores
        self.lb_provedor_item = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab6),
            **style.STYLELABEL,
            text= "Provedor",
            fg_color="transparent"
        )
        self.lb_provedor_item.place(
            relx = 0.7,
            rely = 0
        )
        self.provedor_item_var = ctk.StringVar()
        self.cb_provedor_item = ctk.CTkComboBox(
            self.tab_alimentar.tab(self.tab6),
            values = self.ls_proveedores,
            variable = self.provedor_item_var
        )
        self.cb_provedor_item.place(
            relx = 0.6,
            rely = 0.08,
            relwidth = 0.30
        )
        #Label y Combobox la planta
        self.lb_planta_item = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab6),
            **style.STYLELABEL,
            text= "Planta",
            fg_color="transparent"
        )
        self.lb_planta_item.place(
            relx = 0.14,
            rely = 0.18
        )
        self.planta_item_var = ctk.StringVar()
        self.cb_planta_item = ctk.CTkComboBox(
            self.tab_alimentar.tab(self.tab6),
            values = self.ls_plantas,
            variable = self.planta_item_var
        )
        self.cb_planta_item.place(
            relx = 0.08,
            rely = 0.26,
            relwidth = 0.20
        )
        #Label y entry de Cantidad del item
        self.lb_cantidad_item = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab6),
            **style.STYLELABEL,
            text= "Cantidad",
            fg_color="transparent"
        )
        self.lb_cantidad_item.place(
            relx = 0.35,
            rely = 0.18
        )
        self.et_cantidad_item = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab6),
            placeholder_text = "Cantidad"
        )
        self.et_cantidad_item.place(
            relx = 0.30,
            rely = 0.26,
            relwidth = 0.20
        )
        #Botón que busca según el ID del item
        self.bt_search_item = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab6),
            **style.SMALLBUTTONSTYLE,
            text = "Buscar",
            command = self.search_by_id_item ,
            width= 90
        )
        self.bt_search_item.place(
            relx = 0.055,
            rely = 0.36
        )
        #Botón que guarda el item
        self.bt_save_item = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab6),
            **style.SMALLBUTTONSTYLE,
            text = "Guardar",
            command = self.insert_item ,
            width= 90
        )
        self.bt_save_item.place(
            relx = 0.20,
            rely = 0.36
        )
        #Botón de limpiar
        self.bt_clean_item = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab6),
            **style.SMALLBUTTONSTYLE,
            text = "Limpiar",
            command = self.clean_item,
            width= 90
        )
        self.bt_clean_item.place(
            relx = 0.345,
            rely = 0.36
        )
        #Botón que eliminar el item
        self.bt_delete_item = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab6),
            **style.SMALLBUTTONSTYLE,
            text = "Eliminar",
            command = self.eliminar_item,
            width= 90
        )
        self.bt_delete_item.place(
            relx = 0.495,
            rely = 0.36
        )
        #Botón que muestra todos los items
        self.bt_all_item = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab6),
            **style.SMALLBUTTONSTYLE,
            text = "ITEMS",
            command = self.items_completos,
            width= 90
        )
        self.bt_all_item.place(
            relx = 0.645,
            rely = 0.36
        )

    def search_by_id_item(self):
        ''' Función que carga los datos de un item según el ID'''
        try:
            item_df = DBC.find_by(self.cnx_nac, "ID", int(self.et_id_item.get()), "INVENTARIOTJ")
            self.load_in_widgets_items(item_df)# type: ignore
        except pyodbc.InterfaceError:
            self.login_message = alert_message(self,self, "No se pudo conectar a Nacional\npor favor verifique su conexión y el ID solicitado")
    
    def load_in_widgets_items(self, df: pd.DataFrame):
        '''Carga la información contenida en un dataframe en los widgets de items,
        recibe:
        self = Frame padre
        df = Dataframe con los datos del pedido'''
        self.et_id_item.delete(0, ctk.END)
        self.nombre_item_var.set("")
        self.et_codinv_item.delete(0, ctk.END)
        self.provedor_item_var.set("")
        self.planta_item_var.set("")
        self.et_cantidad_item.delete(0, ctk.END)

        self.et_id_item.insert(0, str(df.loc[0,"ID"]))
        self.nombre_item_var.set(str(df.loc[0,"NOMBRE"]))
        self.et_codinv_item.insert(0, str(df.loc[0,"CODINV"]))
        self.provedor_item_var.set(str(df.loc[0,"PROVEDOR"]))
        self.planta_item_var.set(str(df.loc[0,"PLANTA"]))
        self.et_cantidad_item.insert(0, str(df.loc[0,"CANTIDAD"]))
    
    def insert_item(self):
        ''' Función que se encarga de guardar los datos ingresados en los campos de
        creación de items; guarda en un diccionario los datos en los entry
        para convertirlo en un DataFrame y posteriormente enviarlo a la función
        de la ODBC que guarda los items.'''

        self.confirm_action("¿Seguro que desea crear este registro?")

        df_items = DBC.verificar_inventario(self, self.cnx_nac, int(self.et_codinv_item.get()), self.cb_provedor_item.get(), self.cb_planta_item.get())
        if df_items.empty:# type: ignore
            if self.cfm:
                item_dic = {
                    'NOMBRE' : [self.cb_nombre_item.get()],
                    'CODINV' : [int(self.et_codinv_item.get())],
                    'PROVEDOR' : [self.cb_provedor_item.get()],
                    'PLANTA' : [self.cb_planta_item.get()],
                    'CANTIDAD' : [int(self.et_cantidad_item.get())]
                }
                item_df = pd.DataFrame(item_dic)
                DBC.insert(self, self.cnx_nac,item_df,"INVENTARIOTJ")
                self.clean_item()
                self.cfm = False
                self.login_message = alert_message(self,self, "Se registro el item con eso.")
        else:
            self.login_message = alert_message(self,self, "¡Ese item ya existe!\n Por favor verifique los datos ingresados")


    def clean_item(self):
        '''Limpia la información de los widgets de items'''
        self.et_id_item.delete(0, ctk.END)
        self.nombre_item_var.set("")
        self.et_codinv_item.delete(0, ctk.END)
        self.provedor_item_var.set("")
        self.planta_item_var.set("")
        self.et_cantidad_item.delete(0, ctk.END)
    
    def eliminar_item(self):
        '''Función que se encarga de eliminar un item según su ID'''
        self.confirm_action("¿Está seguro que desea Eliminar este Item de Forma permanente?\nRecuerde que esto representa las existencias de un plastico")

        if self.cfm:
            DBC.delete(self, self.cnx_nac,"ID", int(self.et_id_item.get()), "INVENTARIOTJ")
            self.clean_item()

    def items_completos(self):
        """Genera una hoja de calculo sobre los demás widgets que nos muestras
        todos los items"""
        if not self.tabla:
            self.df_items = DBC.items(self, self.cnx_nac)
            #Tabla en la cual se colocan los datos
            self.sheet_items = Sheet(
                self.tab_alimentar.tab(self.tab6),
                data = self.df_items.values.tolist(),# type: ignore
                headers= self.df_items.columns.tolist(),# type: ignore
                show_x_scrollbar= True,
                font = style.FONT_NORMAL, 
                header_font = style.FONT_NORMAL
            )
            self.sheet_items.place(
                relx = 0,
                rely = 0,
                relwidth = 1,
                relheight = 0.35
            )
            self.tabla = True
        else:
            self.sheet_items.destroy()
            self.tabla = False

        



#_____________________________Inventarios______________________________________________________
    def inventarios(self):
        #Se crea un tabView para los diferentes provedores y inventarios
        self.tab_inventarios = ctk.CTkTabview(
            self.tab_alimentar.tab(self.tab7),
            segmented_button_selected_hover_color = style.BLUE,
            segmented_button_selected_color= style.DARKBLUE
        )
        self.tab_inventarios.pack(
            anchor = ctk.N, 
            fill = ctk.BOTH,
            expand = True
        )
        for i in self.ls_proveedores:
            tab = i
            self.tab_inventarios.add(tab)
            #Se crea un tabView para las diferentes plantas de su provedor
            self.ls_plantasx = DBC.find_planta_x_provedor(self, self.cnx_nac,i).to_list()
            self.ls_plantasx.sort()
            self.ls_plantasx = list(set(self.ls_plantasx))
            self.tab_inventarios_planta = ctk.CTkTabview(
                self.tab_inventarios.tab(tab),
                segmented_button_selected_hover_color = style.BLUE,
                segmented_button_selected_color= style.DARKBLUE
            )
            self.tab_inventarios_planta.pack(
                anchor = ctk.N, 
                fill = ctk.BOTH,
                expand = True
            )
            for j in self.ls_plantasx:
                self.tab = j
                self.tab_inventarios_planta.add(self.tab)   
                #Hacemos un sheet que cargará el inventario de cada planta
                self.df_inventario_j = DBC.inventario_x_planta_provedor(self, self.cnx_nac, j, i)
                #Tabla en la cual se colocan los datos
                self.sheet_ = Sheet(
                    self.tab_inventarios_planta.tab(j),
                    data = self.df_inventario_j.values.tolist(),# type: ignore
                    headers= self.df_inventario_j.columns.tolist(),# type: ignore
                    show_x_scrollbar= True,
                    font = style.FONT_NORMAL, 
                    header_font = style.FONT_NORMAL
                )
                self.sheet_.place(
                    relx = 0,
                    rely = 0,
                    relwidth = 1,
                    relheight = 1
                )
            
        
            

     