import pymysql
# from app import app


def database():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='india',
                           db='palmchat',
                           charset='utf8mb4',
                           )
    if(conn):
        print("Connected to database")

    return conn
