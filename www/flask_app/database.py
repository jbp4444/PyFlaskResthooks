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

from flask import g
from peewee import *

from flask_app import app

db = SqliteDatabase('db.db')

class BaseDB(Model):
	class Meta:
		database = db

class User(BaseDB):
	username    = CharField( unique=True )
	password    = CharField()
	permissions = IntegerField()

class Subscription(BaseDB):
	user       = ForeignKeyField(User)
	event      = CharField( index=True )
	target_url = CharField()

class Token(BaseDB):
	token = CharField( unique=True )
	user  = ForeignKeyField(User)
	device_name = CharField()
	# TODO: could/should be a TimestampField
	time_create = IntegerField()

class Devcode(BaseDB):
	devcode = CharField( unique=True )
	claimed = BooleanField()
	# TODO: could/should be a TimestampField
	time_create = IntegerField()


# Connect to our database.
db.connect()
# alt: db.connect(reuse_if_open=True)

# split the create-tables calls out separately, for debugging
db.create_tables([Subscription])
db.create_tables([User])
db.create_tables([Token])
db.create_tables([Devcode])


@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	db.close()

# # # # # # # # # # # # # # # # # # # # #
## # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # #

# TODO: remove this prior to production!!
if( User.get_or_none( User.username=='mossy') == None ):
	User(username='mossy',password='mossymossy',permissions=7).save()
if( User.get_or_none( User.username=='oona') == None ):
	User(username='oona',password='oonaoona',permissions=3).save()
if( User.get_or_none( User.username=='baba') == None ):
	User(username='baba',password='babababa',permissions=1).save()

import time
dc = Devcode.get_or_none( Devcode.devcode=='001122')
if( dc != None ):
	dc.delete_instance()
Devcode(devcode='001122',claimed=False,time_create=time.time()).save()
