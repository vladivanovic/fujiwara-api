#!/usr/bin/python3
# All of the Imports
from flask import Flask, render_template, request, Response, jsonify
from pyngrok import ngrok
import app_startchecks as appsc

# Kickstart Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fred1234'  # (temporary random string)

appsc.startngroktunnel()


# Default App Route and Webhook Status
@app.route('/')
def index():
    ngrok_tunnels = ngrok.get_tunnels()
    ngrok_tunnel = []
    if ngrok_tunnels is not None:
        for tunnels in ngrok_tunnels:
            tunnels = str(tunnels)
            ngrok_tunnel.append(tunnels)
            print(ngrok_tunnel)
        return jsonify(status='UP', tunnel_data=ngrok_tunnel)
    else:
        return jsonify(status='DOWN')


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
    app.run(host='0.0.0.0', port=5001, debug=False)
