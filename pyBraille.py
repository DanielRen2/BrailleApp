from tkinter import *
import serialCom as sc
import threading

class pyBraille:

    # === Variables
    threads = []

    def __init__(self, master):
        self.master = master
        master.title("pyBraille")

        self.label = Label(master, text="Disconnected")
        self.label.pack()
        
        self.port_box = Text(root, height = 1, width = 10)
        self.port_box.pack()
        self.port_box.insert(END, "COM5")

        self.greet_button = Button(master, text="Connect", command=self.connect)
        self.greet_button.pack()
        
        self.send_button = Button(master, text="Send", state=DISABLED, command=self.self)
        self.send_button.pack()

        self.close_button = Button(master, text="Close", command=self.quitProg)
        self.close_button.pack()

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
        

            
root = Tk()
my_gui = pyBraille(root)
root.mainloop()