import mysql.connector
import datetime
from mysql.connector import Error
from .configuration import DB

""" Database manager """

# Global connection object
connection = mysql.connector.connect(host=DB.host,
                                     database=DB.database,
                                     user=DB.user,
                                     password=DB.password)

# Triggered when server shut down
def close():
    if connection.is_connected():
        print("Closing connection !")
        connection.close()

def fetchArticles():
    try:
        cursor = connection.cursor(dictionary=True)
        sql_fetch_query = "select * from blogs order by uploadDate DESC"
        cursor.execute(sql_fetch_query)
        records = cursor.fetchall()
        # print(records)
        # print(len(records))
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            # connection.close()
            print("MySQL connection is closed")

    return records

def fetchOneArticle(articleId):
    try:
        cursor = connection.cursor(dictionary=True)
        sql_fetch_query = "select * from blogs where blogId=%s"
        cursor.execute(sql_fetch_query, (articleId,))
        records = cursor.fetchone()
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

def fetchAuthorDetails(userId):
    try:
        cursor = connection.cursor(dictionary=True)
        sql_fetch_query = "select * from users where userid=%s"
        cursor.execute(sql_fetch_query, (userId,))
        records = cursor.fetchone()
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

def insertBlog(response):
    try:
        cursor = connection.cursor()
        sql_insert_query = """INSERT INTO blogs values (%s,%s,%s,NOW(),%s,%s)"""
        cursor.execute(sql_insert_query, (str(response["blogId"]), response["userId"], response["title"], response["blogData"], response["imgUrl"]))
        connection.commit()
        print("Success")
    except Error as e:
        print("Error inserting data in MySQL table", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            # connection.close()
            print("MySQL connection is closed")
    return True