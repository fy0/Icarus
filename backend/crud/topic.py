from typing import Optional
from crud.user import Post


class Topic(Post):
    title: str
    board_id: bytes

    edit_count: int
    edit_time: Optional[int]
    last_edit_user_id: Optional[bytes]
    content: str

    awesome: int = 0
    sticky_weight: int = 0
    weight: int = 0
    update_time: Optional[int]
