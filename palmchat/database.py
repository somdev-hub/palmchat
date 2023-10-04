import pymysql
# from app import app


def database():
    conn = pymysql.connect(host='sql12.freesqldatabase.com',
                           user='sql12651008',
                           password='UuMe5ED6qJ',
                           db='sql12651008',
                           charset='utf8mb4',
                           )
    if(conn):
        print("Connected to database")

    return conn
