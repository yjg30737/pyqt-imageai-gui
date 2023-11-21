from PyQt5.QtCore import QThread, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy

from findPathWidget import FindPathWidget


class Thread(QThread):
    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        try:
            pass
        except Exception as e:
            raise Exception(e)


class ObjectDetectionFromVideoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__findPathWidget = FindPathWidget()
        self.__findPathWidget.getLineEdit().setPlaceholderText('Choose the Video File...')
        self.__findPathWidget.setExtOfFiles('Video Files (*.mp4)')
        self.__findPathWidget.added.connect(self.__videoFileAdded)

        self.__playBtn = QPushButton('Play')
        self.__playBtn.clicked.connect(self.__playVideo)
        self.__playBtn.setEnabled(False)

        self.__mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.__videoWidget = QVideoWidget()
        self.__videoWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(self.__findPathWidget)
        lay.addWidget(self.__videoWidget)
        lay.addWidget(self.__playBtn)
        lay.setAlignment(Qt.AlignTop)

        self.__mediaPlayer.setVideoOutput(self.__videoWidget)

        self.setLayout(lay)

    def __videoFileAdded(self, filename):
        self.__playBtn.setEnabled(True)
        self.__mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))

    def __run(self):
        self.__t = Thread()
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