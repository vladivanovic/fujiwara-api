# fujiwara-api

A Meraki HUD (so you don't need to open Dashboard)

This project is built on the latest (July 2021) versions of the following:
- Python3
- Flask
- SQLite3
- Meraki Dashboard APIs
- Bootstrap
- JavaScript

What this project gives you:
1. Automated install of all requirements for this Project (on Ubuntu or CentOS)
2. A HUD to see status of your equipment at a high level in the NOC, including:
	a. WAN Links
	b. Device Status (with name + IP)
	c. Advanced details using SNMP
3. A HUD to see events related to your sensors + cameras, we take snapshots when a sensor triggers

# to-do-list

1. Update automated installer to check for and account if system is CentOS or Ubuntu and adjust
2. Need to fix a few bits of existing app.py code (the section to check for partial first time setup)
3. Check if Automated Webhook + nGrok setup works fine (check if we can automate which webhook for Meraki to talk too via API)
4. Test APIs for WAN links, Device Status
5. Find Python SNMP Module, install it and add to automated installer
6. Build out ability for Python SNMP Module, pulling data and temp storing in SQLite3 DB
7. To support the Sensor API w/ MV camera feature - need to build out a DB to create a mapping between system and camera?? or see if there is device location in the API then we can say any sensor in area X triggers a snapshot on one or multiple cameras in the same area (although differentiating between say what is in a DC and what is outside of a DC is hard so...)
8. Get Beta MT sensor API, test with MV sensor Snapshot API

# random idea list

Something to be added here one day
