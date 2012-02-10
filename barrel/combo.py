"""barrel.combo - access resource via alternate auth methods

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

from barrel.basic import BasicAuth
from barrel.form import FormAuth


class BasicFormAuth(object):
    """Use basic auth if AUTHORIZATION is sent or fall back to form auth.
    
    This is handy if you have both browsers and non-interactive clients
    accessing the same resources (resource doubles as a web service).
    """

    basic_auth = BasicAuth
    form_auth = FormAuth

    def __init__(self, app, users=None):
        """Create alternate versions of app with middlewares."""
        self.app = app
        self.basic_app = self.basic_auth(app, users=users)
        self.form_app = self.form_auth(app, users=users)

    def __setattr__(self, name, value):
        """Pass option setting to both versions of app."""
        self.__dict__[name] = value
        if name not in ['basic_app', 'form_app']:
            try:
                setattr(self.basic_app, name, value)
            except AttributeError:
                pass
            try:
                setattr(self.form_app, name, value)
            except AttributeError:
                pass

    def __call__(self, environ, start_response):
        """Call basic auth if header is present or call form auth."""
        if environ.get('HTTP_AUTHORIZATION'):
            return self.basic_app(environ, start_response)
        else:
            return self.form_app(environ, start_response)


