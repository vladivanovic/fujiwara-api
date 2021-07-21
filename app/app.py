# All of the Imports
from flask import Flask, render_template, request, url_for, flash, redirect, Response
import sqlite3
from werkzeug.exceptions import abort
import os
import meraki
import cv2

# Establish Database Connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Establish First Time Setup DB Setup
if os.path.exists('database.db'):
    print("File Exists")
else:
    # Do initial DB File and Table setup
    conn = get_db_connection()
    with open('schema.sql') as schema:
        conn.executescript(schema.read())
    conn.commit()
    conn.close()

# Establish Meraki API Key
global MERAKI_API_KEY
MERAKI_API_KEY = ''
conn = get_db_connection()
cur = conn.cursor()
keycheck = cur.execute(
       'SELECT * FROM globalparams WHERE name=? LIMIT 1', ["MerakiAPIKey"])
keyexists = keycheck.fetchone()
if not keyexists == None:
        MERAKI_API_KEY = keyexists['param']
conn.close()

# Establish Global dashboard Variable to access Meraki API
global dashboard
dashboard = meraki.DashboardAPI(MERAKI_API_KEY);

# Establish Meraki Org ID
global OrgID
OrgID = ''
conn = get_db_connection()
cur = conn.cursor()
orgidcheck = cur.execute(
        'SELECT param FROM globalparams WHERE name=? AND active=? LIMIT 1', ["MerakiOrgID","1"])
orgidexists = orgidcheck.fetchone()
if not orgidexists == None:
	OrgID = orgidexists['param']
conn.close()

# Establish Network ID
global NetworkID
NetworkID = ''
conn = get_db_connection()
cur = conn.cursor()
networkidcheck = cur.execute(
        'SELECT param FROM globalparams WHERE name=? AND active=? LIMIT 1', ["MerakiNetworkID","1"])
networkidexists = networkidcheck.fetchone()
if not networkidexists == None:
        NetworkID = networkidexists['param']
conn.close()

# Kickstart Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vlad1234'  # (temporary random string)

# Default App Route
@app.route('/')
def index():
    # Check DB Population, if none then redirect to First Time DB Population
    conn = get_db_connection()
    keycheck = conn.execute(
        'SELECT 1 FROM globalparams WHERE name=? LIMIT 1', ["MerakiAPIKey"])
    keyexists = keycheck.fetchone()
    print(keyexists)
    # (NEED TO CHECK FOR ORGID AND NETWORKID TOO)
    if keyexists == None:
        return redirect(url_for('firsttime'))
    else:
        return render_template('index.html')



# First Time setup page - Meraki API Key
@app.route('/firsttime', methods=('GET', 'POST'))
def firsttime():
    global dashboard
    global MERAKI_API_KEY
    if request.method == 'POST':
        MerakiAPIKey = request.form['MerakiAPIKey']
        print(MerakiAPIKey)
        if not MerakiAPIKey:
            flash('Meraki API Key required!')
        else:
            # Update Database with Meraki API Key
            conn = get_db_connection()
            merakiapikey = conn.execute(
                "INSERT INTO globalparams (name, param, other, active) VALUES ('MerakiAPIKey', ?, 'none', '1')", [MerakiAPIKey])
            conn.commit()
            conn.close()
            # Update Global Variable temporarily, when Flask reloads it'll grab it from the Database
            MERAKI_API_KEY = MerakiAPIKey
            # Grab and Store Org IDs in DB
            OrgList = dashboard.organizations.getOrganizations()
            for Org in OrgList:
                OrgID = Org['id']
                OrgName = Org['name']
                conn = get_db_connection()
                orgids = conn.execute(
                    "INSERT INTO globalparams (name, param, other, active) VALUES ('MerakiOrgID', ?, ?, '0')", [OrgID, OrgName])
                conn.commit()
                conn.close()
            return redirect(url_for('firsttimeorgid'))
    # If nothing else, render the page
    return render_template('firsttime.html')

# First Time setup page (Organization ID)
@app.route('/firsttimeorgid', methods=('GET', 'POST'))
def firsttimeorgid():
    global dashboard
    global MERAKI_API_KEY
    # Grab all OrgIDs from Database
    conn = get_db_connection()
    merakiorgids = conn.execute(
        "SELECT * FROM globalparams WHERE name = 'MerakiOrgID'").fetchall()
    conn.close()
    if request.method == 'POST':
        # Grab the confirmed Meraki Org ID
        MerakiOrgID = request.form['MerakiOrgID']
        if not MerakiOrgID:
            flash('Please enter one of these Org IDs')
        else:
            # Update Database with Active Org ID
            conn = get_db_connection()
            activeorgid = conn.execute(
                "UPDATE globalparams SET active = '1' WHERE param = ?", [MerakiOrgID])
            conn.commit()
            conn.close()
            # Update Global Variable, when Flask reloads it'll grab it from the Database
            OrgID = MerakiOrgID
            # Grab and Store Network IDs in DB
            OrgNetworks = dashboard.networks.getOrganizationNetworks(OrgID)
            for Networks in OrgNetworks:
                NetworkID = Networks['id']
                NetworkName = Networks['name']
                conn = get_db_connection()
                networkids = conn.execute(
                    "INSERT INTO globalparams (name, param, other, active) VALUES ('MerakiNetworkID', ?, ?, '0')", [NetworkID, NetworkName])
                conn.commit()
                conn.close()
            return redirect(url_for('firsttimenetworkid'))
    return render_template('firsttimeorgid.html', merakiorgids=merakiorgids)

# First Time setup page - Meraki Org ID
@app.route('/firsttimenetworkid', methods=('GET', 'POST'))
def firsttimenetworkid():
    # Grab all NetworkIDs from Database
    conn = get_db_connection()
    merakinetworkids = conn.execute(
        "SELECT * FROM globalparams WHERE name = 'MerakiNetworkID'").fetchall()
    conn.close()
    if request.method == 'POST':
        # Grab the confirmed Meraki Network ID
        MerakiNetworkID = request.form['MerakiNetworkID']
        if not MerakiNetworkID:
            flash('Please enter one of these Network IDs')
        else:
            # Update Database with Active Org ID
            conn = get_db_connection()
            activeorgid = conn.execute(
                "UPDATE globalparams SET active = '1' WHERE param = ?", [MerakiNetworkID])
            conn.commit()
            conn.close()
            # Update Global Variable, when Flask reloads it'll grab it from the Database
            NetworkID = MerakiNetworkID
            # Grab and Store Network IDs in DB
            return redirect(url_for('admin'))
    return render_template('firsttimenetworkid.html', merakinetworkids=merakinetworkids)

# Create an Admin Page
@app.route('/admin', methods=('GET', 'POST'))
def admin():
    return render_template('admin.html')




