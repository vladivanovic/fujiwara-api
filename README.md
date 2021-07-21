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
2. Check if Automated Webhook + nGrok setup works fine (check if we can automate which webhook for Meraki to talk too via API)
3. Test APIs for WAN links, Device Status
4. Find Python SNMP Module, install it and add to automated installer
5. Build out ability for Python SNMP Module, pulling data and temp storing in SQLite3 DB
6. Get Beta MT sensor API, test with MV sensor Snapshot API

# random idea list

Something to be added here one day
