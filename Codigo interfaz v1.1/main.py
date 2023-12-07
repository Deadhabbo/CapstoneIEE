"""""
README v1.1:

Felipe Munizaga [23/06/23]:

    -Bug fixed in zone.py, line 24: QPoint expected an int value, but a float was given.
    Now, an int value is given.
    
    -Distances were not properly calculated: now it takes the dpi of the main screen 
    and it performs the following px to cm conversion: cm = px * ( 2.54 / DPI ) in
    interfaz.py, line 206.

"""""


import sys

from PyQt5.QtWidgets import QApplication

from interfaz import Interfaz


# # Para poder debbuguear
# def hook(type_error, traceback):
#     print(type_error)
#     print(traceback)


if __name__ == "__main__":
    # sys.__excepthook__ = hook
    app = QApplication(sys.argv)

    interfaz = Interfaz()
    interfaz.show()

    sys.exit(app.exec_())