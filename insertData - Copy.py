import requests, mysql.connector, os
from mysql.connector import Error

# Global connection object
connection = mysql.connector.connect(host='localhost',
                                     database='DcCovidData_Copy',
                                     user='root',
                                     password=os.environ.get("Pass"))

url = "https://corona.lmao.ninja/v2/states?sort&yesterday"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()

for ele in response:
    try:
        cursor = connection.cursor()
        sql_insert_query = """INSERT INTO covidData values (%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql_insert_query, (ele["state"], ele["todayCases"], ele["active"], ele["recovered"], ele["todayDeaths"], ele["tests"]))
        connection.commit()
        print("Success")
    except Error as e:
        print("Error inserting data in MySQL table", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            # connection.close()
            print("MySQL connection is closed")