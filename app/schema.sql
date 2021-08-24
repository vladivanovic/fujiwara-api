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
    organizationId TEXT NOT NULL,
    networkId TEXT NOT NULL,
    networkUrl TEXT NOT NULL,
    networkTags TEXT NOT NULL,
    deviceSerial TEXT NOT NULL,
    deviceMac TEXT NOT NULL,
    deviceName TEXT NOT NULL,
    deviceUrl TEXT NOT NULL,
    deviceTags TEXT NOT NULL,
    deviceModel TEXT NOT NULL,
    alertId TEXT NOT NULL,
    alertType TEXT NOT NULL,
    alertTypeId TEXT NOT NULL,
    alertLevel TEXT NOT NULL,
    occurredAt TEXT NOT NULL,
    alertData TEXT NOT NULL,
    other TEXT
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

