#!./env/bin/python

from flup.server.fcgi import WSGIServer
from flask_app import app

if __name__ == '__main__':
	WSGIServer(app).run()
