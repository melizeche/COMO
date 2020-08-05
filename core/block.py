import time
from secrets import token_bytes
from serialize import Serializable

from pprint import pprint


class Block(Serializable):
    NONCE_SIZE = 12

    def __init__(self, block_id, previous_block, nonce=None, timestamp=None, merkle_root=None):

        self.block_id = block_id
        self.previous_block = previous_block
        self.nonce = nonce
        self.timestamp = timestamp
        self.merkle_root = merkle_root
        self.transactions = []
        self.version = 1

        if not self.timestamp:
            self.new_timestamp()

        if not self.nonce:
            self.new_nonce()

        if not self.merkle_root:
            self.merkle_root = bytes(16)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def new_timestamp(self):
        self.timestamp = int(time.time())

    def new_nonce(self):
        self.nonce = token_bytes(self.NONCE_SIZE)

    # def __repr__(self):
    #     return repr([
    #         self.block_id,
    #         self.previous_block,
    #         self.version,
    #         self.nonce,
    #         self.timestamp,
    #         self.merkle_root,
    #         self.transactions,
    #     ])


print("Tests")
x = Block(195334333123343122, bytes.fromhex('974eeb3e15fee6b8309ec1fc58b8288e3a4eebbc'))

print("serialize:\n", x.serialize())
print("hash:\n", x.hash())
print("to_dict:\n")
pprint(x.to_dict())
print("print:\n", x)
print("to_json:\n")
pprint(x.to_json())
print(type(x.to_json()))
print("deserialize:\n")
pprint(x.deserialize(x.serialize()))
