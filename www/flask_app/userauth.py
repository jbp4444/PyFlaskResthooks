"""
The flask application package.

Copyright (C) 2017 - John Pormann, Duke University Libraries

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

import time
from functools import wraps
from flask import request, abort, g

from flask_app import app, db

# simple permissions model for "higher-level" functions
# database holds an integer 'permissions' field, which is bitwise-and of:
class AUTHLVL:
	USER = 1
	DEVELOPER = 2
	ADMIN = 4
	# devices use a token
	DEVICE = 128

# decorator function to test for permissions
def auth_required( auth_level ):
	def real_auth_decorator(view_function):
		@wraps(view_function)
		def wrapper(*args, **kwargs):
			if( auth_level < AUTHLVL.DEVICE ):
				# user auth (username,password)
				auth = request.authorization
				#app.logger.warning( 'auth tokens: '+str(auth) )
				if( auth != None ):
					#app.logger.error( 'found auth info:'+str(auth) )
					dbc = db.get_db()
					for row in dbc.execute( 'select * from UserDB where username=? and (permissions&?>0)', [auth.username,auth_level] ):
						app.logger.warning( 'auth: userid='+row['userid']+' '+row['username']+':'+row['password']+"::"+str(row['permissions']) )
						if( (row['username']==auth.username) and (row['password']==auth.password) ):
							g.auth_userid = row['userid']
							return view_function(*args,**kwargs)
			else:
				# device auth (token)
				if( 'X-Device-Token' in request.headers ):
					token = request.headers['X-Device-Token']
					app.logger.error( 'found auth token:'+token )
					time_now = time.time()
					dbc = db.get_db()
					for row in dbc.execute( 'select * from TokenDB where token=?', [token] ):
						app.logger.error( 'token tied to userid='+row['userid'] )
						time_created = row['time_create']
						if( (time_now-time_created) > app.config['TOKEN_TIMEOUT'] ):
							# device-token is too old
							abort(401)
						g.token = token
						g.token_userid = row['userid']
					return view_function(*args,**kwargs)
			abort(401)
		return wrapper
	return real_auth_decorator
