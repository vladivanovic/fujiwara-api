#!/bin/bash

# Kickstart Main Flask App in Screen Instance
screen -dmS localhost python3 app.py

# Kickstart Main Flask App in Screen Instance
screen -dmS localhost python3 webhook.py
