"""barrel.form - web form based authentication support

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


import string
import cgi
from cStringIO import StringIO


from barrel.basic import BasicAuth

default_template = """<?xml version="1.0"?>
<!DOCTYPE html 
  PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
    <title>Form Auth</title>
</head>
<body>
    <h1>Resource Requires Authentication</h1>
    <form method="POST" action="">
        <fieldset>
            <legend>$message:</legend>
            <label for="$user_field">Username:</label>
            <input type="text" 
                   name="$user_field" 
                   id="$user_field" 
                   value="$username"/>
            <br/>
            <label for="$pass_field">Password:</label>
            <input type="password" name="$pass_field" id="$pass_field"/>
            <br/>
            <button type="submit" 
                    name="$button" 
                    id="$button"
                    value="submit">Sign In</button>
        </fieldset>
    </form>
</body>
</html>"""


class FormAuth(BasicAuth):
    """Web Form authentication middleware."""
    
    user_field = 'username'
    pass_field = 'password'
    button = 'barrel-form-button'
    environ_user_key = 'barrel.form.username'

    first_message = "Please enter your username and password"
    failed_message = "Sign in failed; please try again"
    
    template = string.Template(default_template)

    def username_and_password(self, environ):
        """Pull the creds from the form encoded request body."""
        # How else can I tell if this is an auth request before reading?
        if environ.get('CONTENT_LENGTH'):
            clen = int(environ['CONTENT_LENGTH'])
            sio = StringIO(environ['wsgi.input'].read(clen))
            fs = cgi.FieldStorage(fp=sio,
                                  environ=environ,
                                  keep_blank_values=True)
            sio.seek(0)
            environ['wsgi.input'] = sio
            if fs.getlist(self.button):
                try:
                    username = fs[self.user_field].value
                    password = fs[self.pass_field].value
                    environ[self.environ_user_key] = username
                    return username, password
                except KeyError:
                    pass # silence
        
        return '', ''

    def not_authenticated(self, environ, start_response):
        """Respond to an unauthenticated request with a form."""
        start_response('200 OK', [('Content-Type', 'text/html')])
        username = environ.get(self.environ_user_key, '')
        if username:
            message = self.failed_message
        else:
            message = self.first_message
        return [self.template.safe_substitute(user_field=self.user_field,
                                              pass_field=self.pass_field,
                                              button=self.button,
                                              username=username,
                                              message=message,
                                              **environ)]


