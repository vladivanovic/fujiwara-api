import requests


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
    
r_envevents = requests.request('GET', f"https://api.meraki.com/api/v1/networks/{network_id}/environmental/events", headers=headers, params=params)

r_envevents_json = r_envevents.json()