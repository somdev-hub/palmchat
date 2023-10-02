from flask_login import UserMixin
import database as database

class User(UserMixin):
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
        self.id = email

    @staticmethod
    def get(email):
        conn = database.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s;", (email,))
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if user:
            return User(email=user[0], password=user[2], name=user[1])
        else:
            return None
