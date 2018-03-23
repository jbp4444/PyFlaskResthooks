# PyFlaskResthooks
Simple demo of Python+Flask code for REST-Hooks.  The primary objective was for
me to get my head around how REST-Hooks work and what (minimal) state was needed
to track the subscriptions, etc. at the server level.

* www directory contains the code needed for start-up (assumes apache/wsgi)
* www/flask_app contains the main code
* testing contains some simple python-requests scripts
* thunkable contains an AIA file suitable for Thunkable or MIT-AppInventor
  * http://thunkable.com/
  * http://appinventor.mit.edu/

With an external subscription service (e.g. Zapier), the service would:
* Reach out to the "subscribe" end-point (POST to /), with a user's credentials
  * Following Zapier, the server looks for an 'event' and 'target_url'
* The server stores that subscription info
* When the 'event' happens (data is received), the server would make the calls to the target_url's
  * The assumption is that a device would POST data to /data/event and that would initiate the callback to the target_url's

The Thunkable/MIT-AI app models a simple IOT-style interaction:
* The device generates a random device-code and registers it with the server
  * The device then presents that code to the user and instructs the user to "activate" it
* The user logs in to some web-UI (not provided, but the hooks are built-in) and activates the device-code
* The device eventually polls the server to see if the code has been "claimed"
* If claimed by a user, the server responds to the device with a device-token (API-key) and stores the device-to-user connection in a database

Requirements:
* Python 2.7
* Flask - http://flask.pocoo.org/
* Requests - http://docs.python-requests.org/en/master/
* Peewee - http://docs.peewee-orm.com/
* Flup and wsgiref (should come by default)
