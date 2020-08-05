from serialize import Serializable


class Output(Serializable):
    def __init__(self, address, value, extra):
        self.address = address
        self.value = value
        self.extra = extra

    def __repr__(self):
        return repr([
            self.address,
            self.value,
        ])
