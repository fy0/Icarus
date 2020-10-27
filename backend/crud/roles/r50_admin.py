from crud.roles.r40_super_user import super_user
from crud.schemas.user import User
from pycurd.permission import RoleDefine, TablePerm, A


admin = RoleDefine({
    User: TablePerm({
        User.group: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
    }, allow_delete=True),
}, based_on=super_user)
