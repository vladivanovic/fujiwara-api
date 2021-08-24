-- THIS FILE DOES THE BASE SETUP OF THE POSTGRESQL merakihuddb DATABASE

-- SETUP globalparams TABLE

CREATE TABLE IF NOT EXISTS globalparams (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    param TEXT NOT NULL,
    other TEXT NOT NULL,
    active TEXT NOT NULL
);

-- SETUP alerts TABLE

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    'organizationId': '599325',
    'networkId': 'L_602356450160805816',
    'networkName': 'Vlad Home Network',
    'networkUrl': 'https://n70.meraki.com/Vlad-Home-Networ/n/B7Ik3cgb/manage/nodes/list',
    'networkTags': [],
    'deviceSerial': 'Q3CC-JL2P-8KDU',
    'deviceMac': 'f8:9e:28:7e:27:fc',
    'deviceName': 'Door Sensor MT20',
    'deviceUrl': 'https://n70.meraki.com/Vlad-Home-Networ/n/B7Ik3cgb/manage/nodes/new_list/273358167877628',
    'deviceTags': [],
    'deviceModel': 'MT20',
    'alertId': '602356450234795601',
    'alertType': 'Sensor change detected',
    'alertTypeId': 'sensor_alert',
    'alertLevel': 'informational',
    'occurredAt': '2021-08-13T08:36:24.732000Z',
    'alertData': {
        'alertConfigId': 602356450161244932,
        'triggerData': [{
            'conditionId': 323,
            'trigger': {
                'ts': 1628843784,
                'type': 'door',
                'nodeId': 273358167877628,
                'sensorValue': 0.0
                }
            }],
        'startedAlerting': False
    }
}
    other TEXT NOT NULL
);

-- SETUP devices TABLE

CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    devicename TEXT NOT NULL,
    serial TEXT NOT NULL UNIQUE,
    macaddress TEXT NOT NULL,
    wirelessMac TEXT,
    model TEXT NOT NULL,
    lanIp TEXT,
    wanIp TEXT,
    tags TEXT NOT NULL,
    networkId TEXT NOT NULL,
    lat TEXT NOT NULL,
    long TEXT NOT NULL,
    status TEXT
);

