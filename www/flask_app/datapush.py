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
import requests
from flask import request, g, jsonify

from flask_app import app, BASEPATH, db, auth_required, AUTHLVL

# the app instance is created in __init__

#
# push the data to the subscription service (e.g. Zapier)
def _int_push_data( a_user, a_event, a_data ):
	app.logger.info( 'data-push '+a_event+' on behalf of userid='+a_user.username )
	# TODO: this changes rtn from hash to list!
	rtn = []
	out_data = { 'event':a_event, 'timestamp':time.time(), 'button':a_data }
	dbq = db.Subscription.select().where( (db.Subscription.event==a_event) & (db.Subscription.user==a_user) )
	for row in dbq:
		rtn.append( { 'subid':row.id, 'username':row.user.username, 'target_url':row.target_url } )
		# TODO: DO THE PUSH
		app.logger.info( 'push data to subscription: '+str(row.id)+','+row.target_url )
		#r = requests.post( row['target_url'], json=out_data )
		# TODO: "If Zapier responds with a 410 status code you should immediately remove the subscription to the failing hook (unsubscribe)."
	return rtn

def push_data_general( authuser, event=None, data=None ):
	app.logger.warning( 'push-data-general '+str(event) )
	rtn = { 'info':'insufficient data', 'status':'error' }

	if( not event in app.config['EVENT_LIST'] ):
		# TODO: customize the error to indicate bad event name
		event = None

	if( (event != None) and (data != None) ):
		rtn = _int_push_data( authuser, event, data )
	return rtn

# NOTE: we ask for 'USER' level auth, but that should occur by
#   way of a x-device-token which we map to a user
@app.route( BASEPATH+'/data/<in_event>', methods=['POST'] )
@app.route( BASEPATH+'/data/', methods=['POST'] )
@auth_required( AUTHLVL.USER )
def api_push_data_general( in_event=None ):
	# TODO: need to clean this up; maybe define precedence of operations?
	if( request.json != None ):
		if( 'event' in request.json ):
			event = request.json['event']
		if( 'data' in request.json ):
			data = request.json['data']
	if( request.form != None ):
		if( 'event' in request.form ):
			event = request.form['event']
		if( 'data' in request.form ):
			data = request.form['data']
	if( in_event != None ):
		event = in_event
	return jsonify( push_data_general(g.auth_user,event,data) )

# # # # # # # # # # # # # # # # # # # #

# TODO: WARNING: this is a dummy placeholder for Zapier testing!
#   not clear if there is a better way to hack this; or is it a
#   useful thing to have in the API anyway?
@app.route( BASEPATH+'/last/', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def get_last_event():
	rtn = [{ 'event':'button', 'button':1, 'timestamp':0 }]
	return jsonify( rtn )
