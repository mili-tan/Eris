import os

from flask import Flask, jsonify

import MDns.DnsQuery
import MDns.DnsSpoofCheck
import MPing.ICMPing
import MPing.TCPing
import MRoute.TCPTrace
import MRoute.Trace

app = Flask(__name__)
wsgi_app = app.wsgi_app


@app.route("/")
def hello_world():
    return "<p>Welcome to Eris!</p>"


@app.route('/dns/query/<name>')
def DNSQuery(name):
    return jsonify(MDns.DnsQuery.Query(name))


@app.route('/dns/check/<name>')
def DNSCheck(name):
    return jsonify(MDns.DnsSpoofCheck.Check(name))


@app.route('/route/trace/<ip>')
def RouteTrace(ip):
    return jsonify(MRoute.Trace.Trace(ip))


@app.route('/route/trace/<ip>/<port>')
def TCPRouteTrace(ip, port):
    return jsonify(MRoute.TCPTrace.Trace(ip, int(port)))


@app.route('/ping/icmp/<ip>')
def ICMPing(ip):
    return jsonify(MPing.ICMPing.Ping(ip))


@app.route('/ping/tcp/<ip>/<port>')
def TCPing(ip, port):
    return jsonify(MPing.TCPing.Ping(ip, int(port)))


if __name__ == '__main__':
    print('Welcome to Eris')
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '2025'))
    except ValueError:
        PORT = 2025
    app.run(HOST, PORT)
