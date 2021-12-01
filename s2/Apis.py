from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import mysql.connector, sys, os, webbrowser
import requests, signal
# from flask_mysqldb import MySQL

app = Flask(__name__, static_url_path='/templates/static')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ.get("Pass")
app.config['MYSQL_DB'] = 'DcCovidData'

# mysql = MySQL(app)

# signal
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    # close()
    sys.exit(0)

# Home page
@app.route('/app')
def home_page():
    return render_template('index.html')

# EDIT Panel page
@app.route('/app/panel')
def panel_page():
    return render_template('panel.html')


if __name__ == '__main__':
    app.secret_key = "super secret key"
    # signal to close the DB connection
    signal.signal(signal.SIGINT, signal_handler)
    app.run(port=5000, debug=False)

# Working on Heroku without DB interactions
# port = int(os.environ.get("PORT", 5001))
# app.run(host='0.0.0.0', port=port)