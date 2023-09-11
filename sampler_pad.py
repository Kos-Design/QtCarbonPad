import json
from pathlib import Path
import pygame.midi
from os import environ
from PySide2 import QtCore
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import rtmidi2

class SamplePlayer():

    def __init__(self,parent):
        self.app = parent
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        self.dir = Path(__file__).parent
        self.allinputdevices = []
        self.my_input = None
        self.audiosamplesfolder = f"{self.dir.joinpath('soundkit')}"
        self.lesplayers = []
        self.lasoundbank = []
        self.currentmididevice = 0
        self.midi_out = None
        try:
            self.lesfilnames = [str(x.name) for x in Path(self.audiosamplesfolder).glob("*.*")]
            self.lesfilnames.sort()
            
            self.load_soundbank()
        except FileNotFoundError:
            self.lesfilnames = list(range(16))
            print("Soundbank not found")

        self.init_pygame()
       
        #self.getsecondtinput()

    def init_pygame(self):
        if pygame.midi.get_init() :
            pygame.midi.quit()
        pygame.midi.init()
        self.listoutdevices()
        #self.print_devices()

    def load_soundbank(self):
        for i in range(0, 16):
            self.lesfilnames[i] = str(Path(self.audiosamplesfolder).joinpath(self.lesfilnames[i]))
            self.lesplayers.append(pygame.mixer.Sound(self.lesfilnames[i]))

    def set_sample(self,samples,i):
        self.lesfilnames[i] = str(next(iter(samples)))
        self.lesplayers[i] = pygame.mixer.Sound(str(next(iter(samples))))

    def listoutdevices(self):
        self.all_devices = []
        self.allinputdevices = []
        self.alloutputdevices = []
        for n in range(pygame.midi.get_count()):
            self.all_devices.append(pygame.midi.get_device_info(n))
            if pygame.midi.get_device_info(n)[2] == 1:
                self.allinputdevices.append(pygame.midi.get_device_info(n))
            elif pygame.midi.get_device_info(n)[3] == 1:
                self.alloutputdevices.append(pygame.midi.get_device_info(n))


    def print_devices(self):
        for n in range(pygame.midi.get_count()):
            print(n, pygame.midi.get_device_info(n))

    def number_to_note(self,number):
        notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
        return notes[number % 12]

    def readInput(self,input_device):
        #clock = pygame.time.Clock()
        if input_device.poll():
            event = input_device.read(1)[0]
            data = event[0]
            lemessagemidi, channel = rtmidi2.splitchannel(data[0])
            timestamp = event[1]
            note_number = data[1]
            velocity = data[2]
            if lemessagemidi == 144:
                if velocity > 0:
                    nodulo = (note_number + 4) % 16
                    for i in range(0, 16):
                        if nodulo == i:
                            self.app.buttons[i].pressed_it()

                    print(self.number_to_note(note_number), velocity)
                if velocity == 0:
                    nodulo = (note_number + 4) % 16

                    for i in range(0, 16):
                        if nodulo == i:
                            self.app.buttons[i].unpressed_it()
        QtCore.QTimer.singleShot(10, lambda: self.doreadm())

    def getsecondtinput(self):
        self.listoutdevices()
        for n in range(pygame.midi.get_count()):
            if len(self.allinputdevices) > 0:
                if pygame.midi.get_device_info(n) == self.allinputdevices[0]:
                    self.my_input = pygame.midi.Input(n)

    def playlesoundi(self, i):
        self.lesplayers[i].stop()
        self.lesplayers[i].play()

    def loadbank(self):
        for i in range(0, 16):
            self.lesplayers[i] = pygame.mixer.Sound(self.lesfilnames[i])

    def doreadm(self):
        try:
            self.readInput(self.my_input)
        except(NameError):
            pass

    def out_device_selected(self,event):
        pygame.midi.quit()
        pygame.midi.init()
        device = event.indexes()[0].row()
        for out_device in self.all_devices:
            if out_device == self.alloutputdevices[device]:
                self.midi_out = pygame.midi.Output(self.all_devices.index(out_device))
               
    def send_midi_on_out(self,index):
        self.midi_out.note_on(64+index, 64, 0)
    
    def send_midi_off_out(self,index):
        self.midi_out.note_off(64+index, 0, 0)
     
    def items_selected(self,event):
        pygame.midi.quit()
        pygame.midi.init()
        """ handle item selected event
        """
        selected_indices = event.indexes()[0].row()
        print(selected_indices)
        #self.my_input = pygame.midi.Input(selected_indices)
        
        #pygame.midi.Input.close(self.my_input)
        #.selectionModel().currentIndex().row()
        for device in self.all_devices:
            if device == self.allinputdevices[selected_indices]:
                self.my_input = pygame.midi.Input(self.all_devices.index(device))
                self.readInput(self.my_input)
        """
        if self.currentmididevice != selected_indices:
            self.currentmididevice = selected_indices
        if pygame.midi.get_device_info(selected_indices)[2] == 1:
            msg = f'You selected: {selected_indices}'
            # print(msg)
            # pygame.midi.Input.close(my_input)
            if pygame.midi.get_init():
                try:
                    self.my_input.close()

                except(NameError):
                    pass
            #self.my_input = pygame.midi.Input(selected_indices)

            for n in range(pygame.midi.get_count()):
                print(self.allinputdevices)
                if len(self.allinputdevices) > 0:
                    if pygame.midi.get_device_info(n) == self.allinputdevices[0]:
                        self.my_input = pygame.midi.Input(n)
                        self.readInput(self.my_input)
                        break
        """            
    def defaulttofirst(event):
        pygame.midi.quit()
        pygame.midi.init()
        listoutdevices()
        getsecondtinput()
        # print(pygame.midi.get_init())
