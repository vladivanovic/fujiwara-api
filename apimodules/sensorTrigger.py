import requests



apiURL = str("https://api.meraki.com/api/v1/networks/" + netID + "/environmental/events")

headers = {
     "Content-Type": "application/json",
     "Accept": "application/json",
     "X-Cisco-Meraki-API-Key": meraki_api_key
}
params = {
    "includedEventTypes[]" : "mt_door",
    "perPage" : num_entries,
    "gatewaySerial" : mt_door_serial
}
    
r_envevents = requests.request('GET', apiURL, headers=headers, params=params)

r_envevents_json = r_envevents.json()

for item in r_envevents_json:
        if item["eventData"]["value"] == "1.0":
            print("Getting Snapshot")
            time_plus_delta = parser.parse(item["occurredAt"]) + datetime.timedelta(0,delta_seconds) #delay in seconds
            new_ts_iso = datetime.datetime.isoformat(time_plus_delta)
            new_ts_unix = time_plus_delta.timestamp()

            snapshot_url = get_snapshot_url_mv_camera(mv_snapshot_camera, new_ts_iso)

            time.sleep(5) #wait at least 5 seconds before trying to download the image
            os.makedirs(os.path.dirname(f"images/{mv_snapshot_camera}/"), exist_ok=True) #create folders if not exists

            retries = 0
            success = False
            while success == False:
                try:
                    r_img = requests.get(snapshot_url)
                    if r_img.status_code == 200:
                        with open(f"images/{mv_snapshot_camera}/{new_ts_unix}.jpeg", 'wb') as f:
                            f.write(r_img.content)
                        success = True
                except Exception as e:
                    retries += 1
                    print(f"Error when downloading images: {e}")
                    print(f"Retry: {retries}")
                    time.sleep(30)
                    if retries > 5:
                        print("Error: Avoid endless loop")
                        success = True