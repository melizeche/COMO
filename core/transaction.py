from typing import List
from serialize import Serializable
from input import Input


class Transaction(Serializable):
    def __init__(self, inputs: List[Input]):
        self.inputs = inputs

    def is_valid(self, b) -> bool:
        pk = []
        for i in range(len(self.inputs)):
            if not self.inputs[i].is_valid(b):
                return False
            pk.append(self.inputs[i].public_key)
        return True
