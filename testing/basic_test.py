#
#

import requests

BASEURL = 'http://localhost:5000/'

#
# add some subscriptions
#
print "Creating 3 subscriptions ..."
r1 = requests.post( BASEURL, auth=('baba','babababa'),
	data={'event':'buttonpress', 'target_url':'http:://a.com'} )
print r1.text
r2 = requests.post( BASEURL, auth=('baba','babababa'),
	data={'event':'keypress', 'target_url':'http:://b.com'} )
print r2.text
r3 = requests.post( BASEURL, auth=('oona','oonaoona'),
	data={'event':'buttonpress', 'target_url':'http:://c.com'} )
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
	data={'event':'buttonpress', 'target_url':'http:://a.com'} )
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
 	data={'event':'buttonpress','target_url':'http://x.com'} )
print r.text
r = requests.get( BASEURL+r1json['subid'], auth=('baba','babababa') )
print r.text

#
# get all subscr for a user
print "Get all subscriptions for a user+event ..."
r = requests.get( 'http://localhost:5000/event/buttonpress', auth=('baba','babababa') )
print r.text
