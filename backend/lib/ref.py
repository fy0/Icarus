
class Reference:
    def __init__(self, obj=None):
        object.__setattr__(self, '_obj', obj)

    def __getattribute__(self, item):
        if item == '_obj':
            return object.__getattribute__(self, '_obj')
        return self._obj.__getattribute__(item)

    def __getitem__(self, item):
        return self._obj.__getitem__(item)

    def __setitem__(self, key, value):
        return self._obj.__setitem__(key, value)

    def __setslice__(self, i, j, sequence):
        return self._obj.__setslice__(i, j, sequence)

    def __setattr__(self, key, value):
        if key == '_obj':
            return object.__setattr__(self, '_obj', value)
        return self._obj.__setattr__(key, value)
