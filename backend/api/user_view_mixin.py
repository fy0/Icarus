from typing import Union, Type

from slim.base.user import BaseAccessTokenUserViewMixin, BaseUser
from slim.utils import sentinel

from model.user import User
from model.user_token import UserToken


class UserViewMixin(BaseAccessTokenUserViewMixin):
    """ 用户Mixin，用于与View """
    def get_user_by_token(self: Union['BaseUserViewMixin', 'BaseView'], token) -> Type[BaseUser]:
        t = UserToken.get_by_token(token)
        if t: return User.get_by_pk(t.user_id)

    async def setup_user_token(self, user_id, key=None, expires=30):
        """ setup user token """
        t = UserToken.new(user_id)
        await t.init(self)
        return t

    def teardown_user_token(self: Union['BaseUserViewMixin', 'BaseView'], token=sentinel):
        """ invalidate the token here"""
        u: User = self.current_user
        if u:
            if token is None:
                # clear all tokens
                UserToken.delete().where(UserToken.user_id == u.id).execute()
                return

            if token is sentinel:
                # clear current token
                try:
                    token = to_bin(self.get_user_token())
                except binascii.Error:
                    return
            UserToken.delete().where(UserToken.user_id == u.id, UserToken.id == token).execute()
