import os
import sys

from downloadModelDialog import DownloadModelDialog
from findPathWidget import FindPathWidget
from imageView import ImageView
from script import is_exists, get_model_path, get_result_image_by_doing_object_detection
from selectModelDialog import SelectModelDialog

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QSplitter, QListWidget, QVBoxLayout, \
    QWidget, QSizePolicy, QDialog, QMessageBox, QLabel
from PyQt5.QtCore import Qt, QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QFont

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    generateFinished = pyqtSignal(str)

    def __init__(self, filename, model_path):
        super(Thread, self).__init__()
        self.__filename = filename
        self.__model_path = model_path

    def run(self):
        try:
            dst_filename = os.path.basename(self.__filename)+'_result'+os.path.splitext(self.__filename)[-1]
            get_result_image_by_doing_object_detection(self.__model_path, self.__filename, dst_filename)
            self.generateFinished.emit(dst_filename)
        except Exception as e:
            raise Exception(e)


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

        findPathWidget = FindPathWidget()
        findPathWidget.getLineEdit().setPlaceholderText('Select the Directory including images...')
        findPathWidget.added.connect(self.__addFiles)
        findPathWidget.setAsDirectory(True)

        self.__fileListWidget = QListWidget()
        self.__fileListWidget.itemActivated.connect(self.__itemActivated)

        self.__runBtn = QPushButton('Run')
        self.__runBtn.clicked.connect(self.__run)

        self.__beforeView = ImageView()
        self.__afterView = ImageView()

        viewSplitter = QSplitter()
        viewSplitter.addWidget(self.__beforeView)
        viewSplitter.addWidget(self.__afterView)
        viewSplitter.setHandleWidth(2)
        viewSplitter.setChildrenCollapsible(False)
        viewSplitter.setSizes([500, 500])
        viewSplitter.setStyleSheet(
            "QSplitterHandle {background-color: blue; }")

        lay = QVBoxLayout()
        lay.addWidget(self.__runBtn)
        lay.addWidget(viewSplitter)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        splitterRightWidget = QWidget()
        splitterRightWidget.setLayout(lay)

        splitter = QSplitter()
        splitter.addWidget(self.__fileListWidget)
        splitter.addWidget(splitterRightWidget)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([300, 700])
        splitter.setStyleSheet(
            "QSplitterHandle {background-color: lightgray;}")
        splitter.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(self.__curModelLbl)
        lay.addWidget(findPathWidget)
        lay.addWidget(splitter)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

        self.__runBtn.setEnabled(False)

    def __addFiles(self, dirname):
        self.__filename_dict.clear()
        self.__fileListWidget.clear()
        filenames = [os.path.join(dirname, filename) for filename in os.listdir(dirname) if os.path.splitext(filename)[-1] in ['.png', '.jpg']]
        self.__fileListWidget.addItems(filenames)
        self.__runBtn.setEnabled(len(filenames) > 0)

    def __itemActivated(self, item):
        filename = item.text()
        self.__cur_src_filename = filename
        if self.__filename_dict.get(self.__cur_src_filename, '') == '':
            if not self.__afterView.scene():
                self.__filename_dict[self.__cur_src_filename] = ''
            else:
                self.__afterView.scene().clear()
        else:
            self.__afterView.scene().clear()
            self.__afterView.setFilename(self.__filename_dict[self.__cur_src_filename])
        self.__beforeView.setFilename(self.__cur_src_filename)

    def __run(self):
        filename = self.__fileListWidget.currentItem().text()
        self.__t = Thread(filename, self.__cur_model_path)
        self.__t.started.connect(self.__started)
        self.__t.finished.connect(self.__finished)
        self.__t.generateFinished.connect(self.__generateFinished)
        self.__t.start()

    def __started(self):
        print('started')

    def __generateFinished(self, filename):
        self.__filename_dict[self.__cur_src_filename] = filename
        self.__afterView.setFilename(filename)

    def __finished(self):
        print('finished')

    def setModel(self, model, model_path):
        self.__cur_model_name = model
        self.__cur_model_path = model_path
        self.__curModelLbl.setText(self.__curModelLbl.text() + ' ' + self.__cur_model_name)



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



if __name__ == "__main__":
    import sys

    main()