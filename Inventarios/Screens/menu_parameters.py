#se importan las librerias que nos permiten generar una interfaz grafica
import tkinter as tk
import customtkinter as ctk
from tksheet import Sheet
import pandas as pd

#Se importan valores constantes de nuestra aplicación
from constants import style
from Functions import ODBC

class menu_parameters(ctk.CTkFrame):
    """
    Clase encargada de la parametrización y creación de datos
    importantes para el sistema.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color = style.GRAYBLACK)
        self.controller = controller
        self.init_tabview()

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
        self.tab2 = "Por definir"
        self.tab_parametros.add(self.tab1)
        self.tab_parametros.add(self.tab2)
        self.tab_parametros.set(self.tab1)

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
            placeholder_text = "",
            state = "disabled"
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
            placeholder_text = ""
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
            placeholder_text = ""
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
            placeholder_text = ""
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
            placeholder_text = ""
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
        self.descont_var = ctk.StringVar(value = "on")
        self.chk_descontinuado = ctk.CTkCheckBox(
            self.tab_parametros.tab(self.tab1),
            text = "Descontinuado",
            **style.STYLELABEL,
            variable = self.descont_var,
            onvalue= "on",
            offvalue="off"
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
        #Label y entry operador
        self.lb_operador = ctk.CTkLabel(
            self.tab_parametros.tab(self.tab1),
            **style.STYLELABEL,
            text= "Operador:",
            fg_color="transparent"
        )
        self.lb_operador.place(
            relx = 0.58,
            rely = 0.45
        )
        self.et_operador = ctk.CTkEntry(
            self.tab_parametros.tab(self.tab1),
            placeholder_text = ""
        )
        self.et_operador.place(
            relx = 0.71,
            rely = 0.45,
            relwidth = 0.06
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
            text= "01/01/1991",
            fg_color="transparent"
        )
        self.lb_fecha.place(
            relx = 0.60,
            rely = 0.53
        )
        #Label y entry de la CANTIDAD
        self.lb_cantidad = ctk.CTkLabel(
            self.tab_parametros.tab(self.tab1),
            **style.STYLELABEL,
            text= "Cantidad:",
            fg_color="transparent"
        )
        self.lb_cantidad.configure(
            font = ("Calibri Bold", 28, "bold")
        )
        self.lb_cantidad.place(
            relx = 0.03,
            rely = 0.655
        )
        self.et_cantidad = ctk.CTkEntry(
            self.tab_parametros.tab(self.tab1),
            placeholder_text = ""
        )
        self.et_cantidad.configure(
            font = ("Calibri Bold", 28, "bold")
        )
        self.et_cantidad.place(
            relx = 0.21,
            rely = 0.65,
            relwidth = 0.1
        )
        #Textbox de las observaciones
        self.tb_observaciones = ctk.CTkTextbox(
            self.tab_parametros.tab(self.tab1),
            **style.STYLELABEL,
            width=520,
            height=100
        )
        self.tb_observaciones.configure(
            font = ("Calibri Bold", 14)
        ) 
        self.tb_observaciones.place(
            relx = 0.03,
            rely = 0.77
        )
        

