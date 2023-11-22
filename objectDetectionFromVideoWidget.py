import os

from PyQt5.QtCore import QThread, Qt, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy, QMessageBox

from findPathWidget import FindPathWidget
from script import get_result_video_by_doing_object_detection


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
            get_result_video_by_doing_object_detection(self.__model_name, self.__model_path, src_filename=self.__filename, dst_filename=dst_filename)
            self.generateFinished.emit(dst_filename)
        except Exception as e:
            raise Exception(e)


class ObjectDetectionFromVideoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__cur_model_name = ''
        self.__cur_model_path = ''

    def __initUi(self):
        self.__findPathWidget = FindPathWidget()
        self.__findPathWidget.getLineEdit().setPlaceholderText('Choose the Video File...')
        self.__findPathWidget.setExtOfFiles('Video Files (*.mp4)')
        self.__findPathWidget.added.connect(self.__videoFileAdded)

        self.__runBtn = QPushButton('Run')
        self.__runBtn.clicked.connect(self.__run)
        self.__runBtn.setEnabled(False)

        self.__playBtn = QPushButton('Play')
        self.__playBtn.clicked.connect(self.__playVideo)
        self.__playBtn.setEnabled(False)

        self.__mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.__videoWidget = QVideoWidget()
        self.__videoWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(self.__findPathWidget)
        lay.addWidget(self.__runBtn)
        lay.addWidget(self.__videoWidget)
        lay.addWidget(self.__playBtn)
        lay.setAlignment(Qt.AlignTop)

        self.__mediaPlayer.setVideoOutput(self.__videoWidget)

        self.setLayout(lay)

    def __videoFileAdded(self, filename):
        self.__runBtn.setEnabled(True)
        self.__playBtn.setEnabled(True)
        self.__mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))

    def __run(self):
        filename = self.__findPathWidget.getLineEdit().text()
        self.__t = Thread(filename, self.__cur_model_name, self.__cur_model_path)
        self.__t.started.connect(self.__started)
        self.__t.finished.connect(self.__finished)
        self.__t.start()

    def __started(self):
        print('started')

    def __finished(self):
        print('finished')

    def __playVideo(self):
        if self.__mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.__playBtn.setText('Play')
            self.__mediaPlayer.pause()
        else:
            self.__playBtn.setText('Pause')
            self.__mediaPlayer.play()

    def __generateFinished(self, filename):
        QMessageBox.information(self, 'Finished', 'Processing Finished!')
        self.__mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))

    def setModel(self, cur_model_name, cur_model_path):
        self.__cur_model_name = cur_model_name
        self.__cur_model_path = cur_model_path