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

import time
from functools import wraps
from flask import request, abort, g

from flask_app import app, db

# decorator function to test for permissions
def auth_required( auth_level ):
	def real_auth_decorator(view_function):
		@wraps(view_function)
		def wrapper(*args, **kwargs):
			g.token       = None
			g.auth_user   = None
			g.auth_userid = None

			app.logger.warning( 'trying to authenticate user' )

			# auth by login-form?
			if( ('username' in request.form) & ('password' in request.form) ):
				username = request.form['username']
				password = request.form['password']
				app.logger.warning( 'login-auth tokens: '+username+','+password )
				if( (username != None) and (password != None) ):
					user = db.User.get_or_none( (db.User.username==username) & (db.User.password==password) )
					#app.logger.warning( 'found user info:'+str(user) )
					if( user != None ):
						g.auth_user   = user
						g.auth_userid = username

			# auth by device auth (token)?
			elif( 'X-Device-Token' in request.headers ):
				hdrtoken = request.headers['X-Device-Token']
				app.logger.warning( 'found dev-auth token:'+hdrtoken )
				time_now = int(time.time())
				token = db.Token.get_or_none( db.Token.token==hdrtoken )
				if( token != None ):
					app.logger.warning( 'token tied to userid='+token.user.username )
					time_created = token.time_create
					#if( (time_now-time_created) > app.config['TOKEN_TIMEOUT'] ):
					#	# device-token is too old
					#	abort(401)
					g.token       = token
					g.auth_user   = token.user
					g.auth_userid = token.user.username

			# auth by http-basic-auth (username,password)?
			elif( request.authorization != None ):
				auth = request.authorization
				app.logger.warning( 'basic-auth tokens: '+str(auth) )
				if( auth != None ):
					user = db.User.get_or_none( (db.User.username==auth.username) & (db.User.password==auth.password) )
					#app.logger.warning( 'found user info:'+str(user) )
					if( user != None ):
						g.auth_user   = user
						g.auth_userid = auth.username

			#app.logger.warning( 'found user '+str(g.auth_user) )

			if( g.auth_user!=None ):
				app.logger.warning( 'found user '+str(g.auth_user)+','+g.auth_userid+','+str(g.auth_user.permissions)+';'+str(auth_level) )
				if( g.auth_user.permissions >= auth_level ):
					return view_function(*args,**kwargs)

			# else this was a bad auth attempt
			abort(401)
		return wrapper
	return real_auth_decorator
