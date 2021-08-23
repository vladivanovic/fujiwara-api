import requests
import os
import json
import cameraSnap as cSnap
import time



def webhook_rx(webhook_body): #receive json body from webhook
    #print ("Secret Key: " + webhook_body["sharedSecret"])
    mt20serial = webhook_body["deviceSerial"]
    mv_serial = "Q2FV-WZDD-NLJC"
    #print(mt20serial, " ", mv_serial)

    # imgURL = cSnap.get_snapshot_by_mt_door_event(mt20serial, mv_serial, 3, 5)
    # print ("this is the imgURL:\n", imgURL)
    
    # time.sleep(5) 

    retries = 5
    success = False
    while success == False:
        try:
            imgURL = cSnap.get_snapshot_by_mt_door_event(mt20serial, mv_serial, 3, 5)
            if imgURL is None:
                raise Exception('*sT* -- URL missing')                               
            else:
                # print ("imgURL = ",imgURL)
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




