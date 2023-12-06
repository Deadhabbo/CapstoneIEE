import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Crear el diseño principal
        self.layout_principal = QVBoxLayout()

        # Crear el QComboBox
        self.selector = QComboBox()
        self.selector.addItem('Opción A')
        self.selector.addItem('Opción B')
        self.selector.currentIndexChanged.connect(self.cambiar_layout)

        # Añadir el QComboBox al diseño principal
        self.layout_principal.addWidget(self.selector)

        # Crear los layouts para las opciones A y B
        self.layout_opcion_a = QVBoxLayout()
        self.layout_opcion_b = QVBoxLayout()

        # Agregar widgets a los layouts de las opciones A y B
        self.layout_opcion_a.addWidget(QLabel('Contenido de la Opción A'))
        self.layout_opcion_b.addWidget(QLabel('Contenido de la Opción B'))

        # Establecer el diseño predeterminado (Opción A)
        self.layout_principal.addLayout(self.layout_opcion_a)

        # Establecer el diseño principal para la ventana
        self.setLayout(self.layout_principal)

        # Configurar la ventana principal
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Selector de Opciones')
        self.show()

    def cambiar_layout(self, index):
        # Eliminar cualquier diseño existente en el diseño principal
        for i in reversed(range(self.layout_principal.count())):
            widget = self.layout_principal.takeAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Añadir el diseño correspondiente según la opción seleccionada
        if index == 0:  # Opción A
            self.layout_principal.addLayout(self.layout_opcion_a)
        elif index == 1:  # Opción B
            self.layout_principal.addLayout(self.layout_opcion_b)

        # Actualizar la interfaz
        self.layout_principal.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    sys.exit(app.exec_())