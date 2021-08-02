#!/usr/bin/env python3

# All of the Imports
from flask import Flask, render_template, request, url_for, flash, redirect, Response, jsonify
from pyngrok import ngrok
import app_startchecks as appsc

# Kickstart Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fred1234'  # (temporary random string)

# Default App Route and Webhook Status
@app.route('/')
def index():
    appsc.startngroktunnel()
    ngrok_tunnels = ngrok.get_tunnels()
    ngrok_tunnel = ''
    for tunnels in ngrok_tunnels:
        ngrok_tunnel = str(tunnels)
    return jsonify(status='UP', tunnel_data=ngrok_tunnel)

# Create Webhook Listener
@app.route('/listen', methods=['POST'])
def listen():
    print(request.json)
    return Response(status=200)

# Secret Status Page
@app.route('/status', methods=['GET'])
def status():
    return render_template('webhook_index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)