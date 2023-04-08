#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
from tkcalendar import Calendar
import customtkinter as ctk
from tksheet import Sheet
import pandas as pd
import pyodbc

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
        #Lista que contiene los consecutivos
        self.ls_pedidos = []
        self.ls_pedidos_idemia = []
        #conexión que usara esta pantalla
        self.cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID={};PWD={}'.format(controller.user, controller.password), autocommit=True )
        self.init_tabview()
        self.entrada_semanal()
        self.descarga_diaria()
        self.inventario_0()

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
        self.tab4 = "Por definir"
        self.tab_alimentar.add(self.tab1)
        self.tab_alimentar.add(self.tab2)
        self.tab_alimentar.add(self.tab3)
        self.tab_alimentar.add(self.tab4)
        self.tab_alimentar.set(self.tab1)



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
            show_x_scrollbar= True
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
        self.temp_file_0 = DBC.import_from_excel(self, self.path_0, "Hoja1")
        self.df_excel_0 = pd.DataFrame(self.temp_file_0)
        #Tabla en la cual se colocan los datos
        self.sheet_0 = Sheet(
            self.tab_alimentar.tab(self.tab3),
            data = self.df_excel_0.values.tolist(),
            headers= self.df_excel_0.columns.tolist(),
            show_x_scrollbar= True
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
            relx = 0.76,
            rely = 0.11
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


#________________________Traslados___________________________________________
#def traslados():

        
            

     