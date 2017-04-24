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

import os
import requests

BASEURL = 'http://localhost:5000/'
if( 'BASEURL' in os.environ ):
	BASEURL = os.environ['BASEURL']

#
# add some subscriptions
#
print "Creating 3 subscriptions ..."
r1 = requests.post( BASEURL, auth=('baba','babababa'),
	data={'event':'button', 'target_url':'http:://a.com'} )
print r1.text
r2 = requests.post( BASEURL, auth=('baba','babababa'),
	data={'event':'key', 'target_url':'http:://b.com'} )
print r2.text
r3 = requests.post( BASEURL, auth=('oona','oonaoona'),
	data={'event':'button', 'target_url':'http:://c.com'} )
print r3.text

#
# some useful variables
r1json = r1.json()
r2json = r2.json()
r3json = r3.json()

#
# try to delete a subscription
print "Creating and Deleting a subscription ..."
r1d = requests.post( BASEURL, auth=('baba','babababa'),
	data={'event':'button', 'target_url':'http:://a.com'} )
print r1d.text
r1djson = r1d.json()
r1dd = requests.delete( BASEURL+r1djson['subid'], auth=('baba','babababa') )
print r1dd.text
print "  is it gone? ..."
r1dd = requests.get( BASEURL+r1djson['subid'], auth=('baba','babababa') )
print r1dd.text
print "  try to delete again ..."
r1dd = requests.delete( BASEURL+r1djson['subid'], auth=('baba','babababa') )
print r1dd.text

#
# get all subscr for a user
print "Get all subscriptions for a user ..."
r = requests.get( BASEURL, auth=('baba','babababa') )
print r.text
print "Get all subscriptions for a user (full data) ..."
r = requests.get( BASEURL+"listfull", auth=('baba','babababa') )
print r.text

# read the specific sub-id that was returned
print 'Reading subscr-id from another user (should fail) ...'
# try to read other user's subscription (should fail)
r = requests.get( BASEURL+r1json['subid'], auth=('oona','oonaoona') )
print r.text

# read the specific sub-id that was returned
print 'Update subscr-id with new url ...'
# try to read other user's subscription (should fail)
r = requests.put( BASEURL+r1json['subid'], auth=('baba','babababa'),
 	data={'event':'button','target_url':'http://x.com'} )
print r.text
r = requests.get( BASEURL+r1json['subid'], auth=('baba','babababa') )
print r.text

#
# get all subscr for a user
print "Get all subscriptions for a user+event ..."
r = requests.get( BASEURL+'event/button', auth=('baba','babababa') )
print r.text
