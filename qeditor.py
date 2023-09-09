from PySide2 import QtWidgets, QtCore, QtGui

from pathlib import Path

class QEditor(QtWidgets.QWidget):

    def __init__(self, application, parent=None):
        super(QEditor, self).__init__(parent=parent)
        self.app = application
        self.labels = {f"label_{i}": "" for i in range(16)}
        self.w_brush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 255))
        self.b_brush = QtGui.QBrush(QtGui.QColor(10, 10, 10, 255))
        self.h_brush = QtGui.QBrush(QtGui.QColor(100, 100, 200, 30))
        self.w_pen = QtGui.QPen(self.w_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.b_pen = QtGui.QPen(self.b_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.h_pen = QtGui.QPen(self.h_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        
        self.font_label = QtGui.QFont()
        self.create_fields()
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setAttribute(QtCore.Qt.WA_InputMethodTransparent)
        #self.grabKeyboard()
        #self.move(0,self.app.menu.size().height())

    def run(self):
        #self.grabKeyboard()
        self.show()

    def update_labels(self):
       
        for buttons in self.app.buttons:
            i = f"label_{buttons.index}"
            keys = [ QtGui.QKeySequence(int(key)).toString() for key in self.app.keymap_map[str(buttons.index)] ]
            self.app.edi.labels[i].setText(f"{(' ').join(keys)}")
  
    def create_fields(self):
        
        for buttons in self.app.buttons:
            i = f"label_{buttons.index}"
            self.labels[i] = QtWidgets.QLabel("A",self)   
          
            self.labels[i].setProperty("keymap","on")
            self.font_label.setBold(True)
            self.font_label.setPixelSize(40)
            self.labels[i].setFont(self.font_label)
            #self.fields = QtWidgets.QLineEdit(self)
            self.labels[i].move(130 + (172 * (buttons.index % 4)), 70 + (172 * (int(buttons.index / 4))))
            self.labels[i].setText("B B U")
            #self.labels[i].setAlignment(QtCore.Qt.AlignHCenter) 
            self.labels[i].setScaledContents(True)
        self.app.set_shadows(list(self.labels.values()))

    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        """Override method from QWidget

        Paint the Pixmap into the widget

        """
        #with QtGui.QPainter(self) as painter:
        painter.setBrush(self.h_brush)
        painter.setPen(self.h_pen)
        #if self.app.show_key_editor.isChecked():
        #    painter.drawRect(event.rect())
       
    def sizeHint(self):
        #print("default sizeHint: ", super(QEditor, self).sizeHint())
        return QtCore.QSize(866, 688+self.app.menu.height())