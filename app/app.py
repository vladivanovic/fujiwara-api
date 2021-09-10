#!/usr/bin/python3

# All of the Imports
from flask import Flask, render_template, request, url_for, flash, redirect
import meraki
import app_startchecks as appsc
from psycopg2.extras import RealDictCursor

# Kickstart Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vlad1234'  # (temporary random string)

# Kickstart DB Setup
appsc.firstTimeDbSetup()

# Establish Global Variables
global MERAKI_API_KEY
global dashboard
global OrgID
global NetworkID


# Default App Route
@app.route('/')
def index():
    global dashboard
    global MERAKI_API_KEY
    # Checking for MerakiID, OrgID and NetworkID then redirecting to finish setup as necessary
    verifyMerAPIKey = appsc.GetMerakiAPIKey()
    verifyMerOrgID = appsc.GetMerakiOrgID()
    verifyMerNetID = appsc.GetMerakiNetworkID()
    if verifyMerAPIKey is None:
        return redirect(url_for('firsttime'))
    elif verifyMerOrgID is None:
        MERAKI_API_KEY = appsc.GetMerakiAPIKey()
        dashboard = meraki.DashboardAPI(MERAKI_API_KEY)
        return redirect(url_for('firsttimeorgid'))
    elif verifyMerNetID is None:
        MERAKI_API_KEY = appsc.GetMerakiAPIKey()
        dashboard = meraki.DashboardAPI(MERAKI_API_KEY)
        return redirect(url_for('firsttimenetworkid'))
    else:
        MERAKI_API_KEY = appsc.GetMerakiAPIKey()
        dashboard = meraki.DashboardAPI(MERAKI_API_KEY)
        return render_template('index.html')


# First Time setup page - Meraki API Key
@app.route('/firsttime', methods=['GET', 'POST'])
def firsttime():
    global MERAKI_API_KEY
    global dashboard
    if request.method == 'POST':
        MerakiAPIKey = request.form['MerakiAPIKey']
        ngrokKey = request.form['ngrokKey']
        if not MerakiAPIKey:
            flash('Meraki API Key required!')
        else:
            # Update ngrok YML file
            if ngrokKey is not None:
                appsc.ngrok_tunnel(ngrokKey)
            # Update Database with Meraki API Key
            conn = appsc.get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            dbupdate = cur.execute(
                "INSERT INTO globalparams (name, param, other, active) VALUES ('MerakiAPIKey', %s , 'none', '1')", [MerakiAPIKey])
            cur.close()
            conn.commit()
            # Update Global Variable temporarily, when Flask reloads it'll grab it from the Database
            MERAKI_API_KEY = MerakiAPIKey
            dashboard = meraki.DashboardAPI(MERAKI_API_KEY)
            # Grab and Store Org IDs in DB
            OrgList = dashboard.organizations.getOrganizations()
            for Org in OrgList:
                OrgID = Org['id']
                OrgName = Org['name']
                conn = appsc.get_db_connection()
                cur = conn.cursor(cursor_factory=RealDictCursor)
                orgids = cur.execute(
                    "INSERT INTO globalparams (name, param, other, active) VALUES ('MerakiOrgID', %s , %s , '0')", [OrgID, OrgName])
                cur.close()
                conn.commit()
            return redirect(url_for('firsttimeorgid'))
    # If nothing else, render the page
    return render_template('firsttime.html')


# First Time setup page (Organization ID)
@app.route('/firsttimeorgid', methods=['GET', 'POST'])
def firsttimeorgid():
    global dashboard
    global OrgID
    # Grab all OrgIDs from Database
    conn = appsc.get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT param, other FROM globalparams WHERE name = 'MerakiOrgID'")
    merakidborgids = cur.fetchall()
    merakiorgids = []
    for row in merakidborgids:
        merakiorgids.append(dict(row))
    cur.close()
    if request.method == 'POST':
        # Grab the confirmed Meraki Org ID
        MerakiOrgID = request.form['MerakiOrgID']
        if not MerakiOrgID:
            flash('Please enter one of these Org IDs')
        else:
            # Update Database with Active Org ID
            conn = appsc.get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            activeorgid = cur.execute(
                "UPDATE globalparams SET active = '1' WHERE param = %s", [MerakiOrgID])
            cur.close()
            conn.commit()
            # Update Global Variable, when Flask reloads it'll grab it from the Database
            OrgID = MerakiOrgID
            # Grab and Store Network IDs in DB
            OrgNetworks = dashboard.organizations.getOrganizationNetworks(OrgID)
            for Networks in OrgNetworks:
                NetworkID = Networks['id']
                NetworkName = Networks['name']
                conn = appsc.get_db_connection()
                cur = conn.cursor()
                networkids = cur.execute(
                    "INSERT INTO globalparams (name, param, other, active) VALUES ('MerakiNetworkID', %s , %s , '0')", [NetworkID, NetworkName])
                cur.close()
                conn.commit()
            return redirect(url_for('firsttimenetworkid'))
    return render_template('firsttimeorgid.html', merakiorgids=merakiorgids)


# First Time setup page - Meraki Org ID
@app.route('/firsttimenetworkid', methods=['GET', 'POST'])
def firsttimenetworkid():
    global NetworkID
    # Grab all NetworkIDs from Database
    conn = appsc.get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT param, other FROM globalparams WHERE name = 'MerakiNetworkID'")
    merakidbnetworkids = cur.fetchall()
    merakinetworkids = []
    for row in merakidbnetworkids:
        merakinetworkids.append(dict(row))
    cur.close()
    if request.method == 'POST':
        # Grab the confirmed Meraki Network ID
        MerakiNetworkID = request.form['MerakiNetworkID']
        if not MerakiNetworkID:
            flash('Please enter one of these Network IDs')
        else:
            # Update Database with Active Org ID
            conn = appsc.get_db_connection()
            cur = conn.cursor()
            activeorgid = cur.execute(
                "UPDATE globalparams SET active = '1' WHERE param = %s ", [MerakiNetworkID])
            cur.close()
            conn.commit()
            # Update Global Variable, when Flask reloads it'll grab it from the Database
            NetworkID = MerakiNetworkID
            # Grab and Store Network IDs in DB
            return redirect(url_for('admin'))
    return render_template('firsttimenetworkid.html', merakinetworkids=merakinetworkids)


# Create an Admin Page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['submit_button'] == 'webhook_restart':
            appsc.webhook_start()
        elif request.form['submit_button'] == 'engineio_restart':
            appsc.engineio_start()
        elif request.form['submit_button'] == 'inventory_collection':
            appsc.getNetworkDevices()
        elif request.form['submit_button'] == 'snmp_poll':
            appsc.pollDevices(device_ip, snmpcomm)  #need input?
        else:
            pass
    webhook_status = appsc.webhook_status()
    if webhook_status is None:
        webhook_status = 'Webhook not up'
    engineio_status = appsc.engineio_status()
    if engineio_status is None:
        engineio_status = 'Engine.IO is not up'
    return render_template('admin.html', webhook_status=webhook_status, engineio_status=engineio_status)


@app.route('/livestatus', methods=['GET'])
def livestatus():
    conn = appsc.get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT devicename, model, serial, lanip, status FROM devices WHERE status IS NOT NULL")
    merakidevices = cur.fetchall()
    merakidevicelist = []
    for row in merakidevices:
        merakidevicelist.append(dict(row))
    cur.execute(
        "SELECT alertid, alerttype, alerttypeid, alertlevel, occurredat, alertdata, devicename, devicemodel FROM alerts")
    merakialerts = cur.fetchall()
    merakialertslist = []
    for row in merakialerts:
        merakialertslist.append(dict(row))
    cur.close()
    print(merakidevicelist)
    print(merakialertslist)
    return render_template('livestatus.html', devicelist=merakidevicelist, alertlist=merakialertslist)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

