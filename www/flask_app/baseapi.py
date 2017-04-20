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
from flask import Flask, request, abort, g, json

from flask_app import app, BASEPATH, db, auth_required, AUTHLVL

# the app instance is created in __init__


@app.errorhandler( 400 )
def handle_bad_req(e):
	return json.jsonify( {'status':400, 'info':'bad request'} ), 400
@app.errorhandler( 401 )
def handle_bad_auth(e):
	return json.jsonify( {'status':401, 'info':'authentication failure'} ), 401

@app.route( BASEPATH+'/help', methods=['GET'] )
def show_endpoints():
	rtn = [ {'endpoint': '/', 'verb':'GET', 'info':'list a user\'s subscrtiptions'},
		{'endpoint':'/', 'verb':'POST', 'info':'create a new subscription'},
		{'endpoint':'/<subid>', 'verb':'GET', 'info':'show info for given subscription-id'},
		{'endpoint':'/<subid>', 'verb':'PUT', 'info':'update an existing subscription'},
		{'endpoint':'/<subid>', 'verb':'DELETE', 'info':'delete an existing subscription'},
		{'endpoint':'/event', 'verb':'GET', 'info':'list known event types'},
		{'endpoint':'/event/<evtname>', 'verb':'GET', 'info':'list a user\'s subscriptions for that event'},
		{'endpoint':'/data/<evtname>', 'verb':'POST', 'info':'post data for a given event'} ]
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/devcodes', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_devcodes_full():
	rtn = {}
	try:
		dbc = db.get_db()
		for row in dbc.execute( 'select * from DevcodeDB' ):
			rtn[row['devcode']] = {'userid':row['userid'],'claimed':row['claimed'],'time_create':row['time_create']}
	except:
		rtn['info'] = 'error in database query'
		rtn['status'] = 'error'
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/tokens', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_tokens_full():
	rtn = {}
	try:
		dbc = db.get_db()
		for row in dbc.execute( 'select * from TokenDB' ):
			rtn[row['token']] = {'userid':row['userid'],'device_name':row['device_name'],'time_create':row['time_create']}
	except:
		rtn['info'] = 'error in database query'
		rtn['status'] = 'error'
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/users', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_users_full():
	rtn = {}
	try:
		dbc = db.get_db()
		for row in dbc.execute( 'select * from UserDB' ):
			rtn[row['userid']] = {'username':row['username'],'permissions':row['permissions']}
	except:
		rtn['info'] = 'error in database query'
		rtn['status'] = 'error'
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/subs', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_subs_full():
	rtn = {}
	try:
		dbc = db.get_db()
		for row in dbc.execute( 'select * from SubsDB' ):
			rtn[row['subid']] = {'userid':row['userid'],'event':row['event'],'target_url':row['target_url']}
	except:
		rtn['info'] = 'error in database query'
		rtn['status'] = 'error'
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/events', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_events():
	rtn = app.config['EVENT_LIST']
	return json.jsonify(rtn)

@app.route( BASEPATH+'/admin/events/<in_event>', methods=['GET'] )
@auth_required( AUTHLVL.ADMIN )
def admin_list_event_data( in_event ):
	rtn = {}
	try:
		dbc = db.get_db()
		for row in dbc.execute( 'select * from SubsDB where event=?', [in_event] ):
			rtn[row['subid']] = {'userid':row['userid'],'event':row['event'],'target_url':row['target_url']}
	except:
		rtn['info'] = 'error in database query'
		rtn['status'] = 'error'
	return json.jsonify(rtn)

# catch-all (mostly for debugging)
@app.route( '/<path:path>' )
def catch_all(path):
	return 'Bzzzt!  Thank you for playing ... %s' % path
