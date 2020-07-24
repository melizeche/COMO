from datetime import datetime

from blake3 import blake3
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

class Actor:
    def __init__(self, name, actor_type):
        self.name = name
        self.key = blake3(str(self.name).encode('utf-8')).hexdigest()
        self.type = actor_type
    
    def __repr__(self):
        return f'<{self.name}: {self.key}>'

@dataclass
class Como:
    issuer: Actor
    benefactor: Actor
    beneficiary: Actor
    timestamp: datetime = datetime.now()