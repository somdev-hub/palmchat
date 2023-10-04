import flask
import flask_login
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user
from werkzeug.security import check_password_hash, generate_password_hash
import palm
from database import database
from User import User


app = flask.Flask(__name__)
mysql = database()


try:

    cur = mysql.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")
    cur.execute("CREATE TABLE IF NOT EXISTS prompts (id INT AUTO_INCREMENT PRIMARY KEY, prompt VARCHAR(1000), result VARCHAR(5000), user VARCHAR(255))")
    mysql.commit()
except Exception as e:
    print(e)


app.secret_key = 'super secret string'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # print(user_id)
    cur.execute("SELECT * FROM users WHERE email=%s;", (user_id,))
    user = cur.fetchone()
    # print(user)
    # conn.commit()
    return User.get(user)


@app.route('/', methods=['GET'])
# @login_required
def index():
    if flask_login.current_user.is_authenticated:
        email = current_user.email
        try:
            cur.execute("SELECT * FROM prompts WHERE user=%s;", (email,))
            prompts = cur.fetchall()
            # print(type(prompts[0][0]))
            # print(prompts)
        except Exception as e:
            print(e)
        return flask.render_template('index.html', prompts=prompts)
    else:
        # User is not logged in
        return flask.redirect('/login')


@app.route('/search/<int:id>', methods=['GET'])
def search(id):
    if flask_login.current_user.is_authenticated:
        email = current_user.email
        try:
            cur.execute(
                "SELECT * FROM prompts WHERE user=%s AND id=%s;", (email, id,))
            getPrompt = cur.fetchone()
            # print(prompts)
            print(getPrompt)
        except Exception as e:
            print(e)
        return flask.Response(response=getPrompt[2], status=200, mimetype='text/plain')
        # return flask.render_template('index.html', getPrompt=getPrompt[2])

    else:
        # User is not logged in
        return flask.redirect('/login')


@app.route('/signup', methods=['GET'])
def signup():
    return flask.render_template('signup.html')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return flask.redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    elif flask.request.method == 'POST':
        email = flask.request.form['email']
        print(email)
        password = flask.request.form['password']
        # user = authenticate_user(email, password)
        try:
            cur.execute("SELECT * FROM users WHERE email=%s;", (email,))
            user = cur.fetchone()
        except Exception as e:
            print(e)
        if user:
            if check_password_hash(user[3], password):
                # login_user(User(uid=user, email=email))
                login_user(User(email=email, password=password, name=user[1]))
                return flask.redirect('/')
            else:
                return flask.Response(response="incorrect email or password", status=200, mimetype='text/plain')
        else:
            return flask.Response(response="incorrect email or password", status=200, mimetype='text/plain')


@app.route('/signup', methods=['POST'])
def signup_post():

    name = flask.request.form['name']
    email = flask.request.form['email']
    password = flask.request.form['password']
    # print(name)
    # print(email)
    # print(password)
    try:
        cur.execute("SELECT * FROM users WHERE email=%s;", (email,))
        user = cur.fetchone()

    # user = create_user(email, password, name)
        if user:
            return flask.Response(response="user already exists", status=200, mimetype='text/plain')
        else:
            try:
                cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s);",
                            (name, email, generate_password_hash(password)))
                mysql.commit()
            except Exception as e:
                print(e)
            # print("user created")
            # print(user)
            # login_user(User(uid=user, email=email))
            # return flask.Response(response="user created", status=200, mimetype='text/plain')
            login_user(User(email=email, password=password, name=name))
            return flask.redirect('/')
    except Exception as e:
        print(e)
        return flask.Response(response="something went wrong! Please try again", status=500, mimetype='text/plain')


@app.route('/prompt', methods=['POST'])
def prompt():
    prompt = flask.request.form['prompt']
    # print(flask.request.form["prompt"])
    response = palm.chat(messages=prompt)
    if current_user.is_authenticated:
        email = current_user.email
        try:
            cur.execute(
                "select * from prompts where user=%s and prompt=%s;", (email, prompt,))
            object = cur.fetchone()
            if object:
                cur.execute(
                    "UPDATE prompts SET result=%s WHERE prompt=%s AND user=%s;", (response, prompt, email,))
                mysql.commit()
            else:
                cur.execute("INSERT INTO prompts (prompt, result, user) VALUES (%s, %s, %s);",
                            (prompt, response, email))
                mysql.commit()
        except Exception as e:
            print(e)

    return flask.Response(response=response, status=200, mimetype='text/plain')


@app.route('/message', methods=['GET'])
def message():
    prompt = flask.request.args.get('prompt')
    # print(prompt)
    return flask.render_template('message.html', prompt=prompt)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.142.254', port='5000')
    # cur.close()
    # conn.close()
