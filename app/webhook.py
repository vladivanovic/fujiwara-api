#!/usr/bin/python3
# All of the Imports
import requests
from flask import Flask, request, Response, jsonify, abort
from pyngrok import ngrok
import app_startchecks as appsc

# Kickstart Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fred1234'  # (temporary random string)

# Start ngrok tunnel
appsc.startngroktunnel()

# Get ngrok Tunnels for auto-set Meraki Webhooks
ngrok_tunnels = ngrok.get_tunnels()
ngrok_tunnel = []
if ngrok_tunnels is not None:
    for tunnels in ngrok_tunnels:
        tunnels = str(tunnels)
        ngrok_tunnel.append(tunnels)
else:
    ngrok_tunnel = None

# Get the Meraki Webhooks and Alerts updated to newest ngrok tunnel
appsc.merakiWebhookSetup(ngrok_tunnel)


# Default App Route and Webhook Status
@app.route('/')
def index():
    global ngrok_tunnel
    if ngrok_tunnel is not None:
        return jsonify(status='TUNNEL UP', tunnel_data=ngrok_tunnel)
    else:
        return jsonify(status='TUNNEL DOWN')


# Create Webhook Listener
@app.route('/listen', methods=['POST'])
def listen():
    if request.method == "POST":
        alert = request.json
        print(alert)
        if alert['sharedSecret'] == 'auto-ngrok':
            if alert['alertTypeId'] == 'sensor_alert':
                payload = alert
                response = requests.post('http://localhost:5002/listen', json=payload)
                print(response)
                return Response(status=200)
            else:
                return Response(status=200)
        else:
            abort(401)
    else:
        abort(400)


# Secret Status Page
@app.route('/status', methods=['GET'])
def status():
    return jsonify(status='SERVER UP')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
