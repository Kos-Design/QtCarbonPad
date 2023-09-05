import json
from pathlib import Path
import pygame.midi
import pygame
import math
import rtmidi2

class SamplePlayer():

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        self.dir = Path(__file__).parent
        self.allinputdevices = []
        self.my_input = None
        self.audiosamplesfolder = f"{self.dir.joinpath('soundkit')}"
        self.lesplayers = []
        self.lasoundbank = []
        self.currentmididevice = 0
        self.listbox = None
        try:
            self.lesfilnames = [str(x.name) for x in Path(self.audiosamplesfolder).glob("*.*")]
            self.lesfilnames.sort()
            
            self.load_soundbank()
        except FileNotFoundError:
            self.lesfilnames = list(range(16))
            print("Soundbank not found")

        self.init_pygame()
        self.listoutdevices()
        self.getsecondtinput()

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
        self.allinputdevices = []
        for n in range(pygame.midi.get_count()):
            if pygame.midi.get_device_info(n)[2] == 1:
                self.allinputdevices.append(pygame.midi.get_device_info(n))

    def print_devices(self):
        for n in range(pygame.midi.get_count()):
            print(n, pygame.midi.get_device_info(n))

    def number_to_note(number):
        notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
        return notes[number % 12]

    def readInput(self,input_device):
        # print("pooling")
        clock = pygame.time.Clock()
        # while True:
        if input_device.poll():
            event = input_device.read(1)[0]

            data = event[0]

            lemessagemidi, channel = rtmidi2.splitchannel(data[0])
            # print(lemessagemidi)
            timestamp = event[1]
            note_number = data[1]
            velocity = data[2]
            if lemessagemidi == 144:

                if velocity > 0:
                    nodulo = (note_number + 4) % 16
                    for i in range(0, 16):
                        if nodulo == i:
                            pushbi(i)

                    print(number_to_note(note_number), velocity)
                if velocity == 0:
                    nodulo = (note_number + 4) % 16

                    for i in range(0, 16):
                        if nodulo == i:
                            pullbi(i)

        root.after(10, doreadm)

    def getsecondtinput(self):
        self.listoutdevices()
        for n in range(pygame.midi.get_count()):
            if len(self.allinputdevices) > 0:
                if pygame.midi.get_device_info(n) == self.allinputdevices[0]:
                    self.my_input = pygame.midi.Input(n)

    def browseFilesi(self,i):
        self.lesfilnames[i] = filedialog.askopenfilename(initialdir=audiosamplesfolder,
                                                    title="Select a File",
                                                    filetypes=(("Wav files",
                                                                "*.wav"),
                                                               ("all files",
                                                                "*.*")))
        self.lesplayers[i] = pygame.mixer.Sound(self.lesfilnames[i])
     
    def playlesoundi(self, i):
        self.lesplayers[i].stop()
        self.lesplayers[i].play()

    def pushbi(self,i):
        global lescanvasb
        global bimgids
        lescanvasb[i].itemconfigure(bimgids[i], state="hidden")
        playlesoundi(i)

    def pullbi(self,i):
        global lescanvasb
        global bimgids
        lescanvasb[i].itemconfigure(bimgids[i], state="normal")

    def loadbank(self):
        for i in range(0, 16):
            self.lesplayers[i] = pygame.mixer.Sound(self.lesfilnames[i])

    def doreadm():
        global my_input
        try:
            readInput(my_input)
        except(NameError):
            pass

    def save():
        savebank()

    def load():
        loadbank()

    def items_selected(event):
        pygame.midi.quit()
        pygame.midi.init()
        global currentmididevice

        global my_input
        global allinputdevices
        listoutdevices()
        """ handle item selected event
        """
        # get selected indices
        selected_indices = listbox.curselection()
        # get selected items
        # selected_langs = ",".join([listbox.get(i) for i in selected_indices])
        if currentmididevice != selected_indices[0]:
            #print(selected_indices[0])
            currentmididevice = selected_indices[0]
        if pygame.midi.get_device_info(selected_indices[0])[2] == 1:
            msg = f'You selected: {selected_indices[0]}'
            # print(msg)
            # pygame.midi.Input.close(my_input)
            if pygame.midi.get_init():
                try:
                    my_input.close()

                except(NameError):
                    pass
            # my_input = pygame.midi.Input(selected_indices[0])

            for n in range(pygame.midi.get_count()):
                if len(allinputdevices) > 0:
                    if pygame.midi.get_device_info(n) == allinputdevices[0]:
                        my_input = pygame.midi.Input(n)

    def defaulttofirst(event):
        pygame.midi.quit()
        pygame.midi.init()
        listoutdevices()
        getsecondtinput()
        # print(pygame.midi.get_init())

'''
        root = tk.Tk()
        root.geometry("866x688")
    
        root.minsize(866, 715)
        root.maxsize(866, 715)
    
        limage = tk.PhotoImage(file="buttons/BGOff.png")
    
        imgwidth = 866
        imgheight = 688
        canvas = tk.Canvas(root, width=imgwidth, height=imgheight, bd=0, highlightthickness=0)
        canvas.create_image(0, 0, image=limage, anchor="nw")
        laframe = tk.Frame(root)
    
        canvas.pack()
        global lesbuttons
        global lesbuttonsOff
        global lesbuttonsOn
        global lesbimages
        global lesbimagesOff
        global lescanvasb
        global bimgidOffs
        global bimgids
        lesbuttonsOn = os.listdir("buttons/bOns")
        lesbuttonsOn.sort()
        lesbuttonsOff = os.listdir("buttons/bOffs")
        lesbuttonsOff.sort()
        lesbuttons = []
        lesbimages = []
        lesbimagesOff = []
        lescanvasb = []
        bimgidOffs = []
        bimgids = []
        for i in range(0, 16):
            lesbuttons.append(tk.Frame(root, width=172, height=172))
            lesbuttonsOn[i] = "buttons/bOns/" + lesbuttonsOn[i]
            lesbuttonsOff[i] = "buttons/bOffs/" + lesbuttonsOff[i]
            lesbimages.append(tk.PhotoImage(file=lesbuttonsOn[i]))
            lesbimagesOff.append(tk.PhotoImage(file=lesbuttonsOff[i]))
            lescanvasb.append(tk.Canvas(root, width=172, height=172, bd=0, highlightthickness=0, ))
            bimgidOffs.append(lescanvasb[i].create_image(0, 0, image=lesbimagesOff[i], anchor="nw"))
            bimgids.append(lescanvasb[i].create_image(0, 0, image=lesbimages[i], anchor='nw'))
            lescanvasb[i].bind("<Button-1>", eval(f"left_click{i}"))
            lescanvasb[i].bind("<ButtonRelease-1>", eval(f"Release_left_click{i}"))
            lescanvasb[i].bind("<ButtonRelease-2>", eval(f"right_click{i}"))
            lescanvasb[i].bind("<ButtonRelease-3>", eval(f"right_click{i}"))

        root.bind("<KeyPress-eacute>", eval(f"left_click{0}"))
        root.bind("<KeyRelease-eacute>", eval(f"Release_left_click{0}"))
        root.bind("<KeyPress-quotedbl>", eval(f"left_click{0}"))
        root.bind("<KeyRelease-quotedbl>", eval(f"Release_left_click{0}"))
        root.bind("<KeyPress-ampersand>", eval(f"left_click{0}"))
        root.bind("<KeyRelease-ampersand>", eval(f"Release_left_click{0}"))
    
        # root.bind("<KeyPress-apostrophe>", eval(f"left_click{1}"))
        # root.bind("<KeyRelease-apostrophe>",eval(f"Release_left_click{1}"))
        root.bind("<KeyPress-parenleft>", eval(f"left_click{1}"))
        root.bind("<KeyRelease-parenleft>", eval(f"Release_left_click{1}"))
        root.bind("<KeyPress-minus>", eval(f"left_click{1}"))
        root.bind("<KeyRelease-minus>", eval(f"Release_left_click{1}"))
    
        root.bind("<KeyPress-egrave>", eval(f"left_click{2}"))
        root.bind("<KeyRelease-egrave>", eval(f"Release_left_click{2}"))
        root.bind("<KeyPress-underscore>", eval(f"left_click{2}"))
        root.bind("<KeyRelease-underscore>", eval(f"Release_left_click{2}"))
        root.bind("<KeyPress-ccedilla>", eval(f"left_click{2}"))
        root.bind("<KeyRelease-ccedilla>", eval(f"Release_left_click{2}"))
    
        root.bind("<KeyPress-agrave>", eval(f"left_click{3}"))
        root.bind("<KeyRelease-agrave>", eval(f"Release_left_click{3}"))
        root.bind("<KeyPress-parenright>", eval(f"left_click{3}"))
        root.bind("<KeyRelease-parenright>", eval(f"Release_left_click{3}"))
        root.bind("<KeyPress-equal>", eval(f"left_click{3}"))
        root.bind("<KeyRelease-equal>", eval(f"Release_left_click{3}"))
    
        root.bind("<KeyPress-a>", eval(f"left_click{4}"))
        root.bind("<KeyRelease-a>", eval(f"Release_left_click{4}"))
        root.bind("<KeyPress-z>", eval(f"left_click{4}"))
        root.bind("<KeyRelease-z>", eval(f"Release_left_click{4}"))
        root.bind("<KeyPress-e>", eval(f"left_click{4}"))
        root.bind("<KeyRelease-e>", eval(f"Release_left_click{4}"))
    
        root.bind("<KeyPress-r>", eval(f"left_click{5}"))
        root.bind("<KeyRelease-r>", eval(f"Release_left_click{5}"))
        root.bind("<KeyPress-t>", eval(f"left_click{5}"))
        root.bind("<KeyRelease-t>", eval(f"Release_left_click{5}"))
        root.bind("<KeyPress-y>", eval(f"left_click{5}"))
        root.bind("<KeyRelease-y>", eval(f"Release_left_click{5}"))
    
        root.bind("<KeyPress-u>", eval(f"left_click{6}"))
        root.bind("<KeyRelease-u>", eval(f"Release_left_click{6}"))
        root.bind("<KeyPress-i>", eval(f"left_click{6}"))
        root.bind("<KeyRelease-i>", eval(f"Release_left_click{6}"))
        root.bind("<KeyPress-o>", eval(f"left_click{6}"))
        root.bind("<KeyRelease-o>", eval(f"Release_left_click{6}"))
    
        root.bind("<KeyPress-p>", eval(f"left_click{7}"))
        root.bind("<KeyRelease-p>", eval(f"Release_left_click{7}"))
        root.bind("<KeyPress-Multi_key>", eval(f"left_click{7}"))
        root.bind("<KeyRelease-Multi_key>", eval(f"Release_left_click{7}"))
        root.bind("<KeyPress-dollar>", eval(f"left_click{7}"))
        root.bind("<KeyRelease-dollar>", eval(f"Release_left_click{7}"))
    
        root.bind("<KeyPress-q>", eval(f"left_click{8}"))
        root.bind("<KeyRelease-q>", eval(f"Release_left_click{8}"))
        root.bind("<KeyPress-s>", eval(f"left_click{8}"))
        root.bind("<KeyRelease-s>", eval(f"Release_left_click{8}"))
        root.bind("<KeyPress-d>", eval(f"left_click{8}"))
        root.bind("<KeyRelease-d>", eval(f"Release_left_click{8}"))
    
        root.bind("<KeyPress-f>", eval(f"left_click{9}"))
        root.bind("<KeyRelease-f>", eval(f"Release_left_click{9}"))
        root.bind("<KeyPress-g>", eval(f"left_click{9}"))
        root.bind("<KeyRelease-g>", eval(f"Release_left_click{9}"))
        root.bind("<KeyPress-h>", eval(f"left_click{9}"))
        root.bind("<KeyRelease-h>", eval(f"Release_left_click{9}"))
    
        root.bind("<KeyPress-j>", eval(f"left_click{10}"))
        root.bind("<KeyRelease-j>", eval(f"Release_left_click{10}"))
        root.bind("<KeyPress-k>", eval(f"left_click{10}"))
        root.bind("<KeyRelease-k>", eval(f"Release_left_click{10}"))
        root.bind("<KeyPress-l>", eval(f"left_click{10}"))
        root.bind("<KeyRelease-l>", eval(f"Release_left_click{10}"))
    
        root.bind("<KeyPress-m>", eval(f"left_click{11}"))
        root.bind("<KeyRelease-m>", eval(f"Release_left_click{11}"))
        root.bind("<KeyPress-ugrave>", eval(f"left_click{11}"))
        root.bind("<KeyRelease-ugrave>", eval(f"Release_left_click{11}"))
        root.bind("<KeyPress-asterisk>", eval(f"left_click{11}"))
        root.bind("<KeyRelease-asterisk>", eval(f"Release_left_click{11}"))
    
        root.bind("<KeyPress-w>", eval(f"left_click{12}"))
        root.bind("<KeyRelease-w>", eval(f"Release_left_click{12}"))
        root.bind("<KeyPress-x>", eval(f"left_click{12}"))
        root.bind("<KeyRelease-x>", eval(f"Release_left_click{12}"))
        root.bind("<KeyPress-c>", eval(f"left_click{12}"))
        root.bind("<KeyRelease-c>", eval(f"Release_left_click{12}"))
    
        root.bind("<KeyPress-v>", eval(f"left_click{13}"))
        root.bind("<KeyRelease-v>", eval(f"Release_left_click{13}"))
        root.bind("<KeyPress-b>", eval(f"left_click{13}"))
        root.bind("<KeyRelease-b>", eval(f"Release_left_click{13}"))
        root.bind("<KeyPress-n>", eval(f"left_click{13}"))
        root.bind("<KeyRelease-n>", eval(f"Release_left_click{13}"))
    
        root.bind("<KeyPress-comma>", eval(f"left_click{14}"))
        root.bind("<KeyRelease-comma>", eval(f"Release_left_click{14}"))
        root.bind("<KeyPress-semicolon>", eval(f"left_click{14}"))
        root.bind("<KeyRelease-semicolon>", eval(f"Release_left_click{14}"))
    
        root.bind("<KeyPress-colon>", eval(f"left_click{15}"))
        root.bind("<KeyRelease-colon>", eval(f"Release_left_click{15}"))
        root.bind("<KeyPress-exclam>", eval(f"left_click{15}"))
        root.bind("<KeyRelease-exclam>", eval(f"Release_left_click{15}"))
    
        for i in range(0, 16):
            lescanvasb[i].place(x=89 + (172 * (i % 4)), y=172 * math.trunc(i / 4), anchor="nw")
    
'''