import mysql.connector
import datetime
from mysql.connector import Error
from .configuration import DB, DB1, locksDB

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
        sql_insert_query = """INSERT INTO covidData values (%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql_insert_query, (response["state"], response["todayCases"], response["active"], response["recovered"], response["todayDeaths"], response["tests"]))
        print("Success1")
    except Error as e:
        print("Error inserting data in MySQL table, DB1", e)

    try:
        cursor1 = connection.cursor()
        sql_insert_query = """INSERT INTO covidData values (%s,%s,%s,%s,%s,%s)"""
        cursor1.execute(sql_insert_query, (response["state"], response["todayCases"], response["active"], response["recovered"], response["todayDeaths"], response["tests"]))
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

def acquireLock():
    pass

def checkLockStatus():
    try:
        cursor = connection.cursor(dictionary=True)
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

def releaseLock():
    pass