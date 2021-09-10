[![python3](https://img.shields.io/badge/python-3.7+-blue.svg)](https://github.com/vladivanovic/fujiwara-api/)

# fujiwara-api

A Meraki HUD (heads-up display, so you don't need to open Dashboard)

This project is built on the latest (August 2021) versions of the following:
- Python3
- Flask
- PostgreSQL
- Meraki Dashboard APIs
- ngrok (Required: AuthToken from ngrok.com)
- Pyngrok
- PySNMP
- Docker
- Ubuntu (on roadmap: CentOS support)

What this project gives you:
1. Automated install of all requirements for this Project (on Ubuntu or CentOS)
2. A HUD to see status of your equipment at a high level in the NOC, including:
    a. WAN Links
    b. Device Status (with name + IP)
    c. Advanced details using SNMP
3. A HUD to see events related to your sensors + cameras, we take snapshots when a sensor triggers
4. Container based run time (future)

## Install and Setup

1. Clone this Github Repository on to any Ubuntu 20.04 LTS installation
```
    git clone https://github.com/vladivanovic/fujiwara-api.git
```

2. On terminal, run *localrunSetup.sh* (will prompt for sudo) and wait for installation to complete
```
    $./localrunSetup.sh
```

3. Open your browser and navigate to http://localhost:5000/ to complete the initial setup
![First Time Setup](https://user-images.githubusercontent.com/45674865/132804090-1dd735dc-9cdf-4702-89b4-f2fd9b3938f5.png)
![Org ID First Time](https://user-images.githubusercontent.com/45674865/132804132-e0688912-12b7-4125-bec2-c64b772a2a0e.png)



** Caution **
Docker is still under construction in our project as of September 9th and may not 100% work

** Caution 2 **
When running locally, please utilise tmux or screen or then run 'python3 app/webhook.py' and 'python3 app/engineio.py' after you have completed the initial setup in step 4 above

## to-do-list

Feature 1 ()
--- Docker ---
Tasks:
1. Troubleshoot Docker SDK when main app is running in a container itself, there's a trick to be done that I'm troubleshooting through
2. use docker sdk to show the status of the container itself, not just the flask service on there

Feature 2 (pxs)
1. Use webhooks to get real time temp/humidity readings and update on the HUD page (instead of SNMP polling)
2. MV-MT Snapshot to support multiple cameras for different angles
3. Water leak sensor support (future)

## random idea list

Something to be added here one day
1. Integrate alerting to Webex Teams Bot
2. Create ElasticLogstashKibana and pre-create dashboards for syslog, netflow and containerize
3. Convert Main App to use AJAX for dynamic page loading of newest alerts/device status
4. Automate the engagement of engineio.py's /device and /devicepoll to update device list in the DB and SNMP polls to update devicestatus in the DB
5. Per device create a table to collect SNMP Performance statistics (need a smart way to do this)
6. Modularize the code in app_startchecks to allow for easier container build/runs on sub-functions
