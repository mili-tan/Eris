import os

from flask import Flask, jsonify, json
from pywebio.platform.flask import webio_view
from werkzeug.exceptions import HTTPException

import MDns.DnsQuery
import MDns.DnsSpoofCheck
import MPing
import MRoute.TCPTrace
import MRoute.Trace

import PingUI
import TraceUI

app = Flask(__name__)

app.add_url_rule('/x/trace', 'trace', webio_view(TraceUI.index),
                 methods=['GET', 'POST', 'OPTIONS'])

app.add_url_rule('/x/tcping', 'tcping', webio_view(PingUI.tcp),
                 methods=['GET', 'POST', 'OPTIONS'])

app.add_url_rule('/x/ping', 'ping', webio_view(PingUI.icmp),
                 methods=['GET', 'POST', 'OPTIONS'])


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
    return jsonify(MPing.Ping(ip).ICMPing())


@app.route('/ping/tcp/<ip>/<port>')
def TCPing(ip, port):
    return jsonify(MPing.Ping(ip, port=int(port)).TCPing())


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    print('Welcome to Eris')
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '2025'))
    except ValueError:
        PORT = 2025

    app.run(HOST, PORT)
