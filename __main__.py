
import sys
import logging
from PySide2.QtCore import Qt,QCoreApplication
from PySide2.QtWidgets import QApplication
from main_window import MainWindow

class CarbonPad:

    def __init__(self, args):
        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        self.pyside_app = QApplication(sys.argv)
        self.main_window = MainWindow(application=self)
        #self.option_window = self.main_window.option_window
        

    def run(self):
        self.main_window.show()
        return (self.pyside_app.exec_())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    application = CarbonPad(sys.argv)
    sys.exit(application.run())