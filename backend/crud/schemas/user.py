from typing import Optional, List, Callable, Awaitable

from crud.schemas._post import Post
from model.user_model import USER_GROUP, UserModel
from pycurd.crud.base_crud import PermInfo
from pycurd.query import QueryInfo
from pycurd.types import IDList
from pycurd.values import ValuesToWrite


class User(Post):
    email: Optional[str]
    phone: Optional[str]
    nickname: Optional[str]
    password: bytes
    salt: bytes
    biology: Optional[str]
    avatar: Optional[str]
    type: int = 0
    url: Optional[str]
    location: Optional[str]

    # level = IntegerField(index=True)  # 用户级别
    group: int = USER_GROUP.NORMAL

    is_wiki_editor: bool = False
    is_board_moderator: bool = False
    is_forum_master: bool = False

    access_time: Optional[int]
    last_check_in_time: Optional[int]
    check_in_his: int = 0

    number: int
    credit: int = 0
    exp: int = 0
    repute: int = 0
    ip_registered: str # 注册IP

    # ref_github = TextField(null=True)
    # ref_zhihu = TextField(null=True)
    # ref_weibo = TextField(null=True)

    is_new_user: bool = True
    phone_verified: bool = False
    change_nickname_chance: int = 0
    reset_key: Optional[bytes]

    @classmethod
    async def on_update(
        cls,
        info: QueryInfo,
        values: 'ValuesToWrite',
        when_before_update: List[Callable[[IDList], Awaitable]],
        when_complete: List[Callable[[], Awaitable]],
        perm: PermInfo = None
    ):
        if 'password' in values:
            ret = UserModel.gen_password_and_salt(values['password'])
            values.update(ret)
