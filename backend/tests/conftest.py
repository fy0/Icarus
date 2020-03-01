import os

import pytest
from slim import Application
from slim.utils import get_ioloop
from slim.utils.autoload import import_path

from app import app
from model.user import User

import model._models


def app_init():
    import_path('api', base_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    loop = get_ioloop()
    # loop.run_until_complete(redis.init(loop))

    app._prepare()


app_init()


user_names = []
user_name_to_id = {}


def user_new(username, *args, **kwargs):
    user_names.append(username)
    u = User.new(username, *args, **kwargs)
    user_name_to_id[username] = u.id
    return u


@pytest.yield_fixture()
def event_loop():
    loop = get_ioloop()
    yield loop
    # loop.close()


@pytest.fixture(scope='session', autouse=True)
def do_setup(request: pytest.Session):
    user_new('_test_user_1', 'password')
    user_new('_test_user_2', 'password')
    user_new('_test_user_3', 'password')


def pytest_sessionfinish(session, exitstatus):
    n = User.delete().where(User.username.in_(user_names)).execute()
