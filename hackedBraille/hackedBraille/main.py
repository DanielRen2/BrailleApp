import tkinter as tk 
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, time, json

requestHeaders = {
    # Request headers.
    'Content-Type': 'application/octet-stream',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': 'a5ab297d53164f3c9f5d94f86bd4fc4e',
}
pathToFile = 'IMG_1992.jpg'
with open(pathToFile, 'rb') as f:
	body = f.read()
params = {'handwriting' : 'true'}

uri_base = 'https://westcentralus.api.cognitive.microsoft.com'

def readImage(name):
	print("Reading Body")
	# Replace the three dots below with the full file path to a JPEG image of a celebrity on your computer or network.
	with open(name,'rb') as f:
		body = f.read()
	try:
	    # This operation requrires two REST API calls. One to submit the image for processing,
	    # the other to retrieve the text found in the image. 
	    #
	    # This executes the first REST API call and gets the response.

	    response = requests.request('POST', uri_base + '/vision/v1.0/RecognizeText', json=None, data=body, headers=requestHeaders, params=params)
	    print(response.status_code)
	    # Success is indicated by a status of 202.
	    if response.status_code != 202:
	        # if the first REST API call was not successful, display JSON data and exit.
	        parsed = json.loads(response.text)
	        print ("Error:")
	        print (json.dumps(parsed, sort_keys=True, indent=2))
	        exit()

	    # The 'Operation-Location' in the response contains the URI to retrieve the recognized text.
	    operationLocation = response.headers['Operation-Location']

	    # Note: The response may not be immediately available. Handwriting recognition is an
	    # async operation that can take a variable amount of time depending on the length
	    # of the text you want to recognize. You may need to wait or retry this GET operation.

	    print('\nHandwritten text submitted. Waiting 10 seconds to retrieve the recognized text.\n')
	    time.sleep(10)

	    # Execute the second REST API call and get the response.
	    response = requests.request('GET', operationLocation, json=None, data=body, headers=requestHeaders, params=None)

	    # 'data' contains the JSON data. The following formats the JSON data for display.
	    parsed = json.loads(response.text)
	    print ("Response:")

	    for x in parsed['recognitionResult']['lines']:
	    	print(x['text'])
	except Exception as e:
	    print('Error:')
	    print(e)
#--------------------------------   
"""
def callback():
    name= askopenfilename() 
    print(name)
    
errmsg = 'Error!'
Button(text='File Open', command=callback).pack(fill=X)
mainloop() """

# where the request can be sent
def printFunction():
	print("Button has been clicked")
	print(entryBox.get())

def callback(self):
    filename = tkFileDialog.askdirectory()
    self.name.set(filename)

def askDirect():
	name = tkfiledialog.askdirectory()
	if name:
		var.set(name)

def openDir():
	name = filedialog.askopenfilename()
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


buttonOpen = Button(bottomFrame, text = "Open", fg = "red", command=lambda: readImage(os.path.basename(entryBox.get())))
buttonOpen.pack()

buttonFile = Button(topFrame, text = "...", command = openDir)
buttonFile.pack(side = RIGHT)

root.mainloop()
