#login script with prompt?

import requests
import os
import json

## declaration and initialization

dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(dir, "login/credentials.json")) as temp:
    creds = temp.read()


jsonCreds = json.loads(creds)

APIKey = str(jsonCreds["APIKey"])

payload = {}

headers = {
  'X-Cisco-Meraki-API-Key': APIKey
}
