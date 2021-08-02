# references credentials.json
# returns image URL from a camera snap

from pprintpp import pprint
import requests
import os
import json

## declaration and initialization

netID = 
deviceSerial = 
timeStamp = 

# call login function

url  = str("https://api.meraki.com/api/v1/networks/" + netID + "cameras/" + deviceSerial + "/videoLink?timestamp=" + timeStamp)

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)


