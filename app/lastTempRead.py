import requests
import json
import app_startchecks as appsc

mt10serial = appsc.GetMerakiMTDevices()


url = "https://api.meraki.com/api/v1/networks/L_683984193406908696/sensor/stats/latestBySensor?metric=temperature"


payload={}
headers = {
  'X-Cisco-Meraki-API-Key': '837665f9a0c365cba79382f6bc035676368e602d',
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

jResp = json.loads(response.text)

for read in jResp:
    print(read)
    if read["serial"] == mt10serial:
        degVal = read["value"]
        print (f"From sensor serial: {mt10serial}")
        print (f"Last sensor reading: {degVal:.2f}")
        break