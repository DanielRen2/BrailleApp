import tkinter as tk 
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import os
import glob
import brailleConverter as bC

import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, time, json

requestHeaders = {
    # Request headers.
    'Content-Type': 'application/octet-stream',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': 'a5ab297d53164f3c9f5d94f86bd4fc4e',
}
params = {'handwriting' : 'true'}

uri_base = 'https://westcentralus.api.cognitive.microsoft.com'

# Takes a file and converts it to text and save the braille mapping to txt file
def readImage(fileName):
    # Replace the three dots below with the full file path to a JPEG image of a celebrity on your computer or network.

    try:
        textPath = os.path.join('./Transcribe/', os.path.basename(fileName)[:-5] + ".txt")
        

        if (not os.path.exists(textPath)):

            with open(fileName, 'rb') as f:
                body = f.read()

            # This operation requrires two REST API calls. One to submit the image for processing,
            # the other to retrieve the text found in the image. 
            #
            # This executes the first REST API call and gets the response.
            response = requests.request('POST', uri_base + '/vision/v1.0/RecognizeText', json=None, data=body, headers=requestHeaders, params=params)

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
            time.sleep(1)

            # Execute the second REST API call and get the response.
            response = requests.request('GET', operationLocation, json=None, data=body, headers=requestHeaders, params=None)

            # 'data' contains the JSON data. The following formats the JSON data for display.
            parsed = json.loads(response.text)
            print ("Response:")

            imageText = ""
            for x in parsed['recognitionResult']['lines']:
                imageText += x['text'] + " "
                
            print(imageText)
            file = open(textPath , "w")
            file.write(str(bC.convertStringToCor(imageText)))
            file.close



    except Exception as e:
        print('Error:')
        print(e)

# Reads all JPEG in file directory
def transcribeFile(pathURL):
    data_list = {}
    for filename in glob.glob(os.path.join(pathURL, '*.jpeg')):
        readImage(filename)
