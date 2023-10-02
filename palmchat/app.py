import flask
import flask_login
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash
import palm
import database as database
from User import User
import firebase_admin
from firebase_admin import credentials
# from firebase_admin import db
from firebase_admin import firestore
from firebase_admin import auth
from flask_login import current_user
from firebase_admin.firestore import FieldFilter

cred = credentials.Certificate(
    './palmchat-a3122-firebase-adminsdk-54vz7-738bb1de9f.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


app = flask.Flask(__name__)

# from models import UserAccount, Prompt
# conn = database.connect()


# cur.execute("CREATE TABLE IF NOT EXISTS users(email varchar(100) PRIMARY KEY,name varchar(100) NOT NULL,password varchar(100) NOT NULL);")
# conn.commit()

app.secret_key = 'super secret string'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def create_user(email, password, name):
    user = auth.create_user(
        email=email,
        email_verified=False,
        password=password,
        display_name=name,
        disabled=False)
    return user.uid


def get_user(uid):
    user = auth.get_user(uid)
    return user


def authenticate_user(email, password):
    user = auth.get_user_by_email(email)
    if user and auth.verify_password(password, user.password_hash):
        return user.uid
    else:
        return None


@login_manager.user_loader
def load_user(uid):
    user = auth.get_user(uid)
    if user:
        return User(uid=user.uid, email=user.email)
    else:
        return None


@app.route('/', methods=['GET'])
def index():
    if flask_login.current_user.is_authenticated:
        # User is logged in
        # cur.execute("SELECT * FROM prompts;")
        # prompts = cur.fetchall()

        # prompts = Prompt.query.all()
        # print(prompts)
        if current_user.is_authenticated:
            user = auth.get_user(current_user.id)

            prompts = db.collection("prompts").where(
                filter=FieldFilter("user", "==", user.email)
            ).get()
            # print(prompts)
            # print(user.email)
            prompts = [prompt.to_dict() for prompt in prompts]
            # print(prompts)

        # prompts = [("hi", "hello"), ("how are you", "I am fine")]
            return flask.render_template('index.html', prompts=prompts)
    else:
        # User is not logged in
        return flask.redirect('/login')


@app.route('/signup', methods=['GET'])
def signup():
    return flask.render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    elif flask.request.method == 'POST':
        email = flask.request.form['email']
        password = flask.request.form['password']
        # cur.execute("SELECT * FROM users WHERE email=?;", (email,))
        # user = cur.fetchone()
        # conn.commit()

        user = authenticate_user(email, password)
        if user:
            login_user(User(uid=user, email=email))
            return flask.redirect('/')
        else:
            return flask.Response(response="incorrect email or password", status=200, mimetype='text/plain')

        # user = UserAccount.query.filter_by(email=email).first()

        # if user:
        #     # if check_password_hash(user[2], password):
        #     #     login_user(User(email=user[0], password=user[2], name=user[1]))
        #     #     return flask.redirect('/')
        #     if check_password_hash(user.password, password):
        #         login_user(
        #             User(email=user.email, password=user.password, name=user.name))
        #         return flask.redirect('/')
        #     else:
        #         return flask.Response(response="incorrect email or password", status=200, mimetype='text/plain')
        # else:
        #     return flask.Response(response="something went wrong", status=500, mimetype="text/plain")


@app.route('/signup', methods=['POST'])
def signup_post():

    name = flask.request.form['name']
    email = flask.request.form['email']
    password = flask.request.form['password']
    print(name)
    print(email)
    print(password)
    # cur.execute("SELECT * FROM users WHERE email=?;", (email,))
    # user = cur.fetchone()

    user = create_user(email, password, name)
    login_user(User(uid=user, email=email))
    return flask.redirect('/')

    # if user:
    #     print(user)
    #     return flask.Response(response="email already exists", status=200, mimetype='text/plain')
    # else:
    #     hashed_password = generate_password_hash(password)
    #     # cur.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?);",
    #     #             (email, name, hashed_password))
    #     # conn.commit()

    #     new_user = UserAccount(email=email, name=name,
    #                            password=hashed_password)
    #     db.session.add(new_user)
    #     db.session.commit()

    #     user = User(email=email, password=hashed_password, name=name)
    #     login_user(user)
    #     return flask.redirect('/login')


@app.route('/prompt', methods=['POST'])
def prompt():
    prompt = flask.request.form['prompt']
    # print(flask.request.form["prompt"])
    response = palm.chat(messages=prompt)
    if current_user.is_authenticated:
        user = auth.get_user(current_user.id)
        # ref=db.reference("prompts")
        # ref.push({
        #     "prompt":prompt,
        #     "response":response,
        #     "user":user.email
        # })
        db.collection("prompts").add({
            "prompt": prompt,
            "result": response,
            "user": user.email
        })
    return flask.Response(response=response, status=200, mimetype='text/plain')


@app.route('/message', methods=['GET'])
def message():
    prompt = flask.request.args.get('prompt')
    # print(prompt)
    return flask.render_template('message.html', prompt=prompt)


if __name__ == '__main__':
    app.run(debug=True,host='192.168.142.254',port='5000')
    # cur.close()
    # conn.close()
