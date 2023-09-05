# -*- coding: utf-8 -*-
"""
Main window of the Sound Pad.
"""

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QLabel, QSpinBox, QGridLayout, QGroupBox, QHBoxLayout,QVBoxLayout, QCheckBox, QMainWindow, QListView,QStatusBar, QWidgetAction, QComboBox, QAction, QWidget, QFileDialog, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PySide2.QtGui import QStandardItem, QIcon, QPixmap , QMouseEvent, QStandardItemModel
import sys
from pathlib import Path
from sampler_pad import SamplePlayer
import json
import itertools
from qpad import QPad
from qeditor import QEditor

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, application, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.dir = Path(str(__file__)).parent
        self.styled = open(f"{self.dir.joinpath('style.css')}").read()
        self.pad = SamplePlayer()
        
        self.background = QLabel()
        self.app = self.application = application
        self.title = "Carbonpad"
        self.setWindowTitle(self.title)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.keymap_map = {str(k): [] for k in range(16)}
        self.w_table = QtWidgets.QTableWidget(4,4)
        self.w_table.horizontalHeader().hide()
        self.w_table.verticalHeader().hide()
        self.w_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.w_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.w_table.verticalHeader().setStretchLastSection(False)
        self.w_table.horizontalHeader().setStretchLastSection(False)
       
        self.layout_grid = QtWidgets.QGridLayout()
        self.layout_grid.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.rect_placheholder = QtCore.QRect(0,0,89,89)
        self.grp = QGroupBox()
        self.setLayout(self.layout_grid)      
        self.setCentralWidget(self.grp)
        self.grp.setLayout(self.layout_grid)
        
        self.background.setParent(self)
        self.w_table.setParent(self)

        self.set_top_menu()
        self.place_buttons()
        self.background.setSizePolicy(QtWidgets.QSizePolicy.Policy(QtWidgets.QSizePolicy.Ignored),QtWidgets.QSizePolicy.Policy(QtWidgets.QSizePolicy.Ignored))
        self.adjustSize()
        self.resize(866, 688)
        self.setFixedSize(866, 688+self.menuBar().height())
        
        self.w_table.setGeometry(89, self.menuBar().height(), 688, 688)
        self.background.setGeometry(0, self.menuBar().height(), 866, 688)
        #self.w_table.clicked[QtCore.QModelIndex].connect(self.widget_click)
        self.set_the_palette([self.w_table,])
        self.w_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.w_table.clearSelection()
        self.edi = QEditor(self)
        self.edi.setParent(self)
        self.edi.hide()
        self.set_shadows([self.menuBar(),self.refresh_midi,self.op_group,self.channel_selector,self.hide_status_bar_checkbox,self.midilist,self.channel_label])
        self.setStyleSheet(self.styled)

        #self.set_blur([self.w_table,self.background])

    def set_shadows(self, attr_list):
        for attr in attr_list:
            effect = QtWidgets.QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(5)
            effect.setOffset(1, 2)
            effect.setColor(QtGui.QColor(16, 16, 16, 64))
            attr.setGraphicsEffect(effect)
    
    def set_blur(self, attr_list,blur=0):
        for attr in attr_list:
            effect = QtWidgets.QGraphicsBlurEffect(self)
            #effect.setBlurRadius(blur)
            #effect.blurRadius
            #effect.setColor(QtGui.QColor(16, 16, 16, 64))
            attr.setGraphicsEffect(effect)
            self.animate_prop(effect,((blur-50)*(blur-50))**0.5,blur)

    def animate_prop(self,prop,start=0,end=50):
        self.anim = QtCore.QPropertyAnimation(prop,b'blurRadius')
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic) if start == 0 else self.anim.setEasingCurve(QtCore.QEasingCurve.InCubic)
        
        self.anim.setDuration(300)
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()
    
    def keyPressEvent(self, e):
        key = QtGui.QKeySequence(e.key()).toString()
        is_modifier_key = ( e.modifiers() & (QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier)
            and not e.isAutoRepeat()
        )
        if e.key() in list(self.keymap_map.values()):
            print("assigned")

    def set_the_palette(self,widgets):
        pa = QtGui.QPalette()
        
        #co = QtGui.QColor(0,0,0,0)
        co = QtGui.Qt.transparent
        ba = QtGui.QBrush(co, QtCore.Qt.BrushStyle.NoBrush)
        pa.setColor(QtGui.QPalette.Highlight, co)
        pa.setColor(QtGui.QPalette.Highlight, co)
        pa.setBrush(QtGui.QPalette.Highlight, ba)
        pa.setColor(QtGui.QPalette.HighlightedText, co)
        pa.setColor(QtGui.QPalette.BrightText, co)
        pa.setColor(QtGui.QPalette.Window, co)
        pa.setColor(QtGui.QPalette.WindowText, co)
        pa.setColor(QtGui.QPalette.Base, co)
        pa.setColor(QtGui.QPalette.AlternateBase, co)

        pa.setColor(QtGui.QPalette.ToolTipBase, co)
        pa.setColor(QtGui.QPalette.ToolTipText, co)
        pa.setColor(QtGui.QPalette.PlaceholderText, co)
        pa.setColor(QtGui.QPalette.Text, co)
        pa.setColor(QtGui.QPalette.Button, co)
        pa.setColor(QtGui.QPalette.ButtonText, co)
       
        
        for wig in widgets:
            wig.setPalette(pa)

    def place_buttons(self):
        self.buttons = []
        self.list_of_buttons = sorted(self.dir.joinpath('themes/Carbon/buttons/On').glob('*.png'))
        self.list_of_buttons_off = sorted(self.dir.joinpath('themes/Carbon/buttons/Off').glob('*.png'))
        #print(self.list_of_buttons_off)
        #print(self.list_of_buttons)
        
        self.pixmaps_on = [QPixmap(str(x)) for x in self.list_of_buttons]
        self.pixmaps_off = [QPixmap(str(x)) for x in self.list_of_buttons_off]
        self.w_table.setShowGrid(False)
        self.w_table.setFrameStyle(0)
        
        i = 0
        for _ in itertools.repeat(None, 16):
            but = QPad(self)
            but.index = i
            
            self.set_the_palette([but,])
            self.w_table.horizontalHeader().setSectionResizeMode(i%4, QtWidgets.QHeaderView.ResizeToContents)
            self.w_table.verticalHeader().setSectionResizeMode(int(i / 4), QtWidgets.QHeaderView.ResizeToContents)
            self.w_table.setCellWidget(int(i / 4),i%4,but)
            self.w_table.cellWidget(int(i / 4),i%4).setFrameStyle(0)
            #self.w_table.cellWidget(int(i / 4),i%4).setQt::ItemIsSelectable == 0
            but.setPixmap(self.pixmaps_on[i])
            #but.setParent(self.background)
            self.buttons.append(but)
            i += 1
        self.w_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
         
        self.pixmap_bg = QPixmap('themes/Carbon/bgoff.png')
        self.background.setPixmap(self.pixmap_bg)
        self.background.move(0,0)
       
    def resizeEvent(self, e: QtGui.QResizeEvent):
        height = e.size().height() - self.menuBar().size().height()
        width = e.size().width()
        size = QtCore.QSize(width,height)
        #print(size)
        #self.pixmap_bg = self.pixmap_bg.scaled(width,height)
        #self.background.setPixmap(self.pixmap_bg)

    def set_top_menu(self):
        self.exit_btn = QAction("&Exit", self)
        self.save_bank_btn = QAction("&Save Sound Bank", self)
        self.load_bank_btn = QAction("&Load Sound Bank", self)
        self.help_btn = QAction("&Help", self)
        self.options_btn = QAction("&Options", self)
        self.file_menu = self.menuBar().addMenu("&File")
        self.edit_menu = self.menuBar().addMenu("&Edit")
        self.edit_menu.addAction(self.options_btn)
        self.about_menu = self.menuBar().addMenu("&About")
        self.about_menu.addAction(self.help_btn)
        self.file_menu.addAction(self.save_bank_btn)
        self.file_menu.addAction(self.load_bank_btn)
        self.file_submenu = self.file_menu.addMenu("&Exit")
        self.file_submenu.addAction(self.exit_btn)
        self.exit_btn.triggered.connect(self.exit_app)
        self.save_bank_btn.triggered.connect(self.save_bank)
        self.load_bank_btn.triggered.connect(self.load_bank)
        self.options_btn.triggered.connect(self.show_options)
        self.help_btn.triggered.connect(self.show_about)
        self.set_option_window()
    
    def set_option_window(self):
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
        self.option_window = QMainWindow(self)
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
        self.option_window.setCentralWidget(self.op_group)
        self.option_window.setWindowTitle("Options")
        self.refresh_midi.clicked.connect(self.set_midilist_items)
        
    def show_status_bar(self):
        if self.hide_status_bar_checkbox.isChecked():
            self.statusBar().hide()
            self.adjustSize()
            self.setFixedSize(866, 688+self.menuBar().height())
            
        else :
            self.statusBar().show()
            self.setFixedSize(866, 688+self.statusBar().height()+self.menuBar().height())
                                          
    def set_midilist_items(self):
        self.pad.init_pygame()
        self.midilist.model().clear()
        for device in self.pad.allinputdevices:
            self.midilist_model.appendRow(QStandardItem(' '.join([str(x).strip("b'") for x in device])))
        self.midilist.update()

    def save_bank(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix(".pls")
        file = dialog.getSaveFileName(self, "Sound Bank", "", "Sound Bank Files (*.json)")[0]
        if ".json" not in str(file):
            file += ".json"    
        with open(file, 'w') as playlist:
            json.dump(dict(zip(range(16),self.pad.lesfilnames)), playlist,indent=4)
            
    def load_bank(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setOption(QFileDialog.ShowDirsOnly,False)
        dialog.exec()
        with open(next(iter(dialog.selectedFiles())), 'r') as bank:
            self.pad.lesfilnames = list(json.load(bank).values())
            self.pad.loadbank()
    
    def key_editor(self):
        self.set_blur([self.w_table,],50*int(self.show_key_editor.isChecked()))
        if self.show_key_editor.isChecked():
            self.edi.show()
            self.releaseKeyboard()
            #self.edi.grabKeyboard()
        else :
            self.edi.hide()
            self.grabKeyboard()

        self.w_table.update()
    
    def keyPressEvent(self, e):
        key = QtGui.QKeySequence(e.key()).toString()
        is_modifier_key = ( e.modifiers() & (QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier)
            and not e.isAutoRepeat()
        )
        #print(self.keymap_map)
        for i in range(16):
   
            if str(e.key()) in self.keymap_map[f"{i}"] :
                self.buttons[i].pressed_it()
                
                #print (i, self.buttons[i].index)
                #TODO: check if no break for multi assign affects lattency increase ?
                #break
            
    def keyReleaseEvent(self, e):
        for i in range(16):
            #print(self.keymap_map)
            if str(e.key()) in self.keymap_map[str(i)] :
                self.buttons[i].unpressed_it()
                #print (i, self.buttons[i].index)
                

    def show_about(self):
        QMessageBox.information(self, "About","Written by Cosmin Planchon")

    def show_options(self):
        self.option_window.show()

    def exit_app(self):
        sys.exit()

