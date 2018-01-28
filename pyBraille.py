from tkinter import *
from tkinter import ttk
import serialCom as sc
import threading
from PIL import ImageTk, Image
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, time, json
from handwrittingAPI import *

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

        self.label = Label(master, text="Disconnected")
        self.label.grid(row=0,column=0, sticky=E+W,ipadx=60)
        
        self.port_box = Text(root, height = 1, width = 10)
        self.port_box.grid(row=1,column=0, sticky=E+W)
        self.port_box.insert(END, "COM5")

        self.connect_button = ttk.Button(master, text="Connect", command=self.connect, style = 'NuclearReactor.TButton')
        self.connect_button.grid(row=2,column=0, sticky=E+W)
        
        self.send_button = ttk.Button(master, text="Send", state=DISABLED, command=self.send, style = 'NuclearReactor.TButton')
        self.send_button.grid(row=3,column=0, sticky=E+W)

        self.close_button = ttk.Button(master, text="Close", command=self.quitProg, style = 'NuclearReactor.TButton')
        self.close_button.grid(row=7,column=0, columnspan = 2, sticky=E+W, rowspan=3)

        self.labelDescription = Label(master, text = "Open a file to read to text")
        self.labelDescription.grid(row=0,column=1,ipadx = 40, sticky=E+W)

        self.entryBox = Entry(master, textvariable = entryVar)
        self.entryBox.grid(row=1,column=1,sticky=E+W)


        self.buttonOpen = ttk.Button(master, text = "Open", command=lambda: transcribeFile(os.path.basename(self.entryBox.get())),style = 'NuclearReactor.TButton')
        self.buttonOpen.grid(row=2,column=1,sticky=E+W)

        self.buttonFile = ttk.Button(master, text = "...", command = self.openDir, style = 'NuclearReactor.TButton')
        self.buttonFile.grid(row=3,column=1,sticky=E+W)

    def connect(self):
        print("Greetings!")
        arduino = self.port_box.get("1.0", END).rstrip("\n\r")
        if sc.connect(arduino):
            self.label['text'] = 'Connected to ' + arduino
            self.send_button['state'] = 'normal'
        else:
            self.label['text'] = 'Connection Failed'

    def send(self):
        sc.sendBraille()
        
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
