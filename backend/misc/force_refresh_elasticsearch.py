"""
重置和刷新es数据
"""

import sys
sys.path.insert(0, '.')

from model import esdb

if __name__ == '__main__':
    esdb.update_all(reset=True)
