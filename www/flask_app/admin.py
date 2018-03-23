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
from flask import abort, g, json

from flask_app import app, BASEPATH, db, auth_required, AUTHLVL

# the app instance is created in __init__

@app.route( BASEPATH+'/admin/devcodes', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_devcodes_full():
	rtn = {}
	dbq = db.Devcode.select()
	for row in dbq:
		rtn[row.id] = { 'devcode':row.devcode,'username':row.user.username,'claimed':row.claimed,'time_create':row.time_create }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/tokens', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_tokens_full():
	rtn = {}
	dbq = db.Token.select()
	for row in dbq:
		rtn[row.id] = { 'token':row.token,'username':row.user.username,'device_name':row.device_name,'time_create':row.time_create }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/users', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_users_full():
	rtn = {}
	dbq = db.User.select()
	for row in dbq:
		rtn[row.id] = { 'username':row.username,'permissions':row.permissions }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/subs', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_subs_full():
	rtn = {}
	dbq = db.Subscription.select()
	for row in dbq:
		rtn[row.id] = { 'userid':row.user,'event':row.event,'target_url':row.target_url }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/events/<in_event>', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_event_data( in_event ):
	rtn = {}
	dbq = db.Subscription.select().where( db.Subscription.event==in_event )
	for row in dbq:
		rtn[row.id] = { 'username':row.user.username,'event':row.event,'target_url':row.target_url }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/links', methods=['GET'] )
def clean_old_device_tokens():
	#app.logger.warning( 'cleaning devcodes' )
	rtn = {}
	time_now = int(time.time())
	n = 0
	dbq = db.Devcode.select()
	for row in dbq:
		time_created = row.time_create
		#app.logger.info( 'time='+str(time_now)+'-'+str(time_created)+'='+str(time_now-time_created)+'::'+str(app.config['DEVCODE_TIMEOUT']))
		if( (time_now-time_created) > app.config['DEVCODE_TIMEOUT'] ):
			n = n + 1
			row.delete_instance()

	rtn['info'] = 'device-codes were cleared'
	rtn['num'] = n
	rtn['status'] = 'ok'
	return json.jsonify(rtn)
