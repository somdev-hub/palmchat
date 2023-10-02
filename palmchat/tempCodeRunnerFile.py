import database

conn = database.connect()

cur = conn.cursor()

cur.execute("select * from users;")
users = cur.fetchall()
for i in users:
    print(i)

# cur.execute("SELECT pg_get_serial_sequence('users', 'email')")
# sequence_name = cur.fetchone()[0]
# print(sequence_name)

conn.commit()



