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

from flask import abort, g, json

from flask_app import app, BASEPATH

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

@app.route( BASEPATH+'/events', methods=['GET'] )
@app.route( BASEPATH+'/event', methods=['GET'] )
def list_events():
	return json.jsonify(app.config['EVENT_LIST'])

# quick test
@app.route( BASEPATH+'/quick/' )
@app.route( BASEPATH+'/quick/<foo>' )
def quick_test(foo=None):
	app.logger.warning( 'quick_test:'+str(foo) )
	return 'foo'

# catch-all (mostly for debugging)
@app.route( '/<path:path>' )
def catch_all(path):
	app.logger.warning( 'BASEPATH is '+BASEPATH )
	return 'Bzzzt!  Thank you for playing ... %s' % path
