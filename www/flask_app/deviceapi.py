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

import uuid
import time
import requests
from flask import Flask, request, abort, g, json

from flask_app import app, BASEPATH, db, auth_required, AUTHLVL

# the app instance is created in __init__

# device generates a random code and posts it to the server
# server waits for user to confirm it
@app.route( BASEPATH+'/link/<in_code>', methods=['GET'] )
def test_device_token( in_code ):
	# returns true/false if someone has claimed the device-code
	# TODO: check that originating IP-addr is same?
	rtn = {}
	time_now = time.time()
	app.logger.warning( 'looking for devcode='+in_code )
	dcode = db.Devcode.get_or_none( db.Devcode.devcode==in_code )
	if( dcode == None ):
		rtn['info'] = 'no such device-code'
		rtn['status'] = 'error'
	else:
		time_created = dcode.time_create
		#app.logger.info( 'time='+str(time_now)+'-'+str(time_created)+'='+str(time_now-time_created)+'::'+str(app.config['DEVCODE_TIMEOUT']))
		if( (time_now-time_created) > app.config['DEVCODE_TIMEOUT'] ):
			rtn['info'] = 'device-code has expired'
			rtn['status'] = 'error'
			# TODO: delete this devcode
		elif( dcode.claimed ):
			rtn['info'] = 'device-code has been claimed'
			rtn['status'] = 'Ok'
		else:
			rtn['info'] = 'device-code is unclaimed'
			rtn['status'] = 'retry'
	return json.jsonify(rtn)

@app.route( BASEPATH+'/link/', methods=['POST'] )
def reg_device_code():
	rtn = {}
	if( 'authcode' in request.form ):
		# TODO: store originaing IP-addr in database too?
		in_devcode = request.form['authcode']
		time_now = time.time()
		app.logger.warning( 'registering dev-code='+in_devcode )
		dcode = db.Devcode.get_or_none( db.Devcode.devcode==in_devcode )
		if( dcode != None ):
			rtn['info'] = 'device-code already in use'
			rtn['status'] = 'retry'
		else:
			dcode = db.Devcode( devcode=in_devcode, claimed=False, time_create=time_now )
			dcode.save()
			rtn['info'] = 'device-code was registered'
			rtn['status'] = 'ok'
	else:
		rtn['info'] = 'no device-code given'
		rtn['status'] = 'error'
	return json.jsonify(rtn)

@app.route( BASEPATH+'/activate/<in_code>', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def claim_device_code( in_code ):
	# a user is claiming a device-code
	# TODO: allow user to name the device that will be attached to this device-key
	rtn = {}
	time_now = int(time.time())
	dcode = db.Devcode.get_or_none( db.Devcode.devcode==in_code )
	if( dcode != None ):
		if( dcode.claimed ):
			rtn['info'] = 'device-code already claimed'
			rtn['status'] = 'error'
		else:
			time_created = dcode.time_create
			#app.logger.info( 'time='+str(time_now)+'-'+str(time_created)+'='+str(time_now-time_created)+'::'+str(app.config['DEVCODE_TIMEOUT']))
			if( (time_now-time_created) > app.config['DEVCODE_TIMEOUT'] ):
				rtn['info'] = 'device-code has expired'
				rtn['status'] = 'error'
				# TODO: delete the devcode from db
			else:
				# TODO: this should be a transaction pair
				dcode.claimed = True
				dcode.save()
				new_uuid = uuid.uuid1().hex
				token = db.Token( token=new_uuid, user=g.auth_user, device_name="foo", time_create=time_now )
				token.save()
				rtn['info'] = 'device-code is now claimed'
				rtn['token'] = new_uuid
				rtn['status'] = 'ok'
	else:
		rtn['info'] = 'invalid device-code'
		rtn['status'] = 'error'
	return json.jsonify(rtn)
