#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk
from tksheet import Sheet
import pandas as pd

#Se importan valores constantes de nuestra aplicación
from constants import style
from Functions import ODBC

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
        self.init_tabview()
        
    def import_file(self):
        """
        Funcion encargada de importar la alimentación del inventario,
        transforma la fuente de datos de pandas en un dataframe y lo pone en pantalla
        en una tabla con tksheet.
        """
        self.path = self.et_file.get()
        self.temp_file = ODBC.import_from_excel(self, self.path)
        self.df_excel = pd.DataFrame(self.temp_file)
        self.df_excel["SEMANAS INVENTARIO"] = pd.Series([round(val,2) for val in self.df_excel["SEMANAS INVENTARIO"]]) 
        #Tabla en la cual se colocan los datos
        self.sheet = Sheet(
            self.tab_alimentar.tab(self.tab1),
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
        """
        Abre una nueva ventana de busqueda local para indicar la
        dirección del archivo deseado.
        """
        path = ctk.filedialog.askopenfilename()
        self.et_file.insert(0,path)

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
        self.tab1 = "Carga de inventarios"
        self.tab2 = "Por definir"
        self.tab_alimentar.add(self.tab1)
        self.tab_alimentar.add(self.tab2)
        self.tab_alimentar.set(self.tab1)
        #Inicia el entri donde se colocará la dirección del archivo
        self.et_file = ctk.CTkEntry(
            self.tab_alimentar.tab(self.tab1),
            placeholder_text = "Ingrese la dirección del archivo o seleccionelo con el botón Explorar"
        )
        self.et_file.place(
            relx = 0.15,
            rely = 0.1,
            relwidth = 0.65
        )
        #Label del entry de dirección de archivo
        self.lb_file = ctk.CTkLabel(
            self.tab_alimentar.tab(self.tab1),
            **style.STYLELABEL,
            text= "Archivo:",
            fg_color="transparent"
        )
        self.lb_file.place(
            relx = 0.03,
            rely = 0.1
        )
        #Botón que ejecuta el buscador de archivos.
        self.bt_file = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab1),
            **style.SMALLBUTTONSTYLE,
            text = "Explorar",
            command = self.find_file
        )
        self.bt_file.place(
            relx = 0.82,
            rely = 0.0995,
            width = 100,
            height= 26,
        )
        #Botón que carga el archivo indicado en la ruta.
        self.bt_load = ctk.CTkButton(
            self.tab_alimentar.tab(self.tab1),
            **style.SMALLBUTTONSTYLE,
            text = "Importar",
            command = self.import_file
        )
        self.bt_load.place(
            relx = 0.03,
            rely = 0.2
        )
        

     