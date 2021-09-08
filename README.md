# fujiwara-api

A Meraki HUD (so you don't need to open Dashboard)

This project is built on the latest (August 2021) versions of the following:
- Python3
- Flask
- PostgreSQL
- Meraki Dashboard APIs
- ngrok (sign up for free to get an AuthToken at ngrok.com)
- Pyngrok
- PySNMP
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

Feature 1 ()
--- Docker ---
Tasks:
1. Troubleshoot Docker SDK when main app is running in a container itself, there's a trick to be done that I'm troubleshooting through
2use docker sdk to show the status of the container itself, not just the flask service on there

Feature 2 (Fred)
1. Use webhooks to get real time temp/humidity readings and update on the HUD page (instead of SNMP polling)
2. Meraki MV Area takes snapshot required?
3. Water module?

## random idea list

Something to be added here one day
1. Integrate alerting to Webex Teams Bot
2. Create ElasticLogstashKibana and pre-create dashboards for syslog, netflow and containerize
3. Convert Main App to use AJAX for dynamic page loading of newest alerts/device status
4. Automate the engagement of engineio.py's /device and /devicepoll to update device list in the DB and SNMP polls to update devicestatus in the DB
