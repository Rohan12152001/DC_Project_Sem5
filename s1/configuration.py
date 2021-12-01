import os

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