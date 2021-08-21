# fujiwara-api

A Meraki HUD (so you don't need to open Dashboard)

This project is built on the latest (August 2021) versions of the following:
- Python3
- Flask
- PostgreSQL
- Meraki Dashboard APIs
- ngrok (sign up for free to get an AuthToken at ngrok.com)
- Pyngrok
- Docker
- Ubuntu (eventually CentOS too)

What this project gives you:
1. Automated install of all requirements for this Project (on Ubuntu or CentOS)
2. A HUD to see status of your equipment at a high level in the NOC, including:
    a. WAN Links
    b. Device Status (with name + IP)
    c. Advanced details using SNMP
3. A HUD to see events related to your sensors + cameras, we take snapshots when a sensor triggers
4. Run it all from Docker (eventually)

## to-do-list

Feature 1 (Vlad)
--- Docker ---
1. Troubleshoot Docker SDK when main app is running in a container itself, there's a trick to be done that I'm troubleshooting through

Tasks:
1. need to add extra buttons in the admin panel to start one service at a time, restart services
2. use docker sdk to show the status of the container itself, not just the flask service on there


Feature 2 (Vlad)
--- Main App ---
1. Find Python SNMP Module, install it and add to automated installer
2. Build out ability for Python SNMP Module, pulling data and temp storing in SQLite3 DB
3. Test APIs for WAN links, Device Status

Feature 3 (Fred)
1. To support the Sensor API w/ MV camera feature - need to build out a DB to create a mapping between system and camera?? or see if there is device location in the API then we can say any sensor in area X triggers a snapshot on one or multiple cameras in the same area (although differentiating between say what is in a DC and what is outside of a DC is hard so...)
2. . Get Beta MT sensor API, test with MV sensor Snapshot API

## random idea list

Something to be added here one day
1. Find out if we can use webhooks to get real time temp/humidity readings and update on the HUD page (instead of SNMP polling)
