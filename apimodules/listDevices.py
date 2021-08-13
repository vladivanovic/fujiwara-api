# warm-up script
# list Meraki devices module
# references credentials.json

import requests
import os
import json

## declaration and initialization

dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(dir, "login/credentials.json")) as temp:
    creds = temp.read()


jsonCreds = json.loads(creds)

APIKey = str(jsonCreds["APIKey"])

url  = str("https://api.meraki.com/api/v1/networks/" + jsonCreds["netID"] + "/devices")

payload={}

headers = {
  'X-Cisco-Meraki-API-Key': APIKey ,
  'Content-Type' : 'application/json'
}

## retrieve device list and normalize data format

response = requests.request("GET", url, headers=headers, data=payload)
listResponse = json.loads(response.text.replace("null", "\" \""))


# display output
for item in listResponse:
  if 'wan1Ip' in item:
    print (item["model"] + "\t" + item["name"])
    print ("\t\t" + item["serial"] + "\t\tWan1: " + item["wan1Ip"] + "\t\tWan2: " + item["wan2Ip"])
  if 'lanIp' in item:
    print (item["model"] + "\t" + item["name"])
    print ("\t\t" + item["serial"] + "\t\tLAN: " + item["lanIp"])