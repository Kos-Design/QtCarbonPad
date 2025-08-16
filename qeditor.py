from PySide2 import QtWidgets, QtCore, QtGui
from datetime import datetime
from pathlib import Path

class QEditor(QtWidgets.QWidget):

    def __init__(self, application, parent):
        super(QEditor, self).__init__(parent=parent)
        self.app = application
        self.parent = parent
        self.labels = {f"label_{i}": "" for i in range(16)}
        self.font_label = QtGui.QFont()
        self.create_fields()
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setAttribute(QtCore.Qt.WA_InputMethodTransparent)

    def run(self):
        #self.grabKeyboard()
        self.show()

    def update_labels(self):
        for buttons in self.parent.buttons:
            i = f"label_{buttons.index}"
            keys = [ str(QtGui.QKeySequence(int(key)).toString()) for key in self.parent.keymap_map[str(buttons.index)] ]
            self.labels[i].setText(f"{(' ').join(keys)}")
            self.labels[i].setScaledContents(True)
            self.parent.update()
            self.update()

    def create_fields(self):
        for buttons in self.parent.buttons:
            i = f"label_{buttons.index}"
            self.labels[i] = QtWidgets.QLabel("A",self)   
            self.labels[i].setProperty("keymap","on")
            self.font_label.setBold(True)
            self.font_label.setPixelSize(40)
            self.labels[i].setFont(self.font_label)
            self.labels[i].setGeometry(140 + (172 * (buttons.index % 4)), 38 + (172 * (int(buttons.index / 4))),100,100)
        self.set_heavy_shadows(list(self.labels.values()))
    
    def set_heavy_shadows(self, attr_list):
        for attr in attr_list:
            effect = QtWidgets.QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(6)
            effect.setOffset(2, 3)
            effect.setColor(QtGui.QColor(16, 16, 16, 200))
            attr.setGraphicsEffect(effect)

    def sizeHint(self):
        #print("default sizeHint: ", super(QEditor, self).sizeHint())
        return QtCore.QSize(866, 688+self.parent.menu.height())