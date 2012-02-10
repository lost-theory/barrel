"""barrel.roles - roles based authorization support

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


class RolesAuthz(object):
    """Authorize (or not) by compairing user roles to allowed roles."""

    environ_roles_key = 'barrel.roles'
    session_key = 'com.saddi.service.session'
    session_roles_key = 'barrel.roles' 

    def __init__(self, app, allowed_roles=None, roles_dict=None):
        """Take the app to wrap and optional settings."""
        self.app = app
        if allowed_roles is None:
            self.allowed_roles = []
        else:
            self.allowed_roles = allowed_roles
        if roles_dict is None:
            self.roles_dict = {}
        else:
            self.roles_dict = roles_dict

    def user_roles(self, username):
        """Get a list of roles for the given username.""" 
        return self.roles_dict.get(username, [])

    def look_up_roles(self, environ):
        """Find the username in environ and use it to get a list of roles."""
        roles_list = self.user_roles(environ.get('REMOTE_USER', ''))
        self.cache_roles(environ, roles_list)
        return roles_list

    def get_roles(self, environ):
        """Get user roles from cache or by looking them up."""
        cached_roles = self.get_cached_roles(environ)
        if cached_roles is not None:
            return cached_roles
        else:
            return self.look_up_roles(environ)
 
    def session_dict(self, environ):
        """Get the session for caching username.
        
        The default place to look for a session is where
        flup puts it.
        """
        service = environ.get(self.session_key)
        if service:
            return service.session

    def cache_roles(self, environ, roles_list):
        """Store roles in environ and session if found."""
        environ[self.environ_roles_key] = roles_list
        session = self.session_dict(environ)
        if session:
            session[self.session_roles_key] = roles_list

    def get_cached_roles(self, environ):
        """Find roles in environ or session if found."""
        roles = environ.get(self.environ_roles_key)
        if roles:
            return roles
        else:
            session = self.session_dict(environ)
            if session:
                return session.get(self.session_roles_key)

    def authorize(self, environ):
        """Is this request from a user with the required roles?"""
        for user_role in self.look_up_roles(environ):
            if user_role in self.allowed_roles:
                return True
        return False

    def not_authorized(self, environ, start_response):
        """Respond to an unauthorized request with a 403."""
        start_response('403 Forbidden', [])
        return ["403 Forbidden: You are not allowed to access that."]

    def __call__(self, environ, start_response):
        """If request is not from an authorized user, complain."""
        if self.authorize(environ):
            return self.app(environ, start_response)
        else:
            return self.not_authorized(environ, start_response)


