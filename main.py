import tkinter as tk 
from tkinter import filedialog
from tkinter import *
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

def openDir():
	name = filedialog.askdirectory()
	print("Directory Name")
	entryVar.set(name)
	print(name)

root = Tk()
entryVar = StringVar()
topFrame = Frame(root, width = 500, height = 500)
topFrame.pack()

bottomFrame = Frame(root, width = 1000, height = 1000)
bottomFrame.pack(side=BOTTOM)


labelDescription = Label(topFrame, text = "Open a file to read to text", fg = "blue")
labelDescription.pack(side=TOP)

entryBox = Entry(topFrame, textvariable = entryVar)
entryBox.pack(side=BOTTOM, fill=X)


buttonOpen = Button(bottomFrame, text = "Open", fg = "red", command=lambda: transcribeFile(os.path.basename(entryBox.get())))
buttonOpen.pack()
print("We are here")
buttonFile = Button(topFrame, text = "...", command = openDir)
buttonFile.pack(side = RIGHT)

root.mainloop()
print("Here")
