"""barrel.basic - basic authentication support

(See the docstrings of the various functions and classes.)

Copyright (C) 2006-2008 Luke Arno - http://lukearno.com/

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to:

The Free Software Foundation, Inc., 
51 Franklin Street, Fifth Floor, 
Boston, MA  02110-1301, USA.

Luke Arno can be found at http://lukearno.com/

"""

class BasicAuth(object):
    """HTTP Basic authentication middleware.
    
    Also the base class for other authentication methods.
    """

    session_key = 'barrel.session'
    session_user_key = 'barrel.user'
    realm = 'WSGIBarrel'
    users = None

    def __init__(self, app, users=None):
        """Take the app to wrap and optional settings."""
        self.app = app
        if users is not None:
            self.users = users
        elif self.users is None:
            self.users = []

    def valid_user(self, username, password):
        """Is this a valid username/password? (True or False)"""
        for usr, pwd in self.users:
            if username == usr and password == pwd:
                return True
        else:
            return False

    def session_dict(self, environ):
        """Get the session for caching username.
        
        The default place to look for a session is where
        flup puts it.
        """
        return environ.get(self.session_key)

    def save_session(self):
        """Save out the session.

        Replace with a do-nothing if you use a package that does
        not require you to explicitly save out sessions.
        """
        session = self.session_dict()
        if session is not None:
            return session.save()

    def cache_username(self, environ, username):
        """Store the username in a session dict if found.
        
        Also populates REMOTE_USER.
        """
        environ['REMOTE_USER'] = username
        session = self.session_dict(environ)
        if session is not None:
            session[self.session_user_key] = username

    def get_cached_username(self, environ):
        """Look for the username in the session if found.
        
        Also populates REMOTE_USER if it can.
        """
        session = self.session_dict(environ)
        if session is not None:
            return session.get(self.session_user_key)
        else:
            return None

    def username_and_password(self, environ):
        """Pull the creds from the AUTHORIZAITON header."""
        # Should I check the auth type here?
        auth_string = environ.get('HTTP_AUTHORIZATION')
        if auth_string is None:
            return ('', '')
        else:
            return auth_string[6:].strip().decode('base64').split(':')

    def authenticate(self, environ):
        """Is this request from an authenicated user? (True or False)"""
        username, password = self.username_and_password(environ)
        if username and password:
            if self.valid_user(username, password):
                self.cache_username(environ, username)
                return True
        else:
            username = self.get_cached_username(environ)
            if username is not None:
                self.cache_username(environ, username)
                return True
            
        return False

    def not_authenticated(self, environ, start_response):
        """Respond to an unauthenticated request with a 401."""
        start_response('401 Unauthorized',
                        [('WWW-Authenticate', 'Basic realm=' + self.realm)])
        return ["401 Unauthorized: Please provide credentials."]

    def __call__(self, environ, start_response):
        """If request is not from an authenticated user, complain."""
        if self.authenticate(environ):
            return self.app(environ, start_response)
            self.save_session()
        else:
            return self.not_authenticated(environ, start_response)


