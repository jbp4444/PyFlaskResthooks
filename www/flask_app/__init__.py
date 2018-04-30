"""
Py-Resthook demo

Copyright (C) 2017-2018 - John Pormann, Duke University Libraries

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

https://opensource.org/licenses/MIT

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
	EVENT_LIST = [ 'button', 'key' ],
	DEVCODE_TIMEOUT = 3600,
	TOKEN_TIMEOUT = 3600
))
#app.config.from_envvar( 'HOOKS_CONFIG', silent=True )

# simple permissions model for "higher-level" functions
# database holds an integer 'permissions' field, which is bitwise-and of:
class AUTHLVL:
	NONE = 0
	# "standard" user auth levels
	USER = 1
	ADMIN = 10

import database as db
from userauth import auth_required

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
BASEPATH = '/pyhk'
#BASEPATH = ''

import baseapi
import api
import deviceapi
import datapush
import admin
import webui
