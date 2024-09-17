import json
from pathlib import Path

from os import environ
from PySide2 import QtCore
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as sound_engine
import pygame.midi
import rtmidi2

class SamplePlayer():

    def __init__(self,parent):
        self.app = parent
        sound_engine.init()
        sound_engine.mixer.pre_init(44100, -16, 2, 2048)
        sound_engine.mixer.init()
        self.dir = Path(__file__).parent
        self.in_devices = []
        self.my_input = None
        self.audiosamplesfolder = f"{self.dir.joinpath('soundkit')}"
        self.samplers = []
        self.lasoundbank = []
        self.currentmididevice = 0
        self.midi_out = None
        try:
            self.samples_files = [str(x.name) for x in Path(self.audiosamplesfolder).glob("*.*")]
            self.samples_files.sort()
            self.load_soundbank()
        except FileNotFoundError:
            self.samples_files = list(range(16))
            if not self.app.hide_status_bar_checkbox.isChecked():
                self.app.statusBar().showMessage(f"Error loading content of {self.audiosamplesfolder}")
                   
        self.init_pygame()

    def init_pygame(self):
        if sound_engine.midi.get_init() :
            sound_engine.midi.quit()
        sound_engine.midi.init()
        self.list_midi_devices()

    def load_soundbank(self):
        for i in range(0, 16):
            self.samples_files[i] = str(Path(self.audiosamplesfolder).joinpath(self.samples_files[i]))
            self.samplers.append(sound_engine.mixer.Sound(self.samples_files[i]))

    def set_sample(self,samples,i):
        self.samples_files[i] = str(next(iter(samples)))
        self.samplers[i] = sound_engine.mixer.Sound(str(next(iter(samples))))

    def list_midi_devices(self):
        self.all_devices = []
        self.in_devices = []
        self.out_devices = []
        for n in range(sound_engine.midi.get_count()):
            self.all_devices.append(sound_engine.midi.get_device_info(n))
            if sound_engine.midi.get_device_info(n)[2] == 1:
                self.in_devices.append(sound_engine.midi.get_device_info(n))
            elif sound_engine.midi.get_device_info(n)[3] == 1:
                self.out_devices.append(sound_engine.midi.get_device_info(n))

    def number_to_note(self,number):
        notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
        return notes[number % 12]

    def listen_midi(self,input_device):
        #clock = sound_engine.time.Clock()
        if input_device.poll():
            data, timestamp = input_device.read(1)[0]
            midi_msg, channel = rtmidi2.splitchannel(data[0])
            note_number = data[1]
            velocity = data[2]
            for i in range(0, 16):
                if (note_number + 4) % 16 == i and midi_msg == 144 :
                    if velocity > 0:
                        self.app.buttons[i].pressed_it()
                        if not self.app.hide_status_bar_checkbox.isChecked():
                            self.app.statusBar().showMessage(f"Sending Midi {(self.number_to_note(note_number), velocity)}")
                    if velocity == 0:
                        self.app.buttons[i].unpressed_it()
                
                if (note_number + 4) % 16 == i and midi_msg == 176 :
                    self.app.buttons[i].received_ccs(data[2])
                        #if not self.app.hide_status_bar_checkbox.isChecked():
                        #    self.app.statusBar().showMessage(f"Sending Midi {(self.number_to_note(note_number), velocity)}")
                    #if velocity == 0:
                    #    self.app.buttons[i].unpressed_it()
                
                if (note_number + 4) % 16 == i and midi_msg == 128 :
                    self.app.buttons[i].unpressed_it()

        if self.app.activate_midi_in.isChecked():
            QtCore.QTimer.singleShot(10, lambda: self.rearm_midi_listener())

    def play_sample(self, i):
        self.samplers[i].stop()
        self.samplers[i].play()

    def assign_samples(self):
        for i in range(0, 16):
            self.samplers[i] = sound_engine.mixer.Sound(self.samples_files[i])

    def rearm_midi_listener(self):
        if self.app.activate_midi_in.isChecked():
            try:
                self.listen_midi(self.my_input)
            except(NameError):
                pass

    def out_device_selected(self,event):
        #TODO: test if midi is initialized
        #sound_engine.midi.quit()
        #sound_engine.midi.init()
        device = event.indexes()[0].row()
        for out_device in self.all_devices:
            if out_device == self.out_devices[device]:
                self.midi_out = sound_engine.midi.Output(self.all_devices.index(out_device))
               
    def send_midi_on_out(self,index):
        self.midi_out.note_on(64+index+self.app.transposer.value(), 64, 0)
    
    def send_midi_cc_out(self,index,val):
        self.midi_out.write_short(0xB0, 64+index+self.app.transposer.value(), val)
        #self.midi_out. .note_on(64+index+self.app.transposer.value(), 64, 0)
    
    def send_midi_off_out(self,index):
        self.midi_out.note_off(64+index+self.app.transposer.value(), 0, 0)
     
    def in_device_selected(self,event):
        sound_engine.midi.quit()
        sound_engine.midi.init()
        """ handle item selected event
        """
        row = event.indexes()[0].row()
        for device in self.all_devices:
            if device == self.in_devices[row]:
                self.my_input = sound_engine.midi.Input(self.all_devices.index(device))
                self.listen_midi(self.my_input)
                break
