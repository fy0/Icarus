import json
import random
import string

import aiohttp
import time

from app import app
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from aioauth_client import GithubClient
import peewee
from slim.utils import to_hex, to_bin

import config
from model import db
from model._post import POST_STATE
from model.user import User
from model.user_oauth import UserOAuth
from api.user import UserViewMixin


@app.route.view('user/oauth')
class UserOAuthView(UserViewMixin, PeeweeView):
    model = UserOAuth

    github = GithubClient(
        client_id='config.CLIENT_ID',
        client_secret='config.CLIENT_SECRET'
    )

    @app.route.interface('GET')
    async def get_oauth_url(self):
        authorize_url = self.github.get_authorize_url(scope="user:email")
        self.finish(RETCODE.SUCCESS, {'state': 0, 'url': authorize_url})

    @app.route.interface('GET')
    async def get_user_data(self):
        code = self.params
        print(code)
        code = code['code']
        if code == 'undefined':
            self.finish(RETCODE.FAILED)
            return
        otoken, _ = await self.github.get_access_token(code)
        github = GithubClient(
            client_id=config.CLIENT_ID,
            client_secret=config.CLIENT_SECRET,
            access_token=otoken,
        )
        response = await github.request('GET', 'user')
        # response = json.loads(response)
        if response['id']:
            try:
                account = UserOAuth.get(UserOAuth.login_id == response['id'], UserOAuth.platform == 'github')
            except UserOAuth.DoesNotExist:
                account = None

            if account:
                if account.user_id:  # 返回用户已有信息
                    u = User.get_by_pk(account.user_id)
                    if u:
                        expires = 30
                        u.refresh_key()
                        self.setup_user_key(u.key, expires)
                        self.finish(RETCODE.SUCCESS, {'oauthcode': 0, 'user_id': account.user_id,
                                                      'state': account.state, 'access_token': u.key})
                else:
                    self.finish(RETCODE.SUCCESS, {'oauthcode': 1, 'state': account.state, 'oauth_id': account.id,
                                                  'login_id': account.login_id, 'platform': account.platform})
            else:
                ins = [{'login_id': response['id'], 'time': time.time(), 'platform': 'github',
                        'state': POST_STATE.APPLY}]
                if not isinstance(config.LONG_ID_GENERATOR, config.SQLSerialGenerator):
                    ins[0]['id'] = config.LONG_ID_GENERATOR().to_bin()

                UserOAuth.insert_many(ins).execute()
                self.finish(RETCODE.SUCCESS, {'oauthcode': 1, 'oauth_id': ins[0]['id'], 'state': ins[0]['state'],
                                              'login_id': ins[0]['login_id'], 'platform': ins[0]['platform']})
        else:
            self.finish(RETCODE.NOT_FOUND)

    @app.route.interface('POST')
    async def update(self):
        post = await self.post_data()
        print('提交的更新内容', post)

        try:
            account = UserOAuth.get(UserOAuth.login_id == post['loginId'], UserOAuth.platform == post['platform'])
        except UserOAuth.DoesNotExist:
            account = None
        except KeyError:
            account = None
            print('keyerror')

        if account:
            if post['state'] == str(POST_STATE.APPLY):
                # 该post['id']是user表中的id
                post_user_id = to_bin(post['id'])
                UserOAuth.update(user_id=post_user_id, state=POST_STATE.NORMAL).where(
                                                        UserOAuth.login_id == post['loginId']).execute()
                self.finish(RETCODE.SUCCESS)
            else:
                print('非法参数')
                self.finish(RETCODE.FAILED)
        else:
            self.finish(RETCODE.FAILED)
            print('failed')


"""
通过 access_token 拿到的数据字段
{
    'login': 'ly-nina',
    'id': 17906006,
    'avatar_url': 'https://avatars1.githubusercontent.com/u/17906006?v=4',
    'gravatar_id': '',
    'url': 'https://api.github.com/users/ly-nina',
    'html_url': 'https://github.com/ly-nina',
    'followers_url': 'https://api.github.com/users/ly-nina/followers',
    'following_url': 'https://api.github.com/users/ly-nina/following{/other_user}',
    'gists_url': 'https://api.github.com/users/ly-nina/gists{/gist_id}',
    'starred_url': 'https://api.github.com/users/ly-nina/starred{/owner}{/repo}',
    'subscriptions_url': 'https://api.github.com/users/ly-nina/subscriptions',
    'organizations_url': 'https://api.github.com/users/ly-nina/orgs',
    'repos_url': 'https://api.github.com/users/ly-nina/repos', 'events_url': https://api.github.com/users/ly-nina/events{/privacy}',
    'received_events_url': 'https://api.github.com/users/ly-nina/received_events',
    'type': 'User',
    'site_admin': False,
    'name': None,
    'company': None,
    'blog': '',
    'location': None,
    'email': None,
    'hireable': None,
    'bio': None,
    'public_repos': 11,
    'public_gists': 0,
    'followers': 0,
    'following': 0,
    'created_at': '2016-03-17T13:49:08Z',
    'updated_at': '2018-05-07T11:09:03Z'
}
"""
