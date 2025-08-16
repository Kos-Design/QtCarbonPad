from PySide2 import QtWidgets, QtCore, QtGui

from pathlib import Path

class QPad(QtWidgets.QLabel):

    def __init__(self, application, parent=None):
        super(QPad, self).__init__(parent=parent)
        self.app = application
        self.setAcceptDrops(True)
        self.index = 0
        self.maximumSize = (172, 172)
        self.minimumSize = (172, 172)
        self.setFrameStyle(0)
        self.w_brush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 255))
        self.b_brush = QtGui.QBrush(QtGui.QColor(10, 10, 10, 255))
        self.h_brush = QtGui.QBrush(QtGui.QColor(100, 100, 200, 100))
        self.editing = False
        self.w_pen = QtGui.QPen(self.w_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.b_pen = QtGui.QPen(self.b_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.h_pen = QtGui.QPen(self.h_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.rect = QtCore.QRect(10,10,400,400)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        #self.setAttribute(QtCore.Qt.WA_InputMethodTransparent)

    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setBrush(self.h_brush)
        painter.setPen(self.h_pen)
        self.rect = event.rect()
        if False :
            painter.drawEllipse(event.rect())
        
    def dragEnterEvent(self, event):
        for obj in event.mimeData().urls():
            if not Path(obj.toLocalFile()).is_file():
                event.ignore()
        event.accept()  

    def dragMoveEvent(self, event):
        for obj in event.mimeData().urls():
            if not Path(obj.toLocalFile()).is_file():
                event.ignore()
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(QtCore.Qt.CopyAction)
        _files = [file.toLocalFile() for file in event.mimeData().urls()]
        self.app.pad.set_sample(_files,self.index)
        self.app.save_default_bank() 
        if not self.app.hide_status_bar_checkbox.isChecked():
            self.app.statusBar().showMessage(f"Sample {Path(next(iter(_files))).name} assigned to Pad n°{self.index}")

    def mousePressEvent(self, e):
        if self.app.show_key_editor.isChecked():
            self.editing = True
        self.pressed_it()
    
    def pressed_it(self):
        if not self.app.pad.samples_files:
            return
        if not Path(f"{self.app.pad.samples_files[self.index]}").is_file():
            return
        self.app.pad.play_sample(self.index)
        self.setPixmap(self.app.pixmaps_off[self.index])
        if self.app.activate_midi_out.isChecked() :
            self.app.pad.send_midi_on_out(self.index)

    def received_ccs(self,val):
        if self.app.activate_midi_out.isChecked() :
            self.app.pad.send_midi_cc_out(self.index,val)

    def unpressed_it(self):
        self.setPixmap(self.app.pixmaps_on[self.index])
        if self.app.activate_midi_out.isChecked() :
            self.app.pad.send_midi_off_out(self.index)

    def mouseReleaseEvent(self, e):
        self.unpressed_it()
    
    def mouseDoubleClickEvent(self, e):
        self.pressed_it()
       