from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QFrame, QFormLayout, QVBoxLayout, QPushButton, QDialog


class SelectModelDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__model_arr = ['RetinaNet', 'YOLOv3', 'TinyYOLOv3']
        self.__model = self.__model_arr[0]

    def __initUi(self):
        self.setWindowTitle('Select the Model to use')
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        modelCmbBox = QComboBox()
        modelCmbBox.addItems(self.__model_arr)
        modelCmbBox.currentTextChanged.connect(self.set_model)

        lay = QFormLayout()
        lay.addRow('Models', modelCmbBox)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        okBtn = QPushButton('OK')
        okBtn.clicked.connect(self.accept)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(sep)
        lay.addWidget(okBtn, alignment=Qt.AlignRight)

        self.setLayout(lay)

        self.setFixedSize(self.sizeHint())
        self.setFixedWidth(300)

    def set_model(self, model):
        self.__model = model

    def get_model(self):
        return self.__model
