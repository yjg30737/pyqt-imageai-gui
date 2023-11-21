import os

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QSplitter, QListWidget, QVBoxLayout, \
    QWidget, QSizePolicy, QMessageBox, QTableWidget, QHeaderView

from findPathWidget import FindPathWidget
from script import get_result_image_by_doing_object_detection
from splittedImageView import SplittedImageView


class Thread(QThread):
    generateFinished = pyqtSignal(str)

    def __init__(self, filename, model_name, model_path):
        super(Thread, self).__init__()
        self.__filename = filename
        self.__model_name = model_name
        self.__model_path = model_path

    def run(self):
        try:
            dst_filename = os.path.basename(self.__filename)+'_result'+os.path.splitext(self.__filename)[-1]
            get_result_image_by_doing_object_detection(self.__model_name, self.__model_path, self.__filename, dst_filename)
            self.generateFinished.emit(dst_filename)
        except Exception as e:
            raise Exception(e)


class ObjectDetectionFromImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__cur_model_name = ''
        self.__cur_model_path = ''
        self.__filename_dict = {}

    def __initUi(self):
        findPathWidget = FindPathWidget()
        findPathWidget.getLineEdit().setPlaceholderText('Select the Directory including images...')
        findPathWidget.added.connect(self.__addFiles)
        findPathWidget.setAsDirectory(True)

        self.__fileListWidget = QListWidget()
        self.__fileListWidget.itemActivated.connect(self.__itemActivated)
        self.__fileListWidget.currentItemChanged.connect(self.__itemActivated)

        self.__runBtn = QPushButton('Run')
        self.__runBtn.clicked.connect(self.__run)

        self.__view = SplittedImageView(self)

        lay = QVBoxLayout()
        lay.addWidget(self.__runBtn)
        lay.addWidget(self.__view)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        splitterRightWidget = QWidget()
        splitterRightWidget.setLayout(lay)

        self.__detectionTableWidget = QTableWidget()
        self.__detectionTableWidget.setColumnCount(2)
        self.__detectionTableWidget.setHorizontalHeaderLabels(['Name', 'Value'])
        self.__detectionTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        splitter = QSplitter()
        splitter.addWidget(self.__fileListWidget)
        splitter.addWidget(splitterRightWidget)
        splitter.addWidget(self.__detectionTableWidget)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([200, 600, 200])
        splitter.setStyleSheet(
            "QSplitterHandle {background-color: lightgray;}")
        splitter.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()

        lay.addWidget(findPathWidget)
        lay.addWidget(splitter)

        self.setLayout(lay)

        self.__runBtn.setEnabled(False)

    def __addFiles(self, dirname):
        self.__filename_dict.clear()
        self.__fileListWidget.clear()
        filenames = [os.path.join(dirname, filename) for filename in os.listdir(dirname) if
                     os.path.splitext(filename)[-1] in ['.png', '.jpg']]
        self.__fileListWidget.addItems(filenames)
        self.__runBtn.setEnabled(len(filenames) > 0)
        self.__fileListWidget.setCurrentRow(0)

    def __setItemToEachView(self, item):
        filename = item.text()
        self.__cur_src_filename = filename
        if self.__filename_dict.get(self.__cur_src_filename, '') == '':
            self.__filename_dict[self.__cur_src_filename] = ''
            self.__view.removeItemOnTheRight()
        else:
            self.__view.setFilenameToRight(self.__filename_dict[self.__cur_src_filename])
        self.__view.setFilenameToLeft(self.__cur_src_filename)

    def __itemActivated(self, item):
        if item:
            self.__setItemToEachView(item)
        else:
            item = self.__fileListWidget.currentItem()
            if item:
                self.__setItemToEachView(item)
            else:
                print('there is no item what')

    def __run(self):
        item = self.__fileListWidget.currentItem()
        if item:
            filename = item.text()
            self.__t = Thread(filename, self.__cur_model_name, self.__cur_model_path)
            self.__t.generateFinished.connect(self.__generateFinished)
            self.__t.start()
        else:
            QMessageBox.information(self, 'Notification', 'Select the item in the list first.')

    def __generateFinished(self, filename):
        self.__filename_dict[self.__cur_src_filename] = filename
        self.__view.setFilenameToRight(filename)

    def setModel(self, cur_model_name, cur_model_path):
        self.__cur_model_name = cur_model_name
        self.__cur_model_path = cur_model_path