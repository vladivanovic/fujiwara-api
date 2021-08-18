#!/bin/bash

# Kickstart Webhook App in Screen Instance
#screen -dmS merakihud python3 webhook.py # screen didn't work
tmux new-session -d -s merakiengineio \; send-keys "python3 engineio.py" Enter