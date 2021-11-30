import os

class DB:
    host = 'localhost'
    database = 'CricStats'
    user = 'root'
    password = os.environ.get("Pass")
    secretKey = 'super secret key'