# Setup Process for Zapier Integration
We'll create a Zapier "App Integration" to allow our Thunkable mobile app
to send data into Zapier.  Inside Zapier, we can create "Zaps" which
then forward that data to other services.

* Worth reading through to get the basics of what we'll be doing:
https://zapier.com/developer/documentation/v2/
  * Especially "Key Zapier Concepts and the 5 "App Lifecycle" stages
* You'll also need to sign up for a "Developer" account at Zapier.


### Create the Zapier App Integration
The first step is to create an "App Integration" -- a connection
between the outside world and Zapier.
All of the companies that Zapier can talk to are separate "Integrations",
and we'll set our system up the same way.

Go to your Developer section -- once you've logged in, click on your
username in the top-right corner of the page and a drop-down should
appear, select "Developers".  We'll use the "Create A Web Builder App"
process, though it is worth noting that this is now considered a
"legacy" approach (the command-line interface is now recommended).
