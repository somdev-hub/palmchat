import flask
import palm

# print(palm.chat("hello"))

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def index():

    return flask.render_template('index.html')


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
# @app.route('/',methods=['POST'])
# def post():
#     return flask.render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
