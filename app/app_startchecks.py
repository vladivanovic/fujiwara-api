# All of the Imports
import sqlite3
import os
import meraki
from pyngrok import ngrok

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
    if not keyexists == None:
        MERAKI_API_KEY = keyexists['param']
    return MERAKI_API_KEY
    conn.close()

# Establish Meraki Org ID
def GetMerakiOrgID():
    OrgID = ''
    conn = get_db_connection()
    cur = conn.cursor()
    orgidcheck = cur.execute(
            'SELECT param FROM globalparams WHERE name=? AND active=? LIMIT 1', ["MerakiOrgID","1"])
    orgidexists = orgidcheck.fetchone()
    if not orgidexists == None:
        OrgID = orgidexists['param']
    return OrgID
    conn.close()

# Establish Network ID
def GetMerakiNetworkID():
    NetworkID = ''
    conn = get_db_connection()
    cur = conn.cursor()
    networkidcheck = cur.execute(
            'SELECT param FROM globalparams WHERE name=? AND active=? LIMIT 1', ["MerakiNetworkID","1"])
    networkidexists = networkidcheck.fetchone()
    if not networkidexists == None:
        NetworkID = networkidexists['param']
    return NetworkID
    conn.close()

# Function to Kickstart nGrok instance for Meraki Webhook - Creates tunnel from nGrok on Port 80 (e.g. http://localhost:80/)
def ngrok_tunnel():
    http_tunnel = ngrok.connect()


