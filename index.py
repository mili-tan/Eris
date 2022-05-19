import os

from flask import Flask, jsonify, json
from pywebio.platform.flask import webio_view
from werkzeug.exceptions import HTTPException

from MPage import PingUI, IndexUI, DnsUI, TraceUI

from MNetwork import MRoute, MPing, MDns

app = Flask(__name__)

app.add_url_rule('/x/tcp-trace', 'tcp-trace', webio_view(TraceUI.tcp),
                 methods=['GET', 'POST', 'OPTIONS'])

app.add_url_rule('/x/icmp-trace', 'icmp-trace', webio_view(TraceUI.icmp),
                 methods=['GET', 'POST', 'OPTIONS'])

app.add_url_rule('/x/tcp-ping', 'tcp-ping', webio_view(PingUI.tcp),
                 methods=['GET', 'POST', 'OPTIONS'])

app.add_url_rule('/x/icmp-ping', 'icmp-ping', webio_view(PingUI.icmp),
                 methods=['GET', 'POST', 'OPTIONS'])

app.add_url_rule('/x/dns', 'dns', webio_view(DnsUI.mdns),
                 methods=['GET', 'POST', 'OPTIONS'])

app.add_url_rule('/', 'index', webio_view(IndexUI.index),
                 methods=['GET', 'POST', 'OPTIONS'])

@app.route('/dns/query/<name>')
def DNSQuery(name):
    return jsonify(MDns.Dns(name).Query())


@app.route('/dns/check/<name>')
def DNSCheck(name):
    return jsonify(MDns.Dns(name).SpoofCheck())


@app.route('/route/trace/<ip>')
def RouteTrace(ip):
    return jsonify(MRoute.Trace(ip).ICMP())


@app.route('/route/trace/<ip>/<port>')
def TCPRouteTrace(ip, port):
    return jsonify(MRoute.Trace(ip, port=int(port)).TCP())


@app.route('/ping/icmp/<ip>')
def ICMPing(ip):
    return jsonify(MPing.Ping(ip).ICMP())


@app.route('/ping/tcp/<ip>/<port>')
def TCPing(ip, port):
    return jsonify(MPing.Ping(ip, port=int(port)).TCP())


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
