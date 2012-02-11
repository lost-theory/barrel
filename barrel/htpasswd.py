"""htpasswd - htpasswd compatible authentication module.

Pass in the path to an htpasswd file, and basic auth will validate users
and passwords from that file.

Copyright (C) 2012 Steven Kryskalla - http://lost-theory.org/

See README for license info.
"""

from barrel.basic import BasicAuth

from crypt import crypt

class HtpasswdBasicAuth(BasicAuth):
    def __init__(self, app, htpasswd_path):
        self.app = app
        htpasswd = open(htpasswd_path)
        htpasswd = [line.strip().split(':') for line in htpasswd]
        self.htpasswd = dict(htpasswd)

    def valid_user(self, username, password):
        if username not in self.htpasswd:
            return False
        vhash = self.htpasswd[username]
        return crypt(password, vhash) == vhash
