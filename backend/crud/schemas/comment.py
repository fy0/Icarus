from typing import Optional

from crud.schemas._post import Post


class Comment(Post):
    related_id: bytes = None
    related_type: int = None
    reply_to_cmt_id: Optional[bytes]
    content: str = None
    post_number: Optional[int]
