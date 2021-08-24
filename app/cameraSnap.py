import requests
import os
import json
import time
import datetime
from dateutil import parser

#Global declaration / prod code must retrieve from SQL DB
dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(dir, "sampleQueryBNEHQ.json")) as temp:
    creds = temp.read()

jCreds = json.loads(creds)

APIKey = str(jCreds["APIKey"])
netID = str(jCreds["networkId"])

## Function: retrieve MV snapshot URL
def get_snapshot_url_mv_camera(mv_serial, timestamp_iso):
    """
    Get snapshot from specific MV camera at specific time (ISO format)
    (Info: Wait >5 seconds to download images after its generation!)
    Return: Download URL
    """
    headers = {
        "Content-Type": "application/json",
        "X-Cisco-Meraki-API-Key": APIKey
    }
    data = {
        "timestamp" : timestamp_iso
    }
    
    try:
        r_snapshoturl = requests.request('POST', f"https://api.meraki.com/api/v1/devices/{mv_serial}/camera/generateSnapshot", headers=headers, data=json.dumps(data))
        r_snapshoturl_json = r_snapshoturl.json()
        
        print(f"Snapped from: {mv_serial}")
        # print (type(r_snapshoturl_json))
        # return (r_snapshoturl_json["url"])
        if "errors" in r_snapshoturl_json:
            raise Exception('*cSnap* -- Snapshot retrieval failed')
        else:
            return (r_snapshoturl_json["url"])
    except Exception as e:
        return print(f"Error: {e}")

## Function: Snapshot request with request parameters

def get_snapshot_by_mt_door_event(mt20serial, mv_serial, num_entries, delta_seconds):

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": APIKey
    }
    params = {
        "includedEventTypes[]" : "mt_door",
        "perPage" : num_entries,
        "gatewaySerial" :  mt20serial
        #gatewaySerial produces ideal output, but need function to match mt20serial
    }
    r_envevents = requests.request('GET', f"https://api.meraki.com/api/v1/networks/{netID}/environmental/events", headers=headers, params=params)
    r_envevents_json = r_envevents.json()

    
    for item in r_envevents_json:
        if item["eventData"]["value"] == "1.0":
            print("Capturing image")
            time_plus_delta = parser.parse(item["occurredAt"]) + datetime.timedelta(0,delta_seconds) #delay in seconds
            
            new_ts_iso = datetime.datetime.isoformat(time_plus_delta)
            new_ts_unix = time_plus_delta.timestamp()

            # print (new_ts_iso)
            # print (new_ts_unix)

            snapshot_url = get_snapshot_url_mv_camera(mv_serial, new_ts_iso)
            
            #create folders if none exists
            os.makedirs(os.path.dirname(f"images/{mv_serial}/"), exist_ok=True) 
            
            #wait at least 5 seconds before trying to download the image
            time.sleep(5) 

            retries = 3
            success = False
            while success == False:
                if snapshot_url is not None:
                    try:
                        r_img = requests.get(snapshot_url)
                        if r_img.status_code == 200:
                           with open(f"images/{mv_serial}/{new_ts_unix}.jpeg", 'wb') as f:
                                f.write(r_img.content)
                           print (f"Snapshot download successful.\nFile:\'{new_ts_unix}.jpeg\' created")
                           success = True
                           return (snapshot_url)
                        else:
                           raise Exception('Image download failed')
                        
                    except Exception as e:
                        retries -= 1
                        print(f"Error: {e}")
                        print(f"Retry attempt remaining: {retries}")
                        time.sleep(5)
                        if retries <= 0:
                            print("Failed. Max attempts reached.")
                            success = True
                else:
                    print ('Error: *cSnap* -- Image not found.')
                    success = True



## execution main
if __name__ == "__main__":
    ## retrieve data from database

    mt20serial = str(jCreds["serial"])
    mv_serial = "xxxx-xxxx-xxxx"
    
    print("Capturing image")
    get_snapshot_by_mt_door_event(mt20serial, mv_serial, 3, 5) #mt20serial, mv_serial, num_entries, delta_seconds
