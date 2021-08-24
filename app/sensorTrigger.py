import requests
import os
import json
import cameraSnap as cSnap
import time
import app_startchecks as appsc



def webhook_rx(webhook_body):  # Receive json body from webhook
    
    mt20serial = webhook_body["deviceSerial"]
    
    ## Need to update data source for mv serial
    mv_serial = appsc.GetMerakiMVDevices()[0]

    retries = 5
    success = False
    while success == False:
        try:
            imgURL = cSnap.get_snapshot_by_mt_door_event(mt20serial, mv_serial, 3, 5)
            if imgURL is None:
                raise Exception('*sT* -- URL missing')                               
            else:
                print (f"imgURL = {imgURL}")
                print ("Image successfully captured and downloaded")
                return 200
                success = True                
        except Exception as e:
            retries -= 1
            print(f"Error: {e}")
            time.sleep(20)
            print(f"Retry attempt remaining: {retries}")
            if retries <= 0:
                print("Error: max attempts reached")
                return 404
                success = True


if __name__ == "__main__":
   webhook_rx(webhook_body)
   print ("**End of Script**")




