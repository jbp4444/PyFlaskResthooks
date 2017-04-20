#
#

import requests

print "Device-codes ..."
r = requests.get( 'http://localhost:5000/admin/devcodes', auth=('mossy','mossymossy') )
print r.text
print "Device-tokens ..."
r = requests.get( 'http://localhost:5000/admin/tokens', auth=('mossy','mossymossy') )
print r.text
print "Users ..."
r = requests.get( 'http://localhost:5000/admin/users', auth=('mossy','mossymossy') )
print r.text
print "Subscriptions ..."
r = requests.get( 'http://localhost:5000/admin/subs', auth=('mossy','mossymossy') )
print r.text
print "Events ..."
r = requests.get( 'http://localhost:5000/admin/events', auth=('mossy','mossymossy') )
print r.text
