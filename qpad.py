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
        #self.setPixmap(self.app.pixmaps_on[self.index])
        self.w_brush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 255))
        self.b_brush = QtGui.QBrush(QtGui.QColor(10, 10, 10, 255))
        self.h_brush = QtGui.QBrush(QtGui.QColor(100, 100, 200, 100))

        self.w_pen = QtGui.QPen(self.w_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.b_pen = QtGui.QPen(self.b_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.h_pen = QtGui.QPen(self.h_brush, 1, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap)
        self.rect_deco = QtCore.QRect(10,10,400,400)
        #self.setAcceptDrops(True)
        #self.index = 0
        #self.maximumSize = (172, 172)
        #self.minimumSize = (172, 172)
        #self.setFrameStyle(0)
        #self.setPixmap(self.app.pixmaps_on[self.index])

    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        """Override method from QWidget

        Paint the Pixmap into the widget

        """
        #with QtGui.QPainter(self) as painter:
        painter.setBrush(self.h_brush)
        painter.setPen(self.h_pen)
        painter.drawText(event.rect(),QtCore.Qt.AlignCenter,'T')
        if False :
            #not self.app.show_key_editor.isChecked():
            painter.drawEllipse(event.rect())
        
    def dragEnterEvent(self, event):
        """
        Triggered when initiating a drag'n drop event.

        Args:
            event: Qt event.
        """
        #print(event.mimeData().formats())
        for obj in event.mimeData().urls():
            if not Path(obj.toLocalFile()).is_file():
                event.ignore()
        event.accept()
        #event.ignore()
    
        #self.setCursor(QtCore.Qt.IBeamCursor)    

    def dragMoveEvent(self, event):
        """
        Triggered when dragging with the mouse on the window.

        Args:
            event: Qt event.
        """
        #print(event.mimeData().formats())
        for obj in event.mimeData().urls():
            if not Path(obj.toLocalFile()).is_file():
                event.ignore()

        event.accept()
   

    def dropEvent(self, event):
        """
        Triggered when dropping an element in the window.

        Args:
            event: Qt event.
        """ 
        event.setDropAction(QtCore.Qt.CopyAction)
        _files = [file.toLocalFile() for file in event.mimeData().urls()]
        self.app.pad.set_sample(_files,self.index)  
        self.app.statusBar().showMessage(f"Sample {Path(next(iter(_files))).name} assigned to Pad n°{self.index}")

    def mousePressEvent(self, e):
        if self.app.show_key_editor.isChecked():
            self.capture_keyboard()
        self.pressed_it()
        #self.app.w_table.clearSelection()
    
    def pressed_it(self):
        self.app.pad.playlesoundi(self.index)
        self.setPixmap(self.app.pixmaps_off[self.index])
    
    def unpressed_it(self):
        self.setPixmap(self.app.pixmaps_on[self.index])

    def capture_keyboard (self):
        self.grabKeyboard()
     
    def keyPressEvent(self, e):
        key = QtGui.QKeySequence(e.key()).toString()
        is_modifier_key = ( e.modifiers() & (QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier)
            and not e.isAutoRepeat()
        )
        if self.app.show_key_editor.isChecked() and not is_modifier_key :
            self.app.keymap_map[f"{self.index}"].append(str(e.key()))

    def mouseReleaseEvent(self, e):
        self.unpressed_it()
    
    def mouseDoubleClickEvent(self, e):
        self.pressed_it()
       