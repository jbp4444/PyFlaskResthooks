#
#

import requests

BASEURL = 'http://localhost:5000/'

#
# add some subscriptions
#
print "Device posts a device-code to server ..."
r1 = requests.post( BASEURL+'link/', data={'authcode':'abc123'} )
print r1.text

print "Device sees if device-code has been claimed by a user ... not yet"
r2 = requests.get( BASEURL+'link/abc123' )
print r2.text

print "User baba claims that dev-code ..."
r3 = requests.get( BASEURL+'activate/abc123', auth=('baba','babababa') )
print r3.text

print "Device sees if device-code has been claimed by a user ... yes"
r4 = requests.get( BASEURL+'link/abc123' )
print r4.text

r4j = r4.json()

print "The device can now push data with its token ..."
r5 = requests.post( BASEURL+'data/buttonpress', headers={'X-Device-Token':r4j['token']} )
print r5.text
