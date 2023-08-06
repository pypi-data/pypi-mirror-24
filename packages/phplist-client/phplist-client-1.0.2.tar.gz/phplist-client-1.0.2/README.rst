Python library for PHPList REST API
===================================

This is a python 3 library for interacting with the PHPList REST API.

To Use
------

1. ``pip install -r requirements``
2. Write your code:

   \`\`\`python from phplist import PHPListClient

   client = PHPListClient("https://myphplistresturl", secret="mysecret")
   client.login(login="myusername", password="mypassword") output =
   client.lists\_get() \`\`\`

Run Tests
---------

1. ``pip install nose``
2. ``nosetests tests.py``

TODO
----

-  add setup.py
-  push up to pypi
