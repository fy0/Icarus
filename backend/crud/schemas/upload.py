from typing import Optional, Any

from crud.schemas._post import Post
from pycurd.const import QUERY_OP_COMPARE
from pycurd.query import ConditionExpr


class Upload(Post):
    key: str = None
    size: int = None
    ext: Optional[str]
    type_name: Optional[str]
    image_info: Optional[Any]
    filename: Optional[str]
    source: Optional[str]

    @classmethod
    async def on_query(cls, info: 'QueryInfo', perm: 'PermInfo' = None):
        from crud.roles import ordinary_roles

        if perm and perm.role in ordinary_roles:
            info.conditions.items.append(
                ConditionExpr(cls.user_id, QUERY_OP_COMPARE.EQ, perm.user.id)
            )
