import flask
import flask_login
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash
import palm
import database as database
from palmchat.app.User import User
from app import app

app.secret_key = 'super secret string'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = database.connect()
cur=conn.cursor()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/', methods=['GET'])
def index():
    if flask_login.current_user.is_authenticated:
        # User is logged in
        cur.execute("SELECT * FROM prompts;")
        prompts = cur.fetchall()
        print(prompts)
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
        cur.execute("SELECT * FROM users WHERE email=%s;", (email,))
        user = cur.fetchone()
        conn.commit()
        if user:
            if check_password_hash(user[2], password):
                login_user(User(email=user[0], password=user[2], name=user[1]))
                return flask.redirect('/')
            else:
                return flask.Response(response="incorrect email or password", status=200, mimetype='text/plain')
        else:
            return flask.Response(response="something went wrong", status=500, mimetype="text/plain")


@app.route('/signup', methods=['POST'])
def signup_post():

    name = flask.request.form['name']
    email = flask.request.form['email']
    password = flask.request.form['password']
    print(name)
    print(email)
    print(password)
    cur.execute("SELECT * FROM users WHERE email=%s;", (email,))
    user = cur.fetchone()

    if user:
        print(user)
        return flask.Response(response="email already exists", status=200, mimetype='text/plain')
    else:
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO users VALUES(%s,%s,%s);",
                    (email, name, hashed_password))
        conn.commit()

        user = User(email=email, password=hashed_password, name=name)
        login_user(user)
        return flask.redirect('/login')


@app.route('/prompt', methods=['POST'])
def prompt():
    prompt = flask.request.form['prompt']
    # print(flask.request.form["prompt"])
    response = palm.chat(messages=prompt)
    return flask.Response(response=response, status=200, mimetype='text/plain')


@app.route('/message', methods=['GET'])
def message():
    prompt = flask.request.args.get('prompt')
    # print(prompt)
    return flask.render_template('message.html', prompt=prompt)