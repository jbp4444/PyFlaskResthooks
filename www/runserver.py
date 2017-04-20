"""
This script runs the flask_app application using a development server.
"""

from flask_app import app

if __name__ == '__main__':
	app.run( 'localhost', 5000 )
