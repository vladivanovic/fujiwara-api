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
    other TEXT NOT NULL
);

-- SETUP devices TABLE

CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    devicename TEXT NOT NULL,
    serial TEXT NOT NULL,
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

