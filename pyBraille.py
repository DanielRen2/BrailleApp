from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import serialCom as sc
import threading
from PIL import ImageTk, Image
import os, sys
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, time, json
from handwrittingAPI import *
from documentReaderAPI import *
import reader as rd

class pyBraille:

    # === Variables
    threads = []

    def __init__(self, master):
        self.master = master
        master.title("pyBraille")
        self.connected = False
        self.defaultPath = os.path.dirname(os.path.realpath(__file__))+"/Images/"

        # === Zero Column
        self.border_top = Label(master, text="")
        self.border_top.grid(row=0, column=0, columnspan = 4)
        
        self.border_bottom = Label(master, text="")
        self.border_bottom.grid(row=11, column=0, columnspan = 4, pady=10)
        
        self.photo = PhotoImage(file=os.path.dirname(os.path.realpath(__file__))+"/pyBrailleSmall.gif")
        self.ppanel = Label(master, image = self.photo)
        self.ppanel.grid(row=0, column=0, rowspan = 10)
        
        # === First Column
        self.label = Label(master, text="Disconnected")
        self.label.grid(row=1,column=1, sticky=E+W,columnspan = 2)
        
        self.label_port= Label(master, text = "Port:")
        self.label_port.grid(row=2,column=1, sticky=W)
        
        self.connect_button = ttk.Button(master, text="Connect", command=self.connect, style = 'NuclearReactor.TButton')
        self.connect_button.grid(row=3,column=1, sticky=E+W,columnspan = 2)
        
        self.labelDescription = Label(master, text = "Transcribe a Folder's Content's")
        self.labelDescription.grid(row=4,column=1,sticky=E+W,columnspan = 2)

        self.label_file= Label(master, text = "Directory:")
        self.label_file.grid(row=5,column=1, sticky=W)
        
        self.buttonOpen = ttk.Button(master, text = "Transcribe", command=self.transcribe,style = 'NuclearReactor.TButton')
        self.buttonOpen.grid(row=6,column=1,sticky=E+W,columnspan = 2)

        self.buttonFile = ttk.Button(master, text = "Choose Directory", command = self.openDir, style = 'NuclearReactor.TButton')
        self.buttonFile.grid(row=7,column=1,sticky=E+W,columnspan = 2)
        
        self.button_delete = ttk.Button(master, text = "Delete all Transcriptions", command = self.transcribeDelete, style = 'NuclearReactor.TButton')
        self.button_delete.grid(row=8,column=1,sticky=E+W,columnspan = 2)
        
        self.close_button = ttk.Button(master, text="Close", command=self.quitProg, style = 'NuclearReactor.TButton')
        self.close_button.grid(row=10,column=1, columnspan = 2, sticky=E+W)
        
        # === Second Column
        self.port_box = Text(root, height = 1, width = 10)
        self.port_box.grid(row=2,column=2, sticky=E+W, ipadx=100)
        self.port_box.insert(END, "COM1")
        
        self.entryBox = Entry(master, textvariable = entryVar)
        self.entryBox.grid(row=5,column=2,sticky=E+W)
        self.entryBox.insert(END, self.defaultPath)

        # === Third Column
        self.list_label = Label(master, text="Transcribable Files")
        self.list_label.grid(row=1,column=3,sticky=E+W, columnspan=2)
        
        self.button_refresh = ttk.Button(master, text = "Refresh Files", command = self.refresh, style = 'NuclearReactor.TButton')
        self.button_refresh.grid(row=2,column=3,sticky=N+S,columnspan=2)
        
        self.list_box = Listbox(master, selectmode=SINGLE)
        self.list_box.grid(row=3,column=3,sticky=N+S+E+W,rowspan=6,padx=20,columnspan=2)
        
        self.hand = Radiobutton(master, text = "Handwriting", variable = t, value=1)
        self.hand.grid(row=9,column=3)
        self.hand.select()
        self.typed = Radiobutton(master, text = "Typed", variable = t, value=2)
        self.typed.grid(row=9,column=4)
        
        self.send_button = ttk.Button(master, text="Send", state=DISABLED, command=self.send, style = 'NuclearReactor.TButton')
        self.send_button.grid(row=10,column=3, sticky=N+S, columnspan=2)

    # === Actions
    
    def refresh(self):
        self.list_box.delete(0,self.list_box.size())
        files = rd.getFiles()
        for id, f in enumerate(files):
            self.list_box.insert(id, f)
        
    def connect(self):
        print("Greetings!")
        arduino = self.port_box.get("1.0", END).rstrip("\n\r")
        if sc.connect(arduino):
            self.label['text'] = 'Connected to ' + arduino
            self.connected = True
            self.connect_button['state'] = DISABLED
            self.checkSend()
        else:
            self.label['text'] = 'Connection Failed'

    def checkSend(self):
        if self.connected:
            self.send_button['state'] = 'normal'
        else:
            self.send_button['state'] = DISABLED

    def transcribe(self):
        if messagebox.askokcancel("Transcribe", "This will transcribe all files in:\n " + self.defaultPath + "\nPlease make sure all files are JPG format before continuing.\nThis may take a long time.", icon='warning'):
            
            if t.get() == 1:
                transcribeFile(os.path.basename(self.entryBox.get()))
            elif t.get() == 2:
                transcribeFileDocument(os.path.basename(self.entryBox.get()))
            else:
                print("This is T: " + str(self.t))
            self.refresh()
            
    def transcribeDelete(self):
        if messagebox.askokcancel("Transcribe", "This will remove ALL files in:\n " + os.path.dirname(os.path.realpath(__file__))+"/Transcribe/" + "\nPlease make sure you want to delete all files before continuing.", icon='warning'):
            rd.removeTrans()
            self.refresh()
            
    def send(self):
        if len(self.list_box.curselection()):
            print(self.list_box.get(self.list_box.curselection()))
            sc.sendBraille(rd.getWords(self.list_box.get(self.list_box.curselection())))
        else:
            self.label['Select a file first']
        
    def quitProg(self):
        sys.exit(0)

    def openDir(self):
        name = filedialog.askdirectory()
        print("Directory Name")
        entryVar.set(name)
        print(name)
        
root = Tk()
#root.geometry('{}x{}'.format(500, 200))

entryVar = StringVar()
t = IntVar()
my_gui = pyBraille(root)
root.iconbitmap("@" + os.path.dirname(os.path.realpath(__file__))+'/pyBraille.xbm')
root.mainloop()
