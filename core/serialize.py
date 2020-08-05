import bson
import json
import hashlib
from copy import copy
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class Serializable:

    def hex(self, a_dict):
        new = copy(a_dict)
        for k, v in new.items():
            if isinstance(v, bytes):
                new[k] = v.hex()
        return new

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.hex(self.__dict__))

    def serialize(self):
        return bson.dumps(self.__dict__)

    def deserialize(self, bson_bytes: bytes):
        return bson.loads(bson_bytes)

    def hash(self):
        hashing = hashlib.sha512()
        hashing.update(self.serialize())

        return hashing.hexdigest()

    def __repr__(self):
        return repr(self.hex(self.__dict__))
