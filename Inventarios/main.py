######Clase Main, donde se ejecuta nuestro programa y se realiza el loop operativo####
import tkinter as tk
import customtkinter as ctk
import pyodbc
import pandas as pd
import re
import datetime as dt

#importamos las clases necesarias para la interfaz grafica
from Manager import Manager

if __name__=="__main__":
    """
    Clase main que ejecuta en bucle todo el codigo.
    """
    app = Manager()
    app.mainloop()