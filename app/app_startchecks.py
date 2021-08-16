#!/usr/bin/env python3

# ------------------
# IMPORTS
# ------------------

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from pyngrok import ngrok, conf
import yaml
import requests
import subprocess
import meraki
import re


# ------------------
# DB FUNCTIONS
# ------------------

# Establish Database Connection Function
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='merakihuddb',
        user='merakihud',
        password='merakihudpassword'
    )
    return conn


# Establish First Time Setup DB Setup Function
def firstTimeDbSetup():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = %s)', ('globalparams',))
    table_exists = cur.fetchone()[0]
    if table_exists is False: # Check if DB is empty or not
        with open('schema.sql', 'r') as schema:
            cur.execute(schema.read())
            cur.close()
            conn.commit()
    else: # Do initial DB File and Table setup
        return "Tables exist"


# ------------------
# APP STARTUP CHECK FUNCTIONS
# ------------------

# Establish Meraki API Key
def GetMerakiAPIKey():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
           'SELECT param FROM globalparams WHERE name= %s LIMIT 1', ["MerakiAPIKey"])
    keyexists = cur.fetchone()
    cur.close()
    if keyexists is not None:
        MERAKI_API_KEY = keyexists['param']
        return MERAKI_API_KEY
    else:
        return None


# Establish Meraki Org ID
def GetMerakiOrgID():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
            'SELECT param FROM globalparams WHERE name= %s AND active= %s LIMIT 1', ["MerakiOrgID", "1"])
    orgidexists = cur.fetchone()
    cur.close()
    if orgidexists is not None:
        OrgID = orgidexists['param']
        return OrgID
    else:
        return None


# Establish Network ID
def GetMerakiNetworkID():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
            'SELECT param FROM globalparams WHERE name= %s AND active= %s LIMIT 1', ["MerakiNetworkID", "1"])
    networkidexists = cur.fetchone()
    conn.close()
    if networkidexists is not None:
        NetworkID = networkidexists['param']
        return NetworkID
    else:
        return None


# ------------------
# NGROK TUNNEL FUNCTIONS
# ------------------

# Function to Create YAML and start ngrok instance on initial setup
def ngrok_tunnel(ngrokkey):
    if ngrokkey is not None:
        doc = {'authtoken': ngrokkey, 'tunnels': {'merakihud': {'addr': 5001, 'proto': 'http', 'root_cas': 'trusted', 'bind_tls': 'true'}}}
        with open("ngrok.yml", "w") as f:
            yaml.dump(doc, f)


# Function to start ngrok instance e.g. when restart button on Admin page is hit
def startngroktunnel():
    ngrokFile = os.path.abspath("ngrok.yml")
    ngrokConfig = conf.PyngrokConfig(config_path=ngrokFile)
    http_tunnel = ngrok.connect(name='merakihud', pyngrok_config=ngrokConfig)


# ------------------
# WEBHOOK SERVER FUNCTIONS
# ------------------

# Global Variables for functions in this section
MerakiOrgID = GetMerakiOrgID()
MerakiAPIKey = GetMerakiAPIKey()
MerakiNetworkID = GetMerakiNetworkID()

# Function to start webhook server
def webhook_start():
    startwebhook = subprocess.call('./startWebhook.sh')
    webhook_proccheck()
    print('running webhook start function')


# Function to check webhook server process running
def webhook_proccheck():
    statuswebhook = subprocess.run('tmux ls', shell=True, stdout=subprocess.PIPE)
    print(statuswebhook.stdout)
    return statuswebhook.stdout


# Function to pull webhook status from webhook server
def webhook_status():
    try:
        webhook_status_response = requests.get('http://localhost:5001/')
    except requests.exceptions.RequestException as e:
        json_res = None
        print("Webhook Error")
        return json_res
    json_res = webhook_status_response.json()
    print(json_res)
    return json_res


# Function to setup the webhook server, update Meraki Dashboard automatically
def merakiWebhookSetup(ngrok_tunnel):
    global MerakiAPIKey
    global MerakiNetworkID
    dashboard = meraki.DashboardAPI(MerakiAPIKey)
    getHttpServers = dashboard.networks.getNetworkWebhooksHttpServers(MerakiNetworkID)
    for httpServer in getHttpServers:
        delHttpServer = dashboard.networks.deleteNetworkWebhooksHttpServer(MerakiNetworkID, httpServer['id'])
    httpServerName = 'auto-ngrok'
    ngrok_tunnel = ngrok_tunnel[0]
    urls = []
    for url in ngrok_tunnel.split(" -> "):
        urls.append(
            re.search("(?P<actualurl>https?://[^\s]+)\"", url).group("actualurl")
        )
    final_url = urls[0] + "/listen"
    setHttpServer = dashboard.networks.createNetworkWebhooksHttpServer(MerakiNetworkID, httpServerName, final_url, sharedSecret='auto-ngrok')
    getHttpServers = dashboard.networks.getNetworkWebhooksHttpServers(MerakiNetworkID)
    httpServerID = getHttpServers[0]['id']
    setAlertsHttpServer = dashboard.networks.updateNetworkAlertsSettings(MerakiNetworkID, defaultDestinations={'httpServerIds': [httpServerID]})


# ------------------
# ENGINE.IO FUNCTIONS
# ------------------

def getNetworkDevices():
    global MerakiAPIKey
    global MerakiNetworkID
    dashboard = meraki.DashboardAPI(MerakiAPIKey)
    conn = get_db_connection()
    cur = conn.cursor()
    getdevices = dashboard.networks.getNetworkDevices(MerakiNetworkID)
    for device in getdevices:
        lat = device['lat']
        long = device['lng']
        devicename = device['name']
        serial = device['serial']
        macaddress = device['mac']
        if 'wirelessMac' in device:  # May not exist for all devices
            wirelessMac = device['wirelessMac']
        else:
            wirelessMac = None
        model = device['model']
        if 'lanIp' in device:
            lanIp = device['lanIp']  # May not exist for all devices
        else:
            lanIp = None
        if 'wanIp1' in device:
            wanIp = device['wanIp1']  # May not exist for all devices
        else:
            wanIp = None
        tags = device['tags']
        networkId = device['networkId']
        updatedevice = cur.execute(  # This needs to be fixed from ON CONFLICT DO NOTHING to ON CONFLICT devicename SET every other value
            "INSERT INTO devices (lat, long, devicename, serial, macaddress, wirelessMac, model, lanIp, wanIp, tags, networkId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", [lat, long, devicename, serial, macaddress, wirelessMac, model, lanIp, wanIp, tags, networkId])
    cur.close()
    conn.commit()


