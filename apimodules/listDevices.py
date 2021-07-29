# warm-up script
# list Meraki devices module
# references credentials.json

from pprintpp import pprint as pp
import requests
import os
import json

## declaration and initialization

dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(dir, "credentials.json")) as temp:
    creds = temp.read()

jsonCreds = json.loads(creds)

keyToken = str(jsonCreds["keyToken"])

url  = str("https://api.meraki.com/api/v1/networks/" + jsonCreds["strNetID"] + "/devices")

payload={}

headers = {
  'X-Cisco-Meraki-API-Key': keyToken
}

## retrieve device list

response = requests.request("GET", url, headers=headers, data=payload)

jsonResp = json.loads(response.text)
pp(jsonResp)