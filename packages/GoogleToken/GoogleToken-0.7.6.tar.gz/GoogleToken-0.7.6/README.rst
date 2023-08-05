.. image:: https://travis-ci.org/scottphilip/google-token.svg?branch=master
    :target: https://travis-ci.org/scottphilip/google-token

Google Token
============

Python Package allowing `Google
Account <https://myaccount.google.com>`__ Authorization Tokens to be
issued when user is not in attendance.

Installation Instructions
-------------------------

::

    pip install GoogleToken

Properties
----------

When manually logging into a Google Account secured web application, the
initial URL will be in the format;

::

    https://accounts.google.com/o/oauth2/v2/auth?response_type=token&client_id=0000000000000-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com&redirect_uri=https://www.website.com/google/callback&scope=https://www.googleapis.com/auth/userinfo.email%20https://www.googleapis.com/auth/userinfo.profile

+-----------+----------------------------------------------------------------+
| Property  | Example                                                        |
+===========+================================================================+
| Client Id | 0000000000000-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleuser |
|           | content.com                                                    |
+-----------+----------------------------------------------------------------+
| Redirect  | https://www.website.com/google/callback                        |
| Uri       |                                                                |
+-----------+----------------------------------------------------------------+
| Scope     | https://www.googleapis.com/auth/userinfo.email                 |
|           | https://www.googleapis.com/auth/userinfo.profile               |
+-----------+----------------------------------------------------------------+

Usage Instructions
------------------

First time login will create a Cookies file which stores the issued
tokens which will subsequently be reused. It is recommended not to the
password or the OTP secret in configuration. Once the cookies file is
created the credentials are not required.

.. code:: python

        from GoogleToken import GoogleTokenGenerator, GoogleTokenParameters
        parameters = GoogleTokenParameters(oauth_client_id="0000000000000-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com",
                                  oauth_redirect_uri="https://www.website.com/google/callback",
                                  oauth_scope="https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
                                  account_email="user@gmail.com",
                                  account_password="password",
                                  account_otp_secret="secret")
        generator = GoogleTokenGenerator(parameters)
        token = generator.generate()
        print(token)

Once the cookies file is created, the credentials can be omitted.

.. code:: python

    from GoogleToken import get_google_token
    token, expiry = get_google_token(account_email="account@gmail.com",
                                     account_password="password",
                                     account_otp_secret="secret",
                                     oauth_client_id="0000000000000-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com",
                                     oauth_redirect_uri="https://www.website.com/google/callback",
                                     oauth_scope="https://www.googleapis.com/auth/userinfo.profile")


Dependencies
------------

`Selenium <https://pypi.python.org/pypi/selenium>`__

`Pyotp <https://pypi.python.org/pypi/pyotp>`__

Credits
-------

Scott Philip

Berlin, Germany

Licence
-------

GNU General Public License (Version 3, 29 June 2007)

CallerLookup Copyright © 2017 Scott Philip
