"""setup - setuptools based setup for barrel

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

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(name='barrel',
      version='0.1.3',
      description=\
        'Flexible WSGI authentication and authorization tools.',
      long_description="""\
This distribution provides a variety of access control middlewares.
Convenience functions which can be used as decorators are included.
The classes have useful defaults yet are highly configurable. 
All interfaces are designed to be easily customized and extended.
Currently supports HTTP Basic and Web forms authentication, 
roles-based authorization and is beaker session compatible out of
the box. (It is no problem to use some other type of sessions or none.)""",
      author='Luke Arno',
      author_email='luke.arno@gmail.com',
      url='http://lukearno.com/projects/barrel/',
      license="GPL2",
      py_modules=[],
      packages = ['barrel'],
      keywords="wsgi authentication authorization web http webapps",
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Security',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Utilities'])

