# import psycopg2
from urllib.parse import urlparse
import sqlite3

def connect():
    # url = urlparse("postgres://default:AoPTF0naIv1d@ep-crimson-surf-51993475.ap-southeast-1.postgres.vercel-storage.com:5432/verceldb")

    # print(url.username)
    # print(url.password)

    # conn = psycopg2.connect(
    #     host=url.hostname,
    #     port=url.port,
    #     database=url.path[1:],
    #     user=url.username,
    #     password=url.password
    # )
    # if(conn):
    #     print("connected to database succesfully")

    # return conn

    conn = sqlite3.connect('database.db')
    return conn
