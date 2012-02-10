"""yalecas - Yale CAS compatible authentication module.

This is still pretty limited.

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

import urllib
from cgi import parse_qs
from xml.dom import minidom
from wsgiref.util import request_uri

from barrel.basic import BasicAuth


class CASAuth(BasicAuth):

    def __init__(self, app, cas_login_uri, cas_validate_uri):
        """Take the app to wrap and optional settings."""
        self.app = app
        self.cas_login_uri = cas_login_uri
        self.cas_validate_uri = cas_validate_uri

    def validate_ticket(self, environ):
        """"""
        qs = parse_qs(environ['QUERY_STRING'])
        ticket = qs.get('ticket', [None])[0]
        if ticket is None:
            return None
        uri = self.validate_uri(environ, ticket, qs)
        handle = urllib.urlopen(uri)
        text = handle.read()
        print text
        xml = minidom.parseString(text)
        user = xml.getElementsByTagName('cas:user')
        if user:
            return user[0].childNodes[0].data
        else:
            return None

    def validate_uri(self, environ, ticket, qs):
        cas_qs = {}
        cas_qs['service'] = request_uri(environ, include_query=0)
        print cas_qs['service']
        new_qs = []
        for k, v in qs.iteritems():
            print k
            if k != 'ticket':
                for vv in v:
                    new_qs.append((k, vv))
        if new_qs:
            cas_qs['service'] += '?' + urllib.urlencode(new_qs)
        print cas_qs['service']
        cas_qs['ticket'] = ticket
        return self.cas_validate_uri + '?' + urllib.urlencode(cas_qs)

    def login_uri(self, environ):
        """"""
        qs = {}
        qs['service'] = request_uri(environ)
        print qs['service']
        return self.cas_login_uri + '?' + urllib.urlencode(qs)

    def authenticate(self, environ):
        """Is this request from an authenicated user? (True or False)"""
        username = self.get_cached_username(environ)
        if username is not None:
            self.cache_username(environ, username)
            return True
        else:
            username = self.validate_ticket(environ)
            if username is not None:
                self.cache_username(environ, username)
                return True
            else:
                return False

    def not_authenticated(self, environ, start_response):
        """Respond to an unauthenticated request with a 401."""
        uri = self.login_uri(environ)
        start_response('302 Found',
                        [('Location', uri)])
        return ["Redirect to CAS: " + uri]

    def __call__(self, environ, start_response):
        """If request is not from an authenticated user, complain."""
        if self.authenticate(environ):
            return self.app(environ, start_response)
        else:
            return self.not_authenticated(environ, start_response)


