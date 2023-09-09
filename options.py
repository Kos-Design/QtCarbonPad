from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QLabel, QSpinBox, QGridLayout, QGroupBox, QHBoxLayout,QVBoxLayout, QCheckBox, QMainWindow, QListView,QStatusBar, QWidgetAction, QComboBox, QAction, QWidget, QFileDialog, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PySide2.QtGui import QStandardItem, QIcon, QPixmap , QMouseEvent, QStandardItemModel

from pathlib import Path

class OptionsPanel(QtWidgets.QWidget):

    def __init__(self, application, parent=None):
        super(OptionsPanel, self).__init__(parent=parent)
        self.parent = parent
        self.app = application
        self.pad = self.parent.pad
        self.midilist = QListView()
        self.midilist_out = QListView()
        self.placeholder_0 = QtWidgets.QLabel("")
        self.channel_label = QtWidgets.QLabel("Midi Channel: ")
        self.refresh_midi = QPushButton("Refresh")
        self.midilist_model = QStandardItemModel()
        self.midilist.setModel(self.midilist_model)
        self.activate_midi_out = QCheckBox("Send Midi Out")
        self.show_key_editor = QCheckBox("Show Keymap Editor")
        self.show_key_editor.stateChanged.connect(self.key_editor)
        #self.option_window = QMainWindow(self.app)
        self.hide_status_bar_checkbox = QCheckBox("Hide Status Bar")
        self.hide_status_bar_checkbox.stateChanged.connect(self.show_status_bar)
        self.op_glay = QGridLayout()
        self.set_midilist_items()
        self.op_vlay = QVBoxLayout()
        self.op_subh_lay = QHBoxLayout()
        self.op_glay.addWidget(self.midilist,0,0,2,1)
        self.op_glay.addLayout(self.op_vlay,0,1,2,1)
        self.op_glay.addWidget(self.midilist_out,0,2,2,1)
        self.channel_selector = QSpinBox()
        self.op_vlay.addWidget(self.placeholder_0)
        self.op_vlay.addWidget(self.show_key_editor)
        self.op_vlay.addWidget(self.activate_midi_out)
        self.op_vlay.addWidget(self.hide_status_bar_checkbox)
        self.op_vlay.addLayout(self.op_subh_lay)
        self.op_subh_lay.addWidget(self.channel_label)
        self.op_subh_lay.addWidget(self.channel_selector)
        self.op_vlay.addWidget(self.refresh_midi)
        self.op_group = QGroupBox()
        self.op_group.setLayout(self.op_glay)
        #self.option_window.setCentralWidget(self.op_group)
        self.setWindowTitle("Options")
        self.refresh_midi.clicked.connect(self.set_midilist_items)
        #self.parent.set_shadows([self.refresh_midi,self.op_group,self.channel_selector,self.hide_status_bar_checkbox,self.midilist,self.channel_label])
        #self.setStyleSheet(self.parent.styled)
        
        #self.setAttribute(QtCore.Qt.WA_InputMethodTransparent)
      
    def show_status_bar(self):
        if self.hide_status_bar_checkbox.isChecked():
            self.parent.statusBar().hide()
            self.parent.adjustSize()
            self.parent.setFixedSize(866, 688+self.parent.menu.height())
            
        else :
            self.parent.statusBar().show()
            self.parent.setFixedSize(866, 688+self.parent.statusBar().height()+self.parent.menu.height())
                                          
    def set_midilist_items(self):
        self.pad.init_pygame()
        self.midilist.model().clear()
        for device in self.pad.allinputdevices:
            self.midilist_model.appendRow(QStandardItem(' '.join([str(x).strip("b'") for x in device])))
        self.midilist.update()

    def key_editor(self):
        self.parent.set_blur([self.parent.w_table,],15*int(self.show_key_editor.isChecked()))
        if self.show_key_editor.isChecked():
            self.parent.edi.run()
            #self.parent.edi.grabKeyboard()
            
            self.parent.edi.update()
            
        else :
            self.parent.edi.hide()
            #self.parent.edi.releaseKeyboard()

        self.parent.w_table.update()
    
    def run(self):
        self.op_group.show()
        #self.parent.show()