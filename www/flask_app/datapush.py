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
import sqlite3
import requests
from flask import Flask, request, abort, g, json

from flask_app import app, BASEPATH, db, auth_required, AUTHLVL

# the app instance is created in __init__

#
# push the data to the subscription service (e.g. Zapier)
def _int_push_data( a_event, a_user, a_data ):
	app.logger.info( 'data-push '+a_event+' on behalf of userid='+a_user )
	# TODO: this changes rtn from hash to list!
	rtn = []
	out_data = { 'event':a_event, 'timestamp':int(time.time()), 'button':a_data }
	try:
		dbc = db.get_db()
		for row in dbc.execute( 'select * from SubsDB where event=? and userid=?', [a_event,a_user] ):
			rtn.append( { 'subid':row['subid'], 'userid':row['userid'], 'target_url':row['target_url'] } )
			# TODO: DO THE PUSH
			app.logger.info( 'push data to subscription: '+row['subid']+','+row['target_url'] )
			r = requests.post( row['target_url'], json=out_data )
			# TODO: "If Zapier responds with a 410 status code you should immediately remove the subscription to the failing hook (unsubscribe)."
	except:
		rtn['info'] = 'database error'
	return rtn

@app.route( BASEPATH+'/data/<in_event>', methods=['POST'] )
@auth_required( AUTHLVL.DEVICE )
def push_data( in_event ):
	rtn = { 'info':'unknown error', 'status':'error' }
	data = None
	if( request.json != None ):
		if( 'button' in request.json ):
			data = request.json['button']
	if( request.form != None ):
		if( 'button' in request.form ):
			data = request.form['button']
	if( in_event in app.config['EVENT_LIST'] ):
		authuser = g.token_userid
		rtn = _int_push_data( in_event, authuser, data )
	return json.jsonify(rtn)

@app.route( BASEPATH+'/data/', methods=['POST'] )
@auth_required( AUTHLVL.DEVICE )
def push_data_general():
	rtn = { 'info':'unknown error', 'status':'error' }
	event = None
	data = None
	if( request.json != None ):
		if( 'event' in request.json ):
			event = request.json['event']
		if( 'button' in request.json ):
			data = request.json['button']
	if( request.form != None ):
		if( 'event' in request.form ):
			event = request.form['event']
		if( 'button' in request.form ):
			data = request.form['button']
	if( not event in app.config['EVENT_LIST'] ):
		# TODO: customize the error to indicate bad event name
		event = None

	if( (event != None) and (data != None) ):
		authuser = g.token_userid
		rtn = _int_push_data( event, authuser, data )
	else:
		rtn = { 'info':'insufficient data', 'status':'error' }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/last/', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def get_last_event():
	rtn = [{ 'event':'button', 'button':1, 'timestamp':0 }]
	return json.jsonify( rtn )
