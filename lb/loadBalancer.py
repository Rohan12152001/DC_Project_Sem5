# Load Balancer

from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import mysql.connector, sys, os, webbrowser
import requests, signal

hitCount = -1

app = Flask(__name__, static_url_path='/templates/static')

# signal
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

# Home page
@app.route('/')
def load_balancer():
    # define Ports
    portsAvailable = [50000, 5000]
    global hitCount
    hitCount += 1
    return redirect(f"http://localhost:{portsAvailable[hitCount%2]}/app", code=200)

if __name__ == '__main__':
    app.secret_key = "super secret key"
    # signal to close the DB connection
    signal.signal(signal.SIGINT, signal_handler)
    app.run(port=8080, debug=False)