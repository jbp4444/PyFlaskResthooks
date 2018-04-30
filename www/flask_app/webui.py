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

from flask import g, render_template

import flask_app
from flask_app import app, BASEPATH, db, auth_required, AUTHLVL

@app.route( BASEPATH+'/hello' )
@auth_required( AUTHLVL.USER )
def webui_hello():
	return render_template( 'hello.html', name=g.auth_user.username )

@app.route( BASEPATH+'/showsubs')
@auth_required( AUTHLVL.USER )
def webui_showsubs():
	data = flask_app.api.list_subs_full( g.auth_user )
	return render_template( 'listsubs.html', data=data, name=g.auth_user.username )

@app.route( BASEPATH+'/showdevs')
@auth_required( AUTHLVL.USER )
def webui_showdevs():
	data = flask_app.deviceapi.list_tokens( g.auth_user )
	return render_template( 'listdevs.html', data=data, name=g.auth_user.username )

@app.route( BASEPATH+'/claim' )
@auth_required( AUTHLVL.USER )
def webui_claim_form():
	return render_template( 'claim.html', name=g.auth_user.username )

@app.route( BASEPATH+'/claimcode', methods=['POST'] )
@auth_required( AUTHLVL.USER )
def webui_claim_code():
	devcode = None
	if( 'devcode' in request.form ):
		devcode = request.form['devcode']
	app.logger.warning( 'devcode='+devcode )
	rtn = flask_app.deviceapi.claim_device_code( g.auth_user, devcode )
	app.logger.warning( 'devcode='+devcode+'  rtn='+str(rtn) )
	return render_template( 'claim_reply.html', claim_reply=rtn, name=g.auth_user.username )
