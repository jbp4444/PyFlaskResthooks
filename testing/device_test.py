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
