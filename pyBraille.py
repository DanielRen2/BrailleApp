from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import serialCom as sc
import threading
from PIL import ImageTk, Image
import os, sys
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, time, json
from handwrittingAPI import *
import reader as rd

requestHeaders = {
    # Request headers.
    'Content-Type': 'application/octet-stream',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': 'a5ab297d53164f3c9f5d94f86bd4fc4e',
}
params = {'handwriting' : 'true'}
uri_base = 'https://westcentralus.api.cognitive.microsoft.com'

class pyBraille:

    # === Variables
    threads = []

    def __init__(self, master):
        self.master = master
        master.title("pyBraille")
        self.connected = False
        self.defaultPath = os.path.dirname(os.path.realpath(__file__))+"/Images/"

        # === First Column
        self.label = Label(master, text="Disconnected")
        self.label.grid(row=0,column=0, sticky=E+W,columnspan = 2)
        
        self.label_port= Label(master, text = "Port:")
        self.label_port.grid(row=1,column=0, sticky=W)
        
        self.connect_button = ttk.Button(master, text="Connect", command=self.connect, style = 'NuclearReactor.TButton')
        self.connect_button.grid(row=2,column=0, sticky=E+W,columnspan = 2)
        
        self.labelDescription = Label(master, text = "Transcribe a Folder's Content's")
        self.labelDescription.grid(row=3,column=0,sticky=E+W,columnspan = 2)

        self.label_file= Label(master, text = "Directory:")
        self.label_file.grid(row=4,column=0, sticky=W)
        
        self.buttonOpen = ttk.Button(master, text = "Transcribe", command=self.transcribe,style = 'NuclearReactor.TButton')
        self.buttonOpen.grid(row=5,column=0,sticky=E+W,columnspan = 2)

        self.buttonFile = ttk.Button(master, text = "Choose Directory", command = self.openDir, style = 'NuclearReactor.TButton')
        self.buttonFile.grid(row=6,column=0,sticky=E+W,columnspan = 2)
        
        self.button_delete = ttk.Button(master, text = "Delete all Transcriptions", command = self.transcribeDelete, style = 'NuclearReactor.TButton')
        self.button_delete.grid(row=7,column=0,sticky=E+W,columnspan = 2)
        
        self.close_button = ttk.Button(master, text="Close", command=self.quitProg, style = 'NuclearReactor.TButton')
        self.close_button.grid(row=8,column=0, columnspan = 2, sticky=E+W, rowspan=3)
        
        # === Second Column
        self.port_box = Text(root, height = 1, width = 10)
        self.port_box.grid(row=1,column=1, sticky=E+W, ipadx=100)
        self.port_box.insert(END, "COM5")
        
        self.entryBox = Entry(master, textvariable = entryVar)
        self.entryBox.grid(row=4,column=1,sticky=E+W)
        self.entryBox.insert(END, self.defaultPath)

        # === Third Column
        self.list_label = Label(master, text="Transcribable Files")
        self.list_label.grid(row=0,column=2,sticky=E+W)
        
        self.button_refresh = ttk.Button(master, text = "Refresh Files", command = self.refresh, style = 'NuclearReactor.TButton')
        self.button_refresh.grid(row=1,column=2,sticky=N+S)
        
        self.list_box = Listbox(master, selectmode=SINGLE)
        self.list_box.grid(row=2,column=2,sticky=N+S+E+W,rowspan=6,padx=20)
        
        self.send_button = ttk.Button(master, text="Send", state=DISABLED, command=self.send, style = 'NuclearReactor.TButton')
        self.send_button.grid(row=8,column=2, sticky=N+S)

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
        if messagebox.askokcancel("Transcribe", "This will transcribe all files in:\n " + self.defaultPath + "\nPlease make sure all files are JPG format before continuing.\nThis will overwrite previous transcripts of the same name", icon='warning'):
            #lambda: transcribeFile(os.path.basename(self.entryBox.get()))
            transcribeFile(os.path.basename(self.entryBox.get()))
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
my_gui = pyBraille(root)
root.mainloop()
