from datetime import datetime

from blake3 import blake3
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from dataclasses import dataclass

from typing import Any, List

class Block:

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hashing()

    def hashing(self):
        key = blake3()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()

class Actor: # Wallet?
    def __init__(self, name, actor_type):
        self.name = name
        self.key = self.generate_key()
        self.type = actor_type

    def generate_key(self):
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

    @property
    def public_key(self):
        pk = self.key.public_key()
        pem = pk.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem

    
    def __repr__(self):
        return f'<{self.name}: {self.key}>'

@dataclass
class Como:
    issuer: Actor
    benefactor: Actor
    beneficiary: Actor
    timestamp: datetime = datetime.now()