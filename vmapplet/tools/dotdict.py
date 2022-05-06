class DotDict(dict):

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self):
        for key, value in self.items():
            self[key] = DotDict(value) if type(value) == dict else value
