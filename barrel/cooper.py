"""barrel.cooper - convenience interface for barrel

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
from barrel.combo import BasicFormAuth
from barrel.roles import RolesAuthz


def decorize(middleware):
    """Return customizable middleware decorator factory.
    
    Returns a decorator factory function that will return
    decorators that apply the given middleware then assign
    any keyword args to corresponding attributes of the result.
    """
    classname = middleware.__class__
    def metadeco(config=None, *args, **kwargs):
        """Decorate with middleware then set attribs."""
        stringkwargs = ["%s=%s" % (key, repr(val)) 
                        for (key, val) in kwargs.iteritems()]
        def deco(app):
            """Decorated with middleware and attribs set."""
            newapp = middleware(app)
            for key, value in kwargs.iteritems():
                try:
                    setattr(newapp, key, value)
                except AttributeError:
                    pass
            return newapp
        deco.__doc__ = """Decorate given app with %s
        
        Sets attributes on the resulting object (if it can):
        
        %s
        """ % (middleware.__name__, "\n      ".join(stringkwargs))
        return deco
    metadeco.__doc__ = ("Create decorator that will use %s "
                        "with given attributes.") % classname
    return metadeco


basicauth = decorize(BasicAuth)
formauth = decorize(FormAuth)
comboauth = decorize(BasicFormAuth)
rolesauth = decorize(RolesAuthz)

