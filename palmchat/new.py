import psycopg2
from urllib.parse import urlparse

url = urlparse("postgres://default:AoPTF0naIv1d@ep-crimson-surf-51993475.ap-southeast-1.postgres.vercel-storage.com:5432/verceldb")

print(url.username)
print(url.password)

conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:],
    user=url.username,
    password=url.password
)
if(conn):
    print("connected to database succesfully")

cur=conn.cursor()

# cur.execute("SELECT * FROM users;")
# print(cur.fetchall())
# cur.execute("CREATE TABLE IF NOT EXISTS prompts(email varchar(100) REFERENCES users(email),prompt varchar(500) PRIMARY KEY,result varchar(1000));")

# cur.execute("INSERT INTO prompts VALUES('rohan12@gmail.com','hello','hi how are you');")

cur.execute("SELECT * FROM users;")
print(cur.fetchall())
cur.execute("SELECT * FROM prompts;")
print(cur.fetchall())

conn.commit()
cur.close()
conn.close()