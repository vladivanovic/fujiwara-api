#!/usr/bin/python3
# All of the Imports
from flask import Flask, request, Response, jsonify
import app_startchecks as appsc
import sensorTrigger as sT
from psycopg2.extras import RealDictCursor

# Kickstart Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'engineio1234'  # (temporary random string)


# Default App Route and Webhook Status
@app.route('/')
def index():
    return Response(status=200)


# Create Webhook Listener
@app.route('/listen', methods=['POST'])
def listen():
    reqbody = request.json
    print(reqbody)
    exec_code = sT.webhook_rx(reqbody)
    return jsonify(status="Alert Received")

# Secret Status Page
@app.route('/status', methods=['GET'])
def status():
    return jsonify(status='SERVER UP')


# Page to trigger device updates
@app.route('/devices', methods=['GET'])
def devices():
    appsc.getNetworkDevices()
    return jsonify(status="Refreshing Meraki Device List")


# Page to trigger device polls
@app.route('/devicepoll', methods=['GET'])
def devicepoll():
    conn = appsc.get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # SQL Query here from SNMP Community per NetworkID
    cur.execute(
        "SELECT param, other FROM globalparams WHERE name = 'MerakiSNMP'")
    snmpcomm = cur.fetchall()
    snmpList = []
    for snmpid in snmpcomm:
        snmpList.append(dict(snmpid))
    print(snmpList)
    # SQL Query here for Devices + NetworkID
    cur.execute(
        "SELECT model, lanip, networkid FROM devices WHERE lanip IS NOT NULL")
    dbdevices = cur.fetchall()
    devicelist = []
    for row in dbdevices:
        print(row)
        row = dict(row)
        print(row)
        for snmpKeys in snmpList:
            if row['networkid'] == snmpKeys['other']:
                row['snmpKey'] = snmpKeys['param']
            else:
                pass
        print(row)
        devicelist.append(row)
    print(devicelist)
    cur.close()
    # Trigger the Device Poll
    for device in devicelist:
        appsc.pollDevices(device['lanip'], device['snmpKey'])
        # Eventually return the result to DB updating available or not
    return jsonify(status="Polling all Network Devices via SNMP")


# Page to trigger updating SNMP and other variables
@app.route('/networksnmp', methods=['GET'])
def getNetworkSnmp():
    appsc.GetMerakiSNMPString()
    return jsonify(status="Refresh Network SNMP List in DB")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
