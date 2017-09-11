# coding:utf-8

from collections import OrderedDict


class _MetaClassForInit(type):
    def __new__(mcs, *args, **kwargs):
        new_class = super().__new__(mcs, *args, **kwargs)
        new_class.init()
        return new_class


class StateObject(metaclass=_MetaClassForInit):
    txt = {}
    _keys = []  # dummy
    _values = []  # dummy
    v2k = {}  # dummy

    @classmethod
    def get_txt(cls, index):
        return cls.txt.get(index)

    @classmethod
    def keys(cls):
        return cls._keys

    @classmethod
    def values(cls):
        return cls._values

    @classmethod
    def items(cls):
        for k, v in zip(cls.keys(), cls.values()):
            yield k, v

    @classmethod
    def init(cls):
        _v2k, v2k = {}, OrderedDict()

        for k, v in cls.__dict__.items():
            if k.isupper() and type(v) == int:
                _v2k[v] = k

        for i in sorted(_v2k.keys()):
            v2k[i] = _v2k[i]

        cls._keys = list(v2k.values())
        cls._values = list(v2k.keys())
        cls.v2k = v2k


if __name__ == '__main__':
    class MyState(StateObject):
        DEL = 0
        HIDE = 10
        CLOSE = 30 # 禁止回复
        NORMAL = 50

        txt = {DEL: "删除", HIDE: "隐藏", CLOSE:"关闭", NORMAL:"正常"}

    print(list(MyState.keys()))
    print(list(MyState.values()))
    print(list(MyState.items()))
    print(list(MyState.v2k.items()))
    print([MyState.get_txt(x) for x in MyState.values()])
