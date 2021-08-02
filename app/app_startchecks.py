#!/usr/bin/env python3

# All of the Imports
import sqlite3
import os
from pyngrok import ngrok, conf
import yaml

# Establish Database Connection Function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Establish First Time Setup DB Setup Function
def firstTimeDbSetup():
    if os.path.exists('database.db'):
        print("Database File Exists")
    else:
        # Do initial DB File and Table setup
        conn = get_db_connection()
        with open('schema.sql') as schema:
            conn.executescript(schema.read())
        conn.commit()
        conn.close()

# Establish Meraki API Key
def GetMerakiAPIKey():
    MERAKI_API_KEY = ''
    conn = get_db_connection()
    cur = conn.cursor()
    keycheck = cur.execute(
           'SELECT * FROM globalparams WHERE name=? LIMIT 1', ["MerakiAPIKey"])
    keyexists = keycheck.fetchone()
    conn.close()
    if keyexists is not None:
        MERAKI_API_KEY = keyexists['param']
        return MERAKI_API_KEY
    else:
        return None

# Establish Meraki Org ID
def GetMerakiOrgID():
    OrgID = ''
    conn = get_db_connection()
    cur = conn.cursor()
    orgidcheck = cur.execute(
            'SELECT param FROM globalparams WHERE name=? AND active=? LIMIT 1', ["MerakiOrgID","1"])
    orgidexists = orgidcheck.fetchone()
    conn.close()
    if orgidexists is not None:
        OrgID = orgidexists['param']
        return OrgID
    else:
        return None

# Establish Network ID
def GetMerakiNetworkID():
    NetworkID = ''
    conn = get_db_connection()
    cur = conn.cursor()
    networkidcheck = cur.execute(
            'SELECT param FROM globalparams WHERE name=? AND active=? LIMIT 1', ["MerakiNetworkID","1"])
    networkidexists = networkidcheck.fetchone()
    conn.close()
    if networkidexists is not None:
        NetworkID = networkidexists['param']
        return NetworkID
    else:
        return None

# Function to Create YAML and start ngrok instance on initial setup
def ngrok_tunnel(ngrokkey):
    if ngrokkey is not None:
        doc = {'authtoken': ngrokkey,'tunnels': {'merakihud': {'addr':5000,'proto':'http','root_cas':'trusted'}}}
        with open("ngrok.yml","w") as f:
            yaml.dump(doc, f)

# Function to start ngrok instance e.g. when restart button on Admin page is hit
def startngroktunnel():
    ngrokFile = os.path.abspath("ngrok.yml")
    ngrokConfig = conf.PyngrokConfig(config_path=ngrokFile)
    # conf.set_default(ngrokConfig)
    http_tunnel = ngrok.connect(name='merakihud', pyngrok_config=ngrokConfig)