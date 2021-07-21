DROP TABLE IF EXISTS globalparams;
DROP TABLE IF EXISTS ssids;

CREATE TABLE globalparams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT  NOT NULL,
    param TEXT NOT NULL,
    other TEXT NOT NULL,
    active TEXT NOT NULL
);

CREATE TABLE ssids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    number TEXT NOT NULL,
    name TEXT NOT NULL,
    enabled TEXT NOT NULL,
    authMode TEXT NOT NULL,
    ipAssignmentMode TEXT NOT NULL,
    useVlanTagging TEXT NOT NULL,
    splashPage TEXT NOT NULL,
    adminSplashUrl TEXT NOT NULL,
    splashTimeout TEXT NOT NULL,
    walledGardenEnabled TEXT NOT NULL,
    perClientBandwidthLimitUp TEXT NOT NULL,
    perClientBandwidthLimitDown TEXT NOT NULL
);

CREATE UNIQUE INDEX ssid_numbers ON ssids (number);
