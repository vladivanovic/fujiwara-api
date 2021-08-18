#!/usr/bin/python3
# All of the Imports
from flask import Flask, render_template, request, Response, jsonify, abort
import app_startchecks as appsc

# Kickstart Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'engineio1234'  # (temporary random string)


# Default App Route and Webhook Status
@app.route('/')
def index():
    return jsonify(status='TUNNEL DOWN'),  Response(status=200)


# Create Webhook Listener
@app.route('/listen', methods=['POST'])
def listen():
    print(request.json)
    return Response(status=200)


# Secret Status Page
@app.route('/status', methods=['GET'])
def status():
    return jsonify(status='SERVER UP')


# Secret Status Page
@app.route('/devices', methods=['GET'])
def devices():
    appsc.getNetworkDevices()
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
