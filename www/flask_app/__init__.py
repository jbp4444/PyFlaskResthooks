"""
The flask application package.
"""

import os
import logging

from flask import Flask
app = Flask(__name__)

# load config settings
app.config.update( dict(
	DEBUG = 1,
	DATABASE = os.path.join(app.root_path,'db.db'),
	API_KEY = 'foobarbaz',
	EVENT_LIST = [ 'buttonpress', 'keypress' ],
	DEVCODE_TIMEOUT = 3600,
	TOKEN_TIMEOUT = 3600
))
#app.config.from_envvar( 'HOOKS_CONFIG', silent=True )

import database as db
from userauth import AUTHLVL, auth_required

# set up logging
logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('access.log')
logger.addHandler(handler)
app.logger.addHandler(handler)
app.logger.setLevel( 'DEBUG' )
app.logger.info( 'app starting up' )

# TODO: try to remove the leading path
#rt_cwd = os.getcwd()
#app.logger.warning( 'cwd='+rt_cwd )
#BASEPATH = '/pyhk'
BASEPATH = ''

import baseapi
import api
import deviceapi
