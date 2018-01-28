########## Python 3.6 #############
import tkinter as tk 
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import os
import glob
import brailleConverter as bC

import http.client, urllib.request, urllib.parse, urllib.error, base64, json

###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = 'a5ab297d53164f3c9f5d94f86bd4fc4e'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'westcentralus.api.cognitive.microsoft.com'

headers = {
    # Request headers.
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.parse.urlencode({
    # Request parameters. The language setting "unk" means automatically detect the language.
    'language': 'unk',
    'detectOrientation ': 'true',
})
#body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png'}"
# The URL of a JPEG image containing text.
#body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png'}"

def readImageProper(fileName):

    try:
        textPath = os.path.join('./Transcribe/', os.path.splitext(os.path.basename(fileName))[0] + ".txt")
        if (not os.path.exists(textPath)):
            print("Attempting to read " + os.path.basename(fileName))
            with open(fileName, 'rb') as f:
                body = f.read()

            # Execute the REST API call and get the response.
            conn = http.client.HTTPSConnection(uri_base)
            conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()

            # 'data' contains the JSON data. The following formats the JSON data for display.
            parsed = json.loads(data)

            imageText = ""
            for x in parsed['regions'][0]['lines']:
                for y in x['words']:
                    imageText += y['text'] + " "
            file = open(textPath , "w")
            file.write(str(bC.convertStringToCor(imageText)))
            file.close

            conn.close()

    except Exception as e:
        print('Error:')
        print(e)

####################################

# Reads all JPEG in file directory
def transcribeFileDocument(pathURL):

    for filename in glob.glob(os.path.join(pathURL, '*.jpeg')):
        readImageProper(filename)

    for filename in glob.glob(os.path.join(pathURL, '*.jpg')):
        readImageProper(filename)


    print("Finish Revewing the files")
    return
