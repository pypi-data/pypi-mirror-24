# -*- coding: utf-8 -*-

import base64
import pickle
from irods.pool import Pool
from irods.session import iRODSSession

"""
Allow to manipulate irods session as a string,
to be saved inside a database.
"""


class iRODSPickleSession(iRODSSession):

    def __getstate__(self):
        attrs = {}
        for attr in self.__dict__:
            obj = getattr(self, attr)
            if attr == 'pool':
                attrs['account'] = obj.account
            else:
                attrs[attr] = obj

        return attrs

    def __setstate__(self, state):

        for name, value in state.items():
            # print(name, value)
            setattr(self, name, value)

        self.pool = Pool(state.get('account'))

    def serialize(self):
        """Returns a byte serialized string from the current session"""
        serialized = pickle.dumps(self)
        return base64.encodestring(serialized)

    @staticmethod
    def deserialize(obj):
        return pickle.loads(base64.decodestring(obj))
