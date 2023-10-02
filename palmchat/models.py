# from app import db

# class UserAccount(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True)
#     name = db.Column(db.String(100))
#     password = db.Column(db.String(100))

#     def __repr__(self):
#         return '<User %r>' % self.email


# class Prompt(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100))
#     prompt = db.Column(db.String(1000))
#     result = db.Column(db.String(1000))

#     def __repr__(self):
#         return '<Prompt %r>' % self.prompt
