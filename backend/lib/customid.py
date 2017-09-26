import os
import time
import socket
import struct
import hashlib
import binascii

'''
6字节时间戳

[粒度：0.1ms/100μs] √
0xffff_ffff_ffff / 10000
28147497671.0655
终止日期：2861年12月16日 13:21:11

[粒度：0.01ms/10μs]
0xffff_ffff_ffff / 100000
2814749767.10655
终止日期：2059年03月13日 10:56:07
'''


class CustomID(object):
    _index = 0
    _hostname_bytes = hashlib.md5(socket.gethostname().encode('utf-8')).digest()[:1]

    def __init__(self, custom_id=None):
        if custom_id:
            self._parse_id(custom_id)
        else:
            self._gen_id()

    def _gen_id(self):
        # 0|1|2|3|4|5   | 6    | 7    | 8|9
        # 时间戳     | 计数器 | 机器 | PID
        cls = self.__class__
        self._time = int(time.time() * 10000)
        _1 = self._time.to_bytes(6, 'big')
        cls._index = (cls._index + 1) % 0xFF  # 安全阈值：每0.1ms 255个
        _2 = cls._index.to_bytes(1, 'big')
        _3 = self._hostname_bytes
        _4 = struct.pack(">H", os.getpid() % 0xFFFF)
        self._id = b''.join((_1, _2, _3, _4),)

    @property
    def time(self):
        return self._time // 10000

    def _parse_id(self, custom_id):
        if type(custom_id) == str:
            if len(custom_id) != 20:
                raise TypeError
            custom_id = binascii.unhexlify(bytes(custom_id, 'utf-8'))

        if type(custom_id) == bytes:
            if len(custom_id) != 10:
                raise TypeError
            self._time = int.from_bytes(custom_id[:6], 'big')
            self._id = custom_id
        else:
            raise TypeError

    @classmethod
    def check_valid(cls, str_or_bytes):
        try:
            return cls(str_or_bytes)
        except TypeError:
            pass

    def to_bin(self):
        return self._id

    def to_hex(self):
        return str(self)

    digest = to_bin
    hexdigest = to_hex

    def __str__(self):
        return str(binascii.hexlify(self._id), 'utf-8')

    def __repr__(self):
        return "CustomID('%s')" % str(self)

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id == other._id
        raise TypeError

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self._id != other._id
        raise TypeError

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self._id < other._id
        raise TypeError

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self._id <= other._id
        raise TypeError

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self._id > other._id
        raise TypeError

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self._id >= other._id
        raise TypeError
