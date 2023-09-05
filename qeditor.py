from PySide2 import QtWidgets, QtCore, QtGui

from pathlib import Path

class QEditor(QtWidgets.QLabel):

    def __init__(self, application, parent=None):
        super(QEditor, self).__init__(parent=parent)
        self.app = application
        self.w_brush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 255))
        self.b_brush = QtGui.QBrush(QtGui.QColor(10, 10, 10, 255))
        self.h_brush = QtGui.QBrush(QtGui.QColor(100, 100, 200, 30))

        self.w_pen = QtGui.QPen(self.w_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.b_pen = QtGui.QPen(self.b_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.h_pen = QtGui.QPen(self.h_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.rect_deco = QtCore.QRect(10,10,400,400)
        self.font_label = QtGui.QFont()
        self.create_fields()
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.grabKeyboard()

    def create_fields(self):
        self.labels = {f"label_{i}": "" for i in range(16)}
        for buttons in self.app.buttons:
            i = f"label_{buttons.index}"
            self.labels[i] = QtWidgets.QLabel("A",self)    
            self.label_0 = QtWidgets.QLabel("A",self)
            self.labels[i].setProperty("keymap","on")
            self.font_label.setBold(True)
            self.font_label.setPixelSize(50)
            self.labels[i].setFont(self.font_label)
            #self.fields = QtWidgets.QLineEdit(self)
            self.labels[i].move(170+172*(buttons.index%4),100+172*(buttons.index%4))

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
    
    def mousePressEvent(self, e):
        pass
        #self.app.pad.playlesoundi(self.index)
        #self.setPixmap(self.app.pixmaps_off[self.index])
        #self.app.w_table.clearSelection()

    def mouseReleaseEvent(self, e):
        pass
        #self.setPixmap(self.app.pixmaps_on[self.index])
    
    def keyPressEvent(self, e):
        key = QtGui.QKeySequence(e.key()).toString()
        is_modifier_key = ( e.modifiers() & (QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier)
            and not e.isAutoRepeat()
        )
        if self.app.show_key_editor.isChecked() and not is_modifier_key :
            self.label_0.setText(key)

    def sizeHint(self):
        print("default sizeHint: ", super(QEditor, self).sizeHint())
        return QtCore.QSize(640, 480)