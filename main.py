import os
import sys

from downloadModelDialog import DownloadModelDialog
from objectDetectionFromImageWidget import ObjectDetectionFromImageWidget
from objectDetectionFromVideoWidget import ObjectDetectionFromVideoWidget
from script import is_exists, get_model_path
from selectModelDialog import SelectModelDialog

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, \
    QWidget, QDialog, QMessageBox, QLabel, QTabWidget
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))





class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__cur_src_filename = ''
        self.__cur_model_name = ''
        self.__cur_model_path = ''
        self.__filename_dict = {}

    def __initUi(self):
        self.setWindowTitle('PyQt ImageAI GUI')

        self.__curModelLbl = QLabel('Current Model: ')

        self.__objectDetectionFromImageWidget = ObjectDetectionFromImageWidget()
        self.__objectDetectionFromVideoWidget = ObjectDetectionFromVideoWidget()

        tabWidget = QTabWidget()
        tabWidget.addTab(self.__objectDetectionFromImageWidget, 'Object Detection from Image')
        tabWidget.addTab(self.__objectDetectionFromVideoWidget, 'Object Detection from Video')

        lay = QVBoxLayout()
        lay.addWidget(self.__curModelLbl)
        lay.addWidget(tabWidget)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

    def setModel(self, model, model_path):
        self.__cur_model_name = model
        self.__cur_model_path = model_path
        self.__curModelLbl.setText(self.__curModelLbl.text() + ' ' + self.__cur_model_name)

        self.__objectDetectionFromImageWidget.setModel(self.__cur_model_name, self.__cur_model_path)
        self.__objectDetectionFromVideoWidget.setModel(self.__cur_model_name, self.__cur_model_path)


def main():
    app = QApplication(sys.argv)
    selectModelDialog = SelectModelDialog()

    if selectModelDialog.exec_() == QDialog.Accepted:
        model = selectModelDialog.get_model()
        mainWindow = MainWindow()
        if is_exists(model):
            model_path = get_model_path(model)
            # mainWindow setModel
            mainWindow.setModel(model, model_path)
            mainWindow.show()
        else:
            QMessageBox.information(mainWindow, 'PyQt ImageAI GUI', 'There is no model file. Proceed to download the model.')
            downloadModelDialog = DownloadModelDialog()
            downloadModelDialog.downloadModel(model)
            if downloadModelDialog.exec_() == QDialog.Accepted:
                # mainWindow setModel
                model_path = get_model_path(model)
                mainWindow.setModel(model, model_path)
                mainWindow.show()
            else:
                QMessageBox.information(mainWindow, 'PyQt ImageAI GUI', 'Downloading process stopped. Goodbye.')
                sys.exit(app.exec())
        sys.exit(app.exec())



if __name__ == "__main__":
    import sys

    main()