import subprocess

from PyQt5.QtCore import QThread, pyqtSignal


class ConsoleThread(QThread):
    updated = pyqtSignal(str)

    def __init__(self, command):
        super(ConsoleThread, self).__init__()
        self.__command = command

    def run(self):
        try:
            process = subprocess.Popen(
                self.__command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                errors='replace'
            )

            while True:
                realtime_output = process.stdout.readline()
                if realtime_output == '' and process.poll() is not None:
                    print('Thread end for a variant of reasons')
                    break
                if realtime_output:
                    self.updated.emit(realtime_output.strip())
        except Exception as e:
            print(e)
            raise Exception(e)

