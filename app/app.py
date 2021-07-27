# All of the Imports
from flask import Flask, render_template, request, url_for, flash, redirect, Response
from werkzeug.exceptions import abort
import meraki
from pyngrok import ngrok
import app_startchecks as appsc

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

test = appsc.GetMerakiAPIKey()
print(test)

# Default App Route
@app.route('/')
def index():
    global dashboard
    global MERAKI_API_KEY
    # Check DB Population, if none then redirect to First Time DB Population
    conn = appsc.get_db_connection()

    # Checking for MerakiID, OrgID and NetworkID then redirecting as necessary
    if appsc.GetMerakiAPIKey == None:
        return redirect(url_for('firsttime'))
    elif appsc.GetMerakiOrgID() == None:
        MERAKI_API_KEY = appsc.GetMerakiAPIKey()
        dashboard = meraki.DashboardAPI(MERAKI_API_KEY)
        return redirect(url_for('firsttimeorgid'))
    elif appsc.GetMerakiNetworkID() == None:
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
            appsc.ngrok_tunnel(ngrokKey)
            # Update Database with Meraki API Key
            conn = appsc.get_db_connection()
            dbupdate = conn.execute(
                "INSERT INTO globalparams (name, param, other, active) VALUES ('MerakiAPIKey', ?, 'none', '1')", [MerakiAPIKey])
            conn.commit()
            conn.close()
            # Update Global Variable temporarily, when Flask reloads it'll grab it from the Database
            MERAKI_API_KEY = MerakiAPIKey
            dashboard = meraki.DashboardAPI(MERAKI_API_KEY)
            # Grab and Store Org IDs in DB
            OrgList = dashboard.organizations.getOrganizations()
            for Org in OrgList:
                OrgID = Org['id']
                OrgName = Org['name']
                conn = appsc.get_db_connection()
                orgids = conn.execute(
                    "INSERT INTO globalparams (name, param, other, active) VALUES ('MerakiOrgID', ?, ?, '0')", [OrgID, OrgName])
                conn.commit()
                conn.close()
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
            conn = appsc.get_db_connection()
            activeorgid = conn.execute(
                "UPDATE globalparams SET active = '1' WHERE param = ?", [MerakiOrgID])
            conn.commit()
            conn.close()
            # Update Global Variable, when Flask reloads it'll grab it from the Database
            OrgID = MerakiOrgID
            # Grab and Store Network IDs in DB
            OrgNetworks = dashboard.organizations.getOrganizationNetworks(OrgID)
            for Networks in OrgNetworks:
                NetworkID = Networks['id']
                NetworkName = Networks['name']
                conn = appsc.get_db_connection()
                networkids = conn.execute(
                    "INSERT INTO globalparams (name, param, other, active) VALUES ('MerakiNetworkID', ?, ?, '0')", [NetworkID, NetworkName])
                conn.commit()
                conn.close()
            return redirect(url_for('firsttimenetworkid'))
    return render_template('firsttimeorgid.html', merakiorgids=merakiorgids)

# First Time setup page - Meraki Org ID
@app.route('/firsttimenetworkid', methods=['GET', 'POST'])
def firsttimenetworkid():
    global NetworkID
    # Grab all NetworkIDs from Database
    conn = appsc.get_db_connection()
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
            conn = appsc.get_db_connection()
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
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    ngrok_tunnel = ngrok.get_tunnels()
    return render_template('admin.html')

# Create Webhook Listener
@app.route('/listen', methods=['POST'])
def listen():
    print(request.json)
    return Response(status=200)


