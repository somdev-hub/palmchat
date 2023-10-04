import pymysql
# from app import app


def database():
    conn = pymysql.connect(host='up-pl-waw1-mysql-1.db.run-on-erla.com',
                           user='db-6uam1x6qimas',
                           password='mGPZX4s4yw22vWhy06Zl0CGC',
                           db='palmchat',
                           charset='utf8mb4',
                           )
    if(conn):
        print("Connected to database")

    return conn
