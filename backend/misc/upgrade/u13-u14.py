"""
如果执行失败，请将此文件复制到backend目录再次执行。
"""

import sys
sys.path.insert(0, '.')

from model import db


def sql_execute(sql):
    try:
        db.execute_sql(sql)
    except Exception as e:
        print(e)
        print('failed: %s' % sql)
        db.rollback()


def work():
    sql_execute('ALTER TABLE board ADD can_post_rank int DEFAULT 0 NULL;')
    sql_execute('CREATE INDEX board_can_post_rank ON board (can_post_rank);')


if __name__ == '__main__':
    work()
    print('done')
