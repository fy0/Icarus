from typing import Optional

from crud.schemas._post import Post


class WikiArticle(Post):
    title: str = None
    content: str = None
    ref: Optional[str]
    flag: Optional[int]
