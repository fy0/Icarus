import json
import random
import string

import aiohttp
import time

from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from aioauth_client import GithubClient
import peewee
from slim.utils import to_hex, to_bin

import config
from model import db
from model.user import User
from model.user_oauth import UserOAuth
from view import route
from view.user import UserMixin


@route('user/oauth')
class UserOAuthView(UserMixin, PeeweeView):
    model = UserOAuth

    github = GithubClient(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET
    )

    @route.interface('GET')
    async def get_oauth_url(self):
        authorize_url = self.github.get_authorize_url(scope="user:email")
        self.finish(RETCODE.SUCCESS, {'state': 0, 'url': authorize_url})

    # 此部分使用拿到的数据字段来注册一个账号，包括但不限于 /新建表/ - 用户校验 - 用户创建
    @route.interface('GET')
    async def get_user_data(self):
        # 前端拿到code，向后端发请求，后端取 access_token ，再通过 token 去取用户数据。
        # 取到数据之后，查询是否已存在。如果已存在，返回用户ID，否则返回部分用户数据，用来让用户确认新用户数据。
        code = self.params
        print(code)
        code = code['code']
        otoken, _ = await self.github.get_access_token(code)
        github = GithubClient(
            client_id=config.CLIENT_ID,
            client_secret=config.CLIENT_SECRET,
            access_token=otoken,
        )
        response = await github.request('GET', 'user')
        print('response:', response)
        # response = json.loads(response)
        if response['id']:
            try:
                account = UserOAuth.get(UserOAuth.login_id == response['id'], UserOAuth.platform == 'github')
            except UserOAuth.DoesNotExist:
                account = None

            print('account:', account)
            if account:
                if account.user_id:  # 返回用户已有信息
                    print('retcode', RETCODE.SUCCESS)
                    u = User.get_by_pk(account.user_id)
                    print('account.id2user', account.id2user)
                    print('account.id:', account.id)
                    print('u:', u)
                    if u:
                        expires = 30
                        u.refresh_key()
                        self.setup_user_key(u.key, expires)
                        self.finish(RETCODE.SUCCESS, {'oauthcode': 0, 'id2user': account.id2user, 'access_token': u.key})
                else:
                    self.finish(RETCODE.SUCCESS, {'oauthcode': 1, 'id2user': account.id2user,
                                                  'login_id': account.login_id, 'platform': account.platform})
                # else:
                #     self.finish(RETCODE.FAILED)
            else:  # 在oauth表中新建用户，返回部分用户数据
                changid = ''.join([random.choice(string.digits) for i in range(9)])
                print('changid:', changid)
                ins = [{'id2user': int(changid), 'login_id': response['id'], 'time': time.time(), 'platform': 'github'}]
                UserOAuth.insert_many(ins).execute()
                self.finish(RETCODE.SUCCESS, {'oauthcode': 1, 'id2user': ins[0]['id2user'],
                                              'login_id': ins[0]['login_id'], 'platform': ins[0]['platform']})
        else:
            self.finish(RETCODE.NOT_FOUND)

    @route.interface('POST')
    async def update(self):
        # 不需要创建新用户了，在 get_user_data 函数中，会判断是否是新人。
        # 是新人的话，前端在用户填好信息，新建用户之后。调用此接口，更新oauth表中该用户的信息。
        post = await self.post_data()
        print('提交的更新内容', post)

        try:
            account = UserOAuth.get(UserOAuth.id2user == post['id2user'], UserOAuth.platform == post['platform'])
        except UserOAuth.DoesNotExist:
            account = None
        except KeyError:
            account = None
            print('keyerror')

        print(account)
        if account:
            if len(str(account.id2user)) == 9:  # 长id # 这里读字段不是这样读的，错了。
                # 把原来随机的id2user更新成user表中对应的用户id
                print('post_id:', post['id'])
                post_user_id = to_bin(post['id'])
                print('post_user_id:', post_user_id)
                UserOAuth.update(id2user=post['id'], user_id=post_user_id).where(UserOAuth.id2user == post['id2user']).execute()
                print('success')
                self.finish(RETCODE.SUCCESS)
            else:
                print('非法参数')
                self.finish(RETCODE.FAILED)
        else:
            self.finish(RETCODE.FAILED)
            print('failed')


'''
@route('user/oauth')
class UserOAuthView(UserMixin, PeeweeView):
    model = UserOAuth

    # 此部分使用拿到的数据字段来注册一个账号，包括但不限于 /新建表/ - 用户校验 - 用户创建
    @route.interface('POST')
    async def oauth(self):

        user_info = await self.get_user_info()
        user_info = json.loads(user_info)
        print(user_info)
        if user_info['id'] and user_info['login']:
            try:
                account = UserOAuth.get(UserOAuth.login_id == user_info['id'],
                                        UserOAuth.platform == 'github')
                print(account)
            except Exception as e:
                print("wwwwwwwwww")
                account = None
                print(e)

            if account:
                print("ccccccccccccc")
                await self.get_user(user_info)
            else:
                print("aaaaaaaaaaa")
                await self.create_user(user_info)

        else:
            return None

    """ get user info """
    async def get_user_info(self):
        async with aiohttp.ClientSession() as session:
            url = "http://118.25.43.194:8080/api/oauth/return"
            async with session.get(url) as response:
                return await response.text()

    """ create user """
    async def create_user(self, user_info):
        info = User.gen_password_and_salt("123456")
        new_user = [{
            'email': "123@qq.com",
            'nickname': user_info['login'],
            'time': int(time.time()),
            'group': 1,
            'key_time': int(time.time())
        }]
        for k in info.keys():
            new_user[0][k] = info[k]
        User.insert_many(new_user).execute()  # 创建用户

        print('test')

        User.get(User.email == "123@qq.com", User.nickname == user_info['login'])
        new_oauth = [{
            'login_id': user_info['login_id'],
            'platform': "github",
        }]
        # info = UserOAuth.insert_many(new_oauth, returning=True).execute()  # 插入oauth数据
        # info = await self._sql.insert(new_oauth, returning=True)

    """ get user """
    async def get_user(self, user_info):
        pass
'''

# 通过 access_token 拿到的数据字段
# {'login': 'ly-nina',
# 'id': 17906006,
# 'avatar_url': 'https://avatars1.githubusercontent.com/u/17906006?v=4',
# 'gravatar_id': '',
# 'url': 'https://api.github.com/users/ly-nina',
# 'html_url': 'https://github.com/ly-nina',
# 'followers_url': 'https://api.github.com/users/ly-nina/followers',
# 'following_url': 'https://api.github.com/users/ly-nina/following{/other_user}',
# 'gists_url': 'https://api.github.com/users/ly-nina/gists{/gist_id}',
# 'starred_url': 'https://api.github.com/users/ly-nina/starred{/owner}{/repo}',
# 'subscriptions_url': 'https://api.github.com/users/ly-nina/subscriptions',
# 'organizations_url': 'https://api.github.com/users/ly-nina/orgs',
# 'repos_url': 'https://api.github.com/users/ly-nina/repos', 'events_url': https://api.github.com/users/ly-nina/events{/privacy}',
# 'received_events_url': 'https://api.github.com/users/ly-nina/received_events',
# 'type': 'User',
# 'site_admin': False,
# 'name': None,
# 'company': None,
# 'blog': '',
# 'location': None,
# 'email': None,
# 'hireable': None,
# 'bio': None,
# 'public_repos': 11,
# 'public_gists': 0,
# 'followers': 0,
# 'following': 0,
# 'created_at': '2016-03-17T13:49:08Z',
# 'updated_at': '2018-05-07T11:09:03Z'
# }
