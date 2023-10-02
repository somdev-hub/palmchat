from flask_login import UserMixin
import database as database
# from app import UserAccount

class User(UserMixin):
    def __init__(self, uid, email):
        self.id = uid
        self.email = email
        
    @staticmethod
    def get(user):
        # cur.execute("SELECT * FROM users WHERE email=?;", (email,))
        # user = cur.fetchone()
        # conn.commit()
        # user = UserAccount.query.filter_by(email=email).first()
        if user:
            # return User(email=user[0], password=user[2], name=user[1])
            return User(email=user.email, password=user.password, name=user.name)
        else:
            return None
