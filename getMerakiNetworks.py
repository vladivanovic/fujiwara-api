import os
import meraki
import sqlite3

MERAKI_API_KEY = os.environ.get("MERAKI_API_KEY")
dashboard = meraki.DashboardAPI(MERAKI_API_KEY);


global OrgID
OrgID = '';

OrgList = dashboard.organizations.getOrganizations();
for Org in OrgList:
	OrgID = Org['id'];


global NetworkID
NetworkID = '';

OrgNetworks = dashboard.networks.getOrganizationNetworks(OrgID);
for Networks in OrgNetworks:
	if [wifi for wifi in Networks['productTypes'] if wifi.endswith('wireless')]:
		NetworkID = Networks['id'];


global WirelessDevices
WirelessDevices = [];

NetworkDevices = dashboard.devices.getNetworkDevices(NetworkID);
for Devices in NetworkDevices:
	if Devices['model'] == 'MR32':
		print(Devices['name'], Devices['model'], Devices['firmware']);


def uploadSSIDs():
	UpSSIDs = dashboard.ssids.getNetworkSsids(NetworkID);
	for SSIDs in UpSSIDs:
		# Set the Variables, convert Null to Strings
		number = str(SSIDs.get('number'));
		name = str(SSIDs.get('name') or 'Unused');
		enabled = str(SSIDs.get('enabled') or 'Unused');
		authMode = str(SSIDs.get('authMode') or 'Unused');
		ipAssignmentMode = str(SSIDs.get('ipAssignmentMode') or 'Unused');
		useVlanTagging = str(SSIDs.get('useVlanTagging') or 'Unused');
		splashPage = str(SSIDs.get('splashPage') or 'Unused');
		adminSplashUrl = str(SSIDs.get('adminSplashUrl') or 'Unused');
		splashTimeout = str(SSIDs.get('splashTimeout') or 'Unused');
		walledGardenEnabled = str(SSIDs.get('walledGardenEnabled') or 'Unused');
		perClientBandwidthLimitUp = str(SSIDs.get('perClientBandwidthLimitUp') or 'Unused');
		perClientBandwidthLimitDown = str(SSIDs.get('perClientBandwidthLimitDown') or 'Unused');
		# Connecting to the Database to Upload
		conn = sqlite3.connect('database.db')
		conup = conn.cursor()
		ssidupload = conup.execute("""INSERT INTO ssids (number, name, enabled, authMode, ipAssignmentMode, useVlanTagging, splashPage, adminSplashUrl, splashTimeout, walledGardenEnabled, perClientBandwidthLimitUp, perClientBandwidthLimitDown) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [number, name, enabled, authMode, ipAssignmentMode, useVlanTagging, splashPage, adminSplashUrl, splashTimeout, walledGardenEnabled, perClientBandwidthLimitUp, perClientBandwidthLimitDown])
		conn.commit()
		conn.close()
		print('sqlite3 database first time upload done');



def updateSSIDs():
	UpSSIDs = dashboard.ssids.getNetworkSsids(NetworkID);
	for SSIDs in UpSSIDs:
		# Set the Variables, convert Null to Strings
		number = str(SSIDs.get('number'));
		name = str(SSIDs.get('name') or 'Unused');
		enabled = str(SSIDs.get('enabled') or 'Unused');
		authMode = str(SSIDs.get('authMode') or 'Unused');
		ipAssignmentMode = str(SSIDs.get('ipAssignmentMode') or 'Unused');
		useVlanTagging = str(SSIDs.get('useVlanTagging') or 'Unused');
		splashPage = str(SSIDs.get('splashPage') or 'Unused');
		adminSplashUrl = str(SSIDs.get('adminSplashUrl') or 'Unused');
		splashTimeout = str(SSIDs.get('splashTimeout') or 'Unused');
		walledGardenEnabled = str(SSIDs.get('walledGardenEnabled') or 'Unused');
		perClientBandwidthLimitUp = str(SSIDs.get('perClientBandwidthLimitUp') or 'Unused');
		perClientBandwidthLimitDown = str(SSIDs.get('perClientBandwidthLimitDown') or 'Unused');
		# Connecting to the Database to Upload
		conn = sqlite3.connect('database.db')
		conup = conn.cursor()
		ssidupload = conup.execute("""INSERT INTO ssids (number, name, enabled, authMode, ipAssignmentMode, useVlanTagging, splashPage, adminSplashUrl, splashTimeout, walledGardenEnabled, perClientBandwidthLimitUp, perClientBandwidthLimitDown) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(number) DO UPDATE SET name=excluded.name""", [number, name, enabled, authMode, ipAssignmentMode, useVlanTagging, splashPage, adminSplashUrl, splashTimeout, walledGardenEnabled, perClientBandwidthLimitUp, perClientBandwidthLimitDown])
		conn.commit()
		conn.close()
		print('sqlite3 database updated')


def deployGuestWifi():
	number = '9';
	name = 'Vlad API Test';
	enabled = 'False';
	authMode = 'open';
	ipAssignmentMode = 'Bridge';
	useVlanTagging = 'False';
	splashPage = 'Click-through splash page';
	adminSplashUrl = 'http://192.168.11.245:3000/';
	splashTimeout = '1440';
	walledGardenEnabled = 'True';
	walledGardenRanges = '192.168.11.245/32';
	perClientBandwidthLimitUp = '512';
	perClientBandwidthLimitDown = '1024';
	deployed = dashboard.ssids.updateNetworkSsid(NetworkID, number=number, name=name, enabled=enabled, authMode=authMode, ipAssignmentMode=ipAssignmentMode, useVlanTagging=useVlanTagging, splashPage=splashPage, adminSplashUrl=adminSplashUrl, splashTimeout=splashTimeout, walledGardenRanges=walledGardenRanges, walledGardenEnabled=walledGardenEnabled, perClientBandwidthLimitUp=perClientBandwidthLimitUp, perClientBandwidthLimitDown=perClientBandwidthLimitDown);


with sqlite3.connect('database.db') as conn:
	conup = conn.cursor()
	conup.execute("""SELECT COUNT(*) from ssids""")
	result = conup.fetchall()
	print(result)
	if result[0][0] == 0:
		print('uploading SSIDs')
		uploadSSIDs()
		print('finished initial SSID upload')
	else:
		print('updating SSIDs')
		updateSSIDs()
		print('finished updating SSIDs')


