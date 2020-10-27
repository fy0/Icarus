# deprecated
from crud.schemas.notif import Notification
from crud.roles.r10_vistor import visitor
from crud.schemas.user import User
from pycurd.permission import RoleDefine, TablePerm, A


inactive_user = RoleDefine({
    User: TablePerm({
        User.nickname: {A.QUERY, A.READ},
        User.group: {A.READ},
        User.access_time: {A.READ},
        User.last_check_in_time: {A.READ},
        User.check_in_his: {A.READ},
    }),
    Notification: TablePerm({
        Notification.receiver_id: {A.QUERY, A.READ},
    }),
}, based_on=visitor)

