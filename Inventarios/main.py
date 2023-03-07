######Clase Main, donde se ejecuta nuestro programa y se realiza el loop operativo####

#importamos las clases necesarias para la interfaz grafica
from Manager import Manager

if __name__=="__main__":
    """
    Clase main que ejecuta en bucle todo el codigo.
    """
    app = Manager()
    app.mainloop()