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
				app.logger.warning( 'auth tokens: '+str(auth) )
				if( auth != None ):
					user = db.User.get_or_none( (db.User.username==auth.username) & (db.User.password==auth.password) )
					#app.logger.warning( 'found user info:'+str(user) )
					if( user != None ):
						g.auth_user   = user
						g.auth_userid = auth.username
						return view_function(*args,**kwargs)
			else:
				# device auth (token)
				if( 'X-Device-Token' in request.headers ):
					hdrtoken = request.headers['X-Device-Token']
					app.logger.warning( 'found auth token:'+hdrtoken )
					time_now = int(time.time())
					token = db.Token.get_or_none( db.Token.token==hdrtoken )
					if( token != None ):
						#app.logger.warning( 'token tied to userid='+row['userid'] )
						time_created = token.time_create
						if( (time_now-time_created) > app.config['TOKEN_TIMEOUT'] ):
							# device-token is too old
							abort(401)
						g.token = token
						g.token_user   = token.user
						g.token_userid = token.user.username
					return view_function(*args,**kwargs)
			abort(401)
		return wrapper
	return real_auth_decorator
