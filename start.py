from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app

print('Eris API Running')
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(2025)
IOLoop.instance().start()
