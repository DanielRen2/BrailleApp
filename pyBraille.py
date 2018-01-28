from tkinter import *
import serialCom as sc

class pyBraille:
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

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def connect(self):
        print("Greetings!")
        arduino = self.port_box.get("1.0", END).rstrip("\n\r")
        if sc.connect(arduino):
            self.label['text'] = 'Connected to ' + arduino
        else:
            self.label['text'] = 'Connection Failed'

root = Tk()
my_gui = pyBraille(root)
root.mainloop()