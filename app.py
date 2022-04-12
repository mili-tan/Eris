from flask import Flask

import MPing.ICMPing
import MPing.TCPing
import os

app = Flask(__name__)
wsgi_app = app.wsgi_app


@app.route("/")
def hello_world():
    return "<p>Welcome to Eris!</p>"


@app.route('/ping/icmp/<ip>')
def ICMPing(ip):
    return str(MPing.ICMPing.Ping(ip))


@app.route('/ping/tcp/<ip>/<port>')
def TCPing(ip, port):
    return str(MPing.TCPing.Ping(ip, int(port)))


if __name__ == '__main__':
    print('Welcome to Eris')
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '2025'))
    except ValueError:
        PORT = 2025
    app.run(HOST, PORT)
