from flask import Flask

app = Flask(__name__)


@app.route('/greet/<name>')
def greet_visitor(name):
	return f"Hello {name}\r\n"


@app.route('/')
def hello_world():
	return "Hello PyNash!\r\n"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

