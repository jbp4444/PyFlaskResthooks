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


@app.route( BASEPATH+'/', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def list_subs():
	authuser = g.auth_userid
	rtn = { 'info':'could not get list','status':'error' }
	try:
		rtn = []
		dbc = db.get_db()
		for row in dbc.execute( 'select subid from SubsDB where userid=?', [authuser] ):
			rtn.append( row['subid'] )
	except:
		# TODO: throw a 500 error?
		rtn = { 'info':'database error','status':'error' }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/listfull', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def list_subs_full():
	authuser = g.auth_userid
	rtn = {'info':'could not get list','status':'error' }
	try:
		dbc = db.get_db()
		for row in dbc.execute( 'select * from SubsDB where userid=?', [authuser] ):
			rtn[row['subid']] = {'event':row['event'],'target_url':row['target_url']}
	except:
		rtn = {'info':'database error','status':'error' }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/<in_subid>', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def get_subs( in_subid ):
	authuser = g.auth_userid
	rtn = { 'info':'could not get subscription','status':'error' }
	try:
		dbc = db.get_db()
		rtn = {}
		for row in dbc.execute( 'select * from SubsDB where subid=? and userid=?', [in_subid,authuser] ):
			rtn[row['subid']] = {'event':row['event'],'target_url':row['target_url']}
	except:
		rtn = { 'info':'database error','status':'error' }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/', methods=['POST'] )
@auth_required( AUTHLVL.USER )
def new_entry():
	rtn = { 'info':'unknown error', 'status':'error' }
	if( ('event' in request.form) and ('target_url' in request.form) ):
		if( request.form['event'] in app.config['EVENT_LIST'] ):
			authuser = g.auth_userid
			new_subid = uuid.uuid1().hex
			try:
				dbc = db.get_db()
				dbc.execute( 'insert into SubsDB values (?,?,?,?)',
							 [new_subid,authuser,request.form['event'],request.form['target_url']] )
				dbc.commit()
				rtn = { 'subid':new_subid,'info':'new subscription created','status':'ok' }
			except:
				# throw error code 500?
				#abort(500)
				rtn = { 'info':'database error','status':'error' }
		else:
			rtn = { 'info':'unknown event name','status':'error' }
	else:
		#abort( 400 )
		rtn = { 'info':'insufficient information to create new subscription','status':'error' }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/<in_subid>', methods=['DELETE'] )
@auth_required( AUTHLVL.USER )
def del_entry( in_subid ):
	rtn = { 'info':'unknown error', 'status':'error' }
	authuser = g.auth_userid
	try:
		dbc = db.get_db()
		dbc.execute( 'delete from SubsDB where subid=? and userid=?', [in_subid,authuser] )
		dbc.commit()
		# TODO: check if the delete actually worked?
		if( dbc.total_changes == 0 ):
			rtn = { 'info':'cannot delete subscription', 'status':'error' }
		else:
			rtn = { 'subid':in_subid,'info':'subscription deleted','status':'ok' }
	except:
		rtn = { 'info':'database error','status':'error' }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/<in_subid>', methods=['PUT'] )
@auth_required( AUTHLVL.USER )
def update_entry( in_subid ):
	rtn = { 'info':'unknown error', 'status':'error' }
	if( request.form['event'] in app.config['EVENT_LIST'] ):
		authuser = g.auth_userid
		rtn = {}
		try:
			dbc = db.get_db()
			dbc.execute( 'update SubsDB set event=?, target_url=? where subid=? and userid=?',
				[request.form['event'],request.form['target_url'],in_subid,authuser] )
			dbc.commit()
			rtn = { 'subid':in_subid,'status':'ok' }
		except:
			rtn = { 'info':'database error','status':'error' }
	else:
		rtn = { 'info':'event name not recognized','status':'error' }
	return json.jsonify(rtn)

@app.route( BASEPATH+'/event', methods=['GET'] )
def list_event_names():
	dbc = db.get_db()
	rtn = app.config['EVENT_LIST']
	return json.jsonify(rtn)

@app.route( BASEPATH+'/event/<in_event>', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def list_event( in_event ):
	rtn = { 'info':'unknown error', 'status':'error' }
	if( in_event in app.config['EVENT_LIST'] ):
		authuser = g.auth_userid
		# TODO: this changes rtn from hash to list!
		rtn = []
		try:
			dbc = db.get_db()
			for row in dbc.execute( 'select subid from SubsDB where event=? and userid=?', [in_event,authuser] ):
				rtn.append( row['subid'] )
		except:
			rtn = { 'info':'database error','status':'error' }
	else:
		rtn = { 'info':'event name not recognized', 'status':'error' }
	return json.jsonify(rtn)
