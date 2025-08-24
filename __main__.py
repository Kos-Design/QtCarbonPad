
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
        self.post_init(args)

    def run(self):
        self.main_window.show()
        return (self.pyside_app.exec_())

    def post_init(self,args):
        if len(args)>1:     
            if args[1] == "custom":
                #loads 3rd midi instrument(usb midi pads) as input and the teensy sequencer as output midi target devices 
                third_index = self.main_window.midilist.model().index(3, 0)
                selection_model = self.main_window.midilist.selectionModel()
                selection_model.select(third_index, selection_model.Select | selection_model.Rows)
                # Update the current selection (optional, but triggers a change event too)
                selection_model.setCurrentIndex(third_index, selection_model.Select)
                second_index = self.main_window.midilist.model().index(1, 0)
                selection_model_2 = self.main_window.midilist_out.selectionModel()
                selection_model_2.setCurrentIndex(second_index, selection_model_2.Select)
                self.main_window.activate_midi_out.toggle()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    application = CarbonPad(sys.argv)
    sys.exit(application.run())