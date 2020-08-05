from serialize import Serializable


class Input(Serializable):
    def __init__(self, prev_hash, signature, public_key, outputs):
        self.prev_hash = prev_hash
        self.signature = signature
        self.public_key = public_key
        self.outputs = outputs

    def is_valid(self):
        return True

    def __repr__(self):
        return repr([
            self.public_key,
            self.prev_hash,
            self.outputs,
        ])
