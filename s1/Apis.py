from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import mysql.connector, sys, os, webbrowser
import requests, signal, time
from mysql.connector import Error

################### CONFIG ###################
class DB:
    host = 'localhost'
    database = 'DcCovidData'
    user = 'root'
    password = os.environ.get("Pass")
    secretKey = 'super secret key'

class DB1:
    host = 'localhost'
    database = 'DcCovidData_Copy'
    user = 'root'
    password = os.environ.get("Pass")
    secretKey = 'super secret key'

class locksDB:
    host = 'localhost'
    database = 'lockDB'
    user = 'root'
    password = os.environ.get("Pass")
    secretKey = 'super secret key'
################### CONFIG END ###################

################### DAO ###################
""" Database manager """
# Global connection objects

# DB1
connection = mysql.connector.connect(host=DB.host,
                                     database=DB.database,
                                     user=DB.user,
                                     password=DB.password)
# DB2
connection1 = mysql.connector.connect(host=DB1.host,
                                     database=DB1.database,
                                     user=DB1.user,
                                     password=DB1.password)

# locksDB
lockDBconnection = mysql.connector.connect(host=locksDB.host,
                                     database=locksDB.database,
                                     user=locksDB.user,
                                     password=locksDB.password)

# Triggered when server shut down
def close():
    if connection.is_connected():
        print("Closing connection !")
        connection.close()

def insertData(response):
    # insert data into two DB's for backup purpose
    try:
        cursor = connection.cursor()
        # sql_insert_query = """INSERT INTO covidData values (%s,%s,%s,%s,%s,%s)"""
        sql_insert_query = """UPDATE covidData SET casesToday = %s, activeCases = %s, recovered = %s, deathsToday = %s, totalTests = %s WHERE state=%s;"""
        cursor.execute(sql_insert_query, (response["todayCases"], response["active"], response["recovered"], response["todayDeaths"], response["tests"], response["state"]))
        print("Success1")
    except Error as e:
        print("Error inserting data in MySQL table, DB1", e)

    try:
        cursor1 = connection1.cursor()
        # sql_insert_query = """INSERT INTO covidData values (%s,%s,%s,%s,%s,%s)"""
        # cursor1.execute(sql_insert_query, (response["state"], response["todayCases"], response["active"], response["recovered"], response["todayDeaths"], response["tests"]))
        sql_insert_query = """UPDATE covidData SET casesToday = %s, activeCases = %s, recovered = %s, deathsToday = %s, totalTests = %s WHERE state=%s;"""
        cursor1.execute(sql_insert_query, (response["todayCases"], response["active"], response["recovered"], response["todayDeaths"], response["tests"], response["state"]))
        print("Success2")
    except Error as e:
        print("Error inserting data in MySQL table, DB2", e)

    if connection.is_connected() and connection1.is_connected():
        connection.commit()
        connection1.commit()
        cursor.close()
        cursor1.close()
        # connection.close()
        print("MySQL connection is closed")
    return True

def getAllData():
    try:
        cursor = connection.cursor(dictionary=True)
        sql_fetch_query = "select * from covidData order by state ASC"
        cursor.execute(sql_fetch_query)
        records = cursor.fetchall()
        # print(records)
        # print(len(records))
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            cursor.close()
            # connection.close()
            print("MySQL connection is closed")
    return records

def acquireLock():
    try:
        cursor = lockDBconnection.cursor()
        sql_insert_query = """UPDATE locks SET lockStatus = 1;"""
        cursor.execute(sql_insert_query,)
        print("Lock Success")
    except Error as e:
        print("Error inserting data in MySQL table, locksDB", e)
    finally:
        lockDBconnection.commit()
        cursor.close()
        # connection.close()
        print("MySQL connection is closed")
        return True

def checkLockStatus():
    try:
        cursor = lockDBconnection.cursor(dictionary=True)
        sql_fetch_query = "select * from locks"
        cursor.execute(sql_fetch_query,)
        records = cursor.fetchone()
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            cursor.close()
            # connection.close()
            print("MySQL connection is closed")
    return records

def releaseLock():
    try:
        cursor = lockDBconnection.cursor()
        sql_insert_query = """UPDATE locks SET lockStatus = 0;"""
        cursor.execute(sql_insert_query, )
        print("Lock Released")
    except Error as e:
        print("Error inserting data in MySQL table, locksDB", e)
    finally:
        lockDBconnection.commit()
        cursor.close()
        # connection.close()
        print("MySQL connection is closed")
        return True

################### DAO  END ###################

# from flask_mysqldb import MySQL

app = Flask(__name__, static_url_path='/templates/static')


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
    records = getAllData()
    finalResponse = []

    for ele in records:
        finalData = {"state": ele["state"],
                     "todayCases": ele["casesToday"],
                     "activeCases": ele["activeCases"],
                     "recovered": ele["recovered"],
                     "todayDeaths": ele["deathsToday"],
                     "tests": ele["totalTests"]
                     }
        finalResponse.append(finalData)
    return render_template('blog_form.html', states=finalResponse)

# POST DATA
@app.route('/app/data', methods=["POST"])
def insert_data():
    # acquire lock
    attemptCounter = 0
    while True and attemptCounter<100:
        # if a TRUE then acqiure in Transac
        if not checkLockStatus()["lockStatus"]:
            acquireLock()
            break
        # else wait for 3 and try again
        attemptCounter += 1
        time.sleep(3)

    # form response if LOCK ACQUIRED
    response = {
        "state": str(request.form["state"]),
        "todayCases": request.form["todayCases"],
        "active": request.form["active"],
        "recovered": request.form["recovered"],
        "todayDeaths": request.form["todayDeaths"],
        "tests": request.form["tests"],
    }

    # insert data into DB
    done = insertData(response)

    # release lock
    releaseLock()

    return redirect(url_for('home_page'))

# Statewise page
@app.route('/app/statewise')
def stateWise_page():
    records = getAllData()
    finalResponse = []

    for ele in records:
        finalData = {"state": ele["state"],
                     "todayCases": ele["casesToday"],
                     "activeCases": ele["activeCases"],
                     "recovered": ele["recovered"],
                     "todayDeaths": ele["deathsToday"],
                     "tests": ele["totalTests"]
                     }
        finalResponse.append(finalData)

    return render_template('state_wise.html', states=finalResponse)

if __name__ == '__main__':
    app.secret_key = "super secret key"
    # signal to close the DB connection
    signal.signal(signal.SIGINT, signal_handler)
    app.run(port=50000, debug=False)