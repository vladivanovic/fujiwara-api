#!/bin/bash

# Kickstart Webhook App in Screen Instance
#screen -dmS merakihud python3 webhook.py # screen didn't work
tmux new-session -d -s merakihud \; send-keys "python3 webhook.py" Enter