from model import db
from model import _models


def work():
    try:
        db.execute_sql('ALTER TABLE public.topic ADD awesome INTEGER DEFAULT 0;')
    except:
        db.rollback()


if __name__ == '__main__':
    work()
    print('done')
