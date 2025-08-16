# -*- coding: utf-8 -*-
"""
Main window of the Sound Pad.
"""

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QMenuBar, QLabel, QSpinBox, QGridLayout, QGroupBox, QHBoxLayout,QVBoxLayout, QCheckBox, QMainWindow, QListView,QStatusBar, QWidgetAction, QComboBox, QAction, QWidget, QFileDialog, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PySide2.QtGui import QStandardItem, QIcon, QPixmap , QMouseEvent, QStandardItemModel,QPalette,QColor
import sys
from pathlib import Path
from sampler_pad import SamplePlayer
import json
import itertools
from qpad import QPad
from qeditor import QEditor
from platformdirs import user_config_dir

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, application, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.dir = Path(str(__file__)).parent
        self.styled = open(f"{self.dir.joinpath('style.css')}").read()
        self.pad = SamplePlayer(self)
        self.app = self.application = application
        self.title = "Carbonpad"
        self.setWindowTitle(self.title)
        self.set_top_menu()
        self.main_widget = QtWidgets.QWidget(self)
        self.menu_height = 16
        self.mainframe = QtWidgets.QFrame(self.main_widget)
        self.mainframe.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.keymap_map = json.loads(json.dumps({str(k): [] for k in range(16)}))
        self.layout_grid = QtWidgets.QGridLayout()
        self.layout_grid.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.setCentralWidget(self.main_widget)
        self.h_layout = QHBoxLayout(self.main_widget)
        self.set_background()
        self.set_w_table()
        self.edi = QEditor(self.app,self)
        self.edi.hide()
        self.edi.update_labels()
        self.setFixedSize(866, 688+self.menu_height)
        self.edi.setGeometry(0, self.menu_height, 866, 688)
        self.setStyleSheet(self.styled)
        self.main_widget.setStyleSheet(u"background: transparent;")
        self.check_config_file()
    
    def check_config_file(self):
        config_dir = Path(user_config_dir('QtPads', 'Kos-Design'))
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "QtPads_config.json"
        default_config = { "bank": "QtPads_bank", "keymap": "QtPads_keymap"}
        if config_file.exists():
            with config_file.open("r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            with config_file.open("w", encoding="utf-8") as f:
                config = default_config
                json.dump(default_config, f, indent=2)
        default_bank = config_dir / f"{config['bank']}.json"
        if default_bank.exists() and default_bank.is_file():
            with open(f"{default_bank}", 'r') as bank:
                self.pad.samples_files = list(json.load(bank).values())
                self.pad.assign_samples()
        default_keys = config_dir / f"{config['keymap']}.json"
        if default_keys.exists() and default_keys.is_file():
            with open(f"{default_keys}", 'r') as keymap:
                self.keymap_map = json.load(keymap)
                self.edi.update_labels()
               
    def save_default_keymap(self):
        config_dir = Path(user_config_dir('QtPads', 'Kos-Design'))
        default_keys = config_dir / "QtPads_keymap.json" 
        with open(f"{default_keys}", 'w') as mapped:
            json.dump(self.keymap_map, mapped,indent=4)
    
    def save_default_bank(self):
        config_dir = Path(user_config_dir('QtPads', 'Kos-Design'))
        default_bank = config_dir / "QtPads_bank.json" 
        with open(f"{default_bank}", 'w') as bank:
            json.dump(dict(zip(range(16),self.pad.samples_files)), bank,indent=4)
            
    def set_background(self):
        self.background = QLabel()
        self.pixmap_bg = QPixmap(f"{self.dir.joinpath('themes/Carbon/bgoff.png')}")
        self.background.setPixmap(self.pixmap_bg)
        self.background.setParent(self.main_widget)
        self.background.setGeometry(0, 0, 866, 688)
        self.background.setSizePolicy(QtWidgets.QSizePolicy.Policy(QtWidgets.QSizePolicy.Ignored),QtWidgets.QSizePolicy.Policy(QtWidgets.QSizePolicy.Ignored))

    def set_w_table(self):
        self.w_table = QtWidgets.QTableWidget(4,4)
        self.w_table.horizontalHeader().hide()
        self.w_table.verticalHeader().hide()
        self.w_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.w_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.w_table.verticalHeader().setStretchLastSection(False)
        self.w_table.horizontalHeader().setStretchLastSection(False)
        self.set_the_palette([self.w_table,])
        self.w_table.setParent(self.main_widget)
        self.w_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.w_table.clearSelection()
        self.w_table.setGeometry(89, 0, 688, 688)
        self.w_table.setShowGrid(False)
        self.w_table.setFrameStyle(0)
        self.place_buttons()

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
            self.animate_prop(effect,((blur-15)*(blur-15))**0.5,blur)

    def animate_prop(self,prop,start=0,end=15):
        self.anim = QtCore.QPropertyAnimation(prop,b'blurRadius')
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic) if start == 0 else self.anim.setEasingCurve(QtCore.QEasingCurve.InCubic)
        
        self.anim.setDuration(300)
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()
    
    def set_the_palette(self,widgets):
        pa = QtGui.QPalette()
        palette = QPalette()
        palette.setColor(QPalette.Background, QtGui.QColor('lightblue'))
        co = QtGui.QColor(0,0,0,0)
        #co = QtGui.Qt.transparent
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
            wig.setPalette(palette)

    def place_buttons(self):
        
        self.buttons = []
        self.list_of_buttons = sorted(self.dir.joinpath('themes/Carbon/buttons/On').glob('*.png'))
        self.list_of_buttons_off = sorted(self.dir.joinpath('themes/Carbon/buttons/Off').glob('*.png'))
        self.pixmaps_on = [QPixmap(str(x)) for x in self.list_of_buttons]
        self.pixmaps_off = [QPixmap(str(x)) for x in self.list_of_buttons_off]
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
        #self.w_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
         
    def set_top_menu(self):
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("&File")
        self.exit_btn = QAction("&Exit", self)
        self.save_bank_btn = QAction("&Save Sound Bank", self)
        self.load_bank_btn = QAction("&Load Sound Bank", self)
        self.save_keys = QAction("&Save Keymap", self)
        self.load_keys = QAction("&Load KeyMap", self)
        self.help_btn = QAction("&Help", self)
        self.options_btn = QAction("&Options", self)
        
        self.edit_menu = self.menu.addMenu("&Edit")
        self.keymap_menu = self.file_menu.addMenu("&Keymap")
        self.soundbank_menu = self.file_menu.addMenu("&SoundBank")

        self.edit_menu.addAction(self.options_btn)
        self.about_menu = self.menu.addMenu("&About")
        self.about_menu.addAction(self.help_btn)
        self.soundbank_menu.addAction(self.save_bank_btn)
        self.soundbank_menu.addAction(self.load_bank_btn)
        
        self.file_submenu = self.file_menu.addMenu("&Exit")
        self.file_submenu.addAction(self.exit_btn)
        self.keymap_menu.addAction(self.save_keys)
        self.keymap_menu.addAction(self.load_keys)
        self.exit_btn.triggered.connect(self.exit_app)
        self.save_bank_btn.triggered.connect(self.save_bank)
        self.load_bank_btn.triggered.connect(self.load_bank)
        self.save_keys.triggered.connect(self.save_keymap)
        self.load_keys.triggered.connect(self.load_keymap)
        self.options_btn.triggered.connect(self.show_options)
        self.help_btn.triggered.connect(self.show_about)
        self.option_window = QWidget()  
 
        self.midilist = QListView()
        self.midilist_out = QListView()
        self.placeholder_0 = QtWidgets.QLabel("")
        self.transpose_midi = QtWidgets.QLabel("Transpose Midi: ")
        self.refresh_midi = QPushButton("Refresh")
        self.midilist_in_model = QStandardItemModel()
        self.midilist.setModel(self.midilist_in_model)
        self.midilist_out_model = QStandardItemModel()
        self.midilist_out.setModel(self.midilist_out_model)
        self.activate_midi_out = QCheckBox("Send Midi Out")
        self.activate_midi_in = QCheckBox("Receive Midi In")
        self.activate_midi_in.setChecked(True)
        self.activate_midi_in.stateChanged.connect(self.pad.rearm_midi_listener)
        self.show_key_editor = QCheckBox("Show Keymap Editor")
        self.show_key_editor.stateChanged.connect(self.key_editor)
        #self.option_window = QMainWindow(self.app)
        self.hide_status_bar_checkbox = QCheckBox("Hide Status Bar")
        self.hide_status_bar_checkbox.setChecked(True)
        self.hide_status_bar_checkbox.stateChanged.connect(self.show_status_bar)
        self.op_glay = QGridLayout()
        self.set_midilist_items()
        self.op_vlay = QVBoxLayout()
        self.op_subh_lay = QHBoxLayout()
        self.op_glay.addWidget(self.midilist,0,0,2,1)
        self.op_glay.addLayout(self.op_vlay,0,1,2,1)
        self.op_glay.addWidget(self.midilist_out,0,2,2,1)
        self.transposer = QSpinBox()
        self.transposer.setMinimum(-64)
        self.transposer.setMaximum(64)
        self.op_vlay.addWidget(self.placeholder_0)
        self.op_vlay.addWidget(self.show_key_editor)
        self.op_vlay.addWidget(self.activate_midi_in)
        self.op_vlay.addWidget(self.activate_midi_out)
        self.op_vlay.addWidget(self.hide_status_bar_checkbox)
        self.op_vlay.addLayout(self.op_subh_lay)
        self.op_subh_lay.addWidget(self.transpose_midi)
        self.op_subh_lay.addWidget(self.transposer)
        self.op_vlay.addWidget(self.refresh_midi)
        self.op_group = QGroupBox()
        self.op_group.setLayout(self.op_glay)
        self.refresh_midi.clicked.connect(self.set_midilist_items)
        self.midilist.selectionModel().selectionChanged.connect(self.pad.in_device_selected)
        self.midilist_out.selectionModel().selectionChanged.connect(self.pad.out_device_selected)

    def show_status_bar(self):
        if self.hide_status_bar_checkbox.isChecked():
            self.statusBar().hide()
            self.adjustSize()
            self.setFixedSize(866, 688+self.menu.height())
            
        else :
            self.statusBar().show()
            self.setFixedSize(866, 688+self.statusBar().height()+self.menu.height())
                                          
    def set_midilist_items(self):
        self.pad.init_pygame()
        self.midilist.model().clear()
        for device in self.pad.in_devices:
            self.midilist_in_model.appendRow(QStandardItem(' '.join([str(x).strip("b'") for x in device])))
        self.midilist.update()
        self.set_midi_out_items()
    
    def set_midi_out_items(self):
        self.midilist_out.model().clear()
        for device in self.pad.out_devices:
            self.midilist_out_model.appendRow(QStandardItem(' '.join([str(x).strip("b'") for x in device])))
        self.midilist_out.update()    

    def key_editor(self):
        self.set_blur([self.w_table,],15*int(self.show_key_editor.isChecked()))
        if self.show_key_editor.isChecked():
            self.edi.run()
            self.edi.update()
        else :
            self.edi.hide()
        self.w_table.update()
    
    def save_bank(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix(".pls")
        file = dialog.getSaveFileName(self, "Sound Bank", "", "Sound Bank Files (*.json)")[0]
        if ".json" not in str(file):
            file += ".json"    
        with open(file, 'w') as playlist:
            json.dump(dict(zip(range(16),self.pad.samples_files)), playlist,indent=4)
            
    def load_bank(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setOption(QFileDialog.ShowDirsOnly,False)
        dialog.exec()
        with open(next(iter(dialog.selectedFiles())), 'r') as bank:
            self.pad.samples_files = list(json.load(bank).values())
            self.pad.assign_samples()
        self.save_default_bank()
    
    def save_keymap(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix(".pls")
        file = dialog.getSaveFileName(self, "KeyMap", "", "Key Assignement Files (*.json)")[0]
        if ".json" not in str(file):
            file += ".json"    
        with open(file, 'w') as mapped:
            json.dump(self.keymap_map, mapped,indent=4)
            
    def load_keymap(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setOption(QFileDialog.ShowDirsOnly,False)
        dialog.exec()
        with open(next(iter(dialog.selectedFiles())), 'r') as mapped:
            self.keymap_map = json.load(mapped)
            self.edi.update_labels()
        self.save_default_keymap()
    
    def keyPressEvent(self, e):
        is_modifier_key = ( e.modifiers() & (QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier)
            and not e.isAutoRepeat()
        )
        for butt in self.buttons:
            if butt.editing:
                if not is_modifier_key :
                    self.keymap_map[f"{butt.index}"].append(str(e.key()))
                    self.edi.update_labels()
                    self.save_default_keymap()
                butt.editing = False 
            if str(e.key()) in self.keymap_map[f"{butt.index}"] :
                butt.pressed_it()
                  
    def keyReleaseEvent(self, e):
        for i in range(16):
            if str(e.key()) in self.keymap_map[str(i)] :
                self.buttons[i].unpressed_it()
                         
    def show_about(self):
        QMessageBox.information(self, "About","4x4 Midi Pad Sample player\nWritten by Cosmin Planchon")

    def show_options(self):
        self.op_group.show()

    def exit_app(self):
        sys.exit()

