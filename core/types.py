from datetime import datetime

from blake3 import blake3
from collections import OrderedDict
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
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
        key.update(str(self.index).encode("utf-8"))
        key.update(str(self.timestamp).encode("utf-8"))
        key.update(str(self.data).encode("utf-8"))
        key.update(str(self.previous_hash).encode("utf-8"))
        return key.hexdigest()


class Actor:  # Wallet?
    def __init__(self, name, actor_type):
        self.name = name
        self.key = self.generate_key()
        self.type = actor_type

    def generate_key(self):
        return rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

    @property
    def public_key(self):
        pk = self.key.public_key()
        pem = pk.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return pem

    @property
    def private_key(self):
        pem = self.key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
        )
        return pem

    def __repr__(self):
        return f"<{self.name}: {self.public_key}>"


@dataclass
class Como:
    uid: int
    issuer: Actor
    benefactor: Actor
    beneficiary: Actor
    timestamp: datetime = datetime.now()


class Transaction:

    def __init__(self, sender_address, sender_private_key: rsa.RSAPrivateKey, recipient_address, value):
        # TODO: check types
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.value = value

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return dict(
            sender_address=self.sender_address,
            recipient_addres=self.recipient_address,
            value=self.value
            )

    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        self.signature = self.sender_private_key.sign(
            data=str(self.to_dict).encode(),
            padding=padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            algorithm=hashes.SHA256()
        )
        return self.signature
