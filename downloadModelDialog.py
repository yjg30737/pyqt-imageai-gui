from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
from PyQt5.QtCore import Qt

from consoleWidgetThread import ConsoleThread
from loadingProgressBar import LoadingProgressBar


class DownloadModelDialog(QDialog):
    def __init__(self):
        super(DownloadModelDialog, self).__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Downloading...')
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self.__loadingProgressBar = LoadingProgressBar()
        self.__consoleWidget = QTextBrowser()

        self.__okBtn = QPushButton('OK')
        self.__okBtn.setEnabled(False)
        self.__okBtn.clicked.connect(self.accept)

        lay = QVBoxLayout()
        lay.addWidget(self.__loadingProgressBar)
        lay.addWidget(self.__consoleWidget)
        lay.addWidget(self.__okBtn)

        self.setLayout(lay)

    def downloadModel(self, model):
        command = f'python loadModel.py {model}'
        self.__t = ConsoleThread(command)
        self.__t.started.connect(self.__started)
        self.__t.updated.connect(self.__consoleWidget.append)
        self.__t.finished.connect(self.__finished)
        self.__t.start()

    def __started(self):
        self.__consoleWidget.append('Started')

    def __finished(self):
        self.__consoleWidget.append('Finished')
        self.__loadingProgressBar.setVisible(False)
        self.__okBtn.setEnabled(True)
