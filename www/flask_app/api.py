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

from flask import request, g, jsonify

from flask_app import app, BASEPATH, db, auth_required, AUTHLVL

# the app instance is created in __init__

# # # # # # # # # # # # # # # # # # # #

def list_subs( authuser ):
	rtn = []
	dbq = db.Subscription.select().where( db.Subscription.user==authuser )
	for row in dbq:
		rtn.append( row.id )
	if( len(rtn) == 0 ):
		rtn = { 'info':'could not get list','status':'error' }
	return rtn

@app.route( BASEPATH+'/', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def api_list_subs():
	return jsonify( list_subs(g.auth_user) )

# # # # # # # # # # # # # # # # # # # #

def list_subs_full( authuser ):
	rtn = { 'info':'unknown error', 'status':'error' }
	dbq = db.Subscription.select().where( db.Subscription.user==authuser )
	for row in dbq:
		rtn[row.id] = { 'event':row.event,'target_url':row.target_url }
	if( len(rtn) == 0 ):
		rtn = { 'info':'could not get list','status':'error' }
	return rtn

@app.route( BASEPATH+'/listfull', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def api_list_subs_full():
	return jsonify( list_subs_full(g.auth_user) )

# # # # # # # # # # # # # # # # # # # #

def get_subs( authuser, in_subid ):
	rtn = { 'info':'unknown error', 'status':'error' }
	sub = db.Subscription.get_or_none( (db.Subscription.user==authuser) & (db.Subscription.id==in_subid) )
	if( sub == None ):
		rtn = { 'info':'could not get subscription','status':'error' }
	else:
		rtn = {'event':sub.event,'target_url':sub.target_url}
	return rtn

@app.route( BASEPATH+'/<in_subid>', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def api_get_subs( in_subid ):
	return jsonify( get_subs(g.auth_user,in_subid) )

# # # # # # # # # # # # # # # # # # # #

def new_entry( authuser, event=None, target_url=None ):
	rtn = { 'info':'unknown error', 'status':'error' }
	if( not event in app.config['EVENT_LIST'] ):
		# TODO: customize the error to indicate bad event name
		event = None

	if( (event != None) and (target_url != None) ):
		newsub = db.Subscription( user=authuser, event=event, target_url=target_url )
		newsub.save()
		rtn = { 'subid':newsub.id,'info':'new subscription created','status':'ok' }
	else:
		rtn = { 'info':'insufficient information to create new subscription','status':'error' }
	return rtn

@app.route( BASEPATH+'/', methods=['POST'] )
@auth_required( AUTHLVL.USER )
def api_new_entry():
	event = None
	target_url = None
	if( request.json != None ):
		if( 'event' in request.json ):
			event = request.json['event']
		if( 'target_url' in request.json ):
			target_url = request.json['target_url']
	if( request.form != None ):
		if( 'event' in request.form ):
			event = request.form['event']
		if( 'target_url' in request.form ):
			target_url = request.form['target_url']
	return jsonify( new_entry(g.auth_user,event,target_url) )

# # # # # # # # # # # # # # # # # # # #

def del_entry( authuser, in_subid ):
	rtn = { 'info':'unknown error', 'status':'error' }
	sub = db.Subscription.get_or_none( (db.Subscription.user==authuser) & (db.Subscription.id==in_subid) )
	if( sub == None ):
		rtn = { 'info':'cannot delete subscription', 'status':'error' }
	else:
		sub.delete_instance()
		rtn = { 'subid':in_subid,'info':'subscription deleted','status':'ok' }
	return rtn

@app.route( BASEPATH+'/<in_subid>', methods=['DELETE'] )
@auth_required( AUTHLVL.USER )
def api_del_entry( in_subid ):
	return jsonify( del_entry(g.auth_user,in_subid) )

# # # # # # # # # # # # # # # # # # # #

def update_entry( authuser, in_subid, event=None, target_url=None ):
	rtn = { 'info':'unknown error', 'status':'error' }
	if( not event in app.config['EVENT_LIST'] ):
		# TODO: customize the error to indicate bad event name
		event = None

	if( (event != None) and (target_url != None) ):
		rtn = {}
		sub = db.Subscription.get_or_none( (db.Subscription.user==authuser) & (db.Subscription.id==in_subid) )
		if( sub != None ):
			if( event != None ):
				sub.event = event
			if( target_url != None ):
				sub.target_url = target_url
			sub.save()
			rtn = { 'subid':in_subid,'status':'ok' }
		else:
			rtn = { 'info':'subid not found','status':'error' }
	return rtn

@app.route( BASEPATH+'/<in_subid>', methods=['PUT'] )
@auth_required( AUTHLVL.USER )
def api_update_entry( in_subid ):
	event = None
	target_url = None
	if( request.json != None ):
		if( 'event' in request.json ):
			event = request.json['event']
		if( 'target_url' in request.json ):
			target_url = request.json['target_url']
	if( request.form != None ):
		if( 'event' in request.form ):
			event = request.form['event']
		if( 'target_url' in request.form ):
			target_url = request.form['target_url']
	return jsonify( update_entry(g.auth_user,in_subid,event,target_url) )

# # # # # # # # # # # # # # # # # # # #

def list_event( authuser, in_event ):
	rtn = { 'info':'unknown error', 'status':'error' }
	if( in_event in app.config['EVENT_LIST'] ):
		rtn = []
		dbq = db.Subscription.select().where( (db.Subscription.user==authuser) & (db.Subscription.event==in_event) )
		for row in dbq:
			rtn.append( row.id )
	else:
		rtn = { 'info':'event name not recognized', 'status':'error' }
	return rtn

@app.route( BASEPATH+'/event/<in_event>', methods=['GET'] )
@auth_required( AUTHLVL.USER )
def api_list_event( in_event ):
	return jsonify( list_event(g.auth_user,in_event) )
