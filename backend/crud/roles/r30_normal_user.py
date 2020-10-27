from crud.schemas.comment import Comment
from crud.schemas.notif import Notification
from crud.roles.r20_inactive_user import inactive_user
from crud.schemas.topic import Topic
from crud.schemas.upload import Upload
from crud.schemas.user import User
from pycurd.permission import RoleDefine, TablePerm, A


normal_user = RoleDefine({
    User: TablePerm({
        User.nickname: {A.QUERY, A.READ},
        User.group: {A.READ},
        User.biology: {A.QUERY, A.READ, A.UPDATE},
        User.avatar: {A.QUERY, A.READ},
        User.type: {A.QUERY, A.READ, A.UPDATE},
        User.url: {A.QUERY, A.READ, A.UPDATE},
        User.location: {A.QUERY, A.READ, A.UPDATE},
    }),
    Topic: TablePerm({
        Topic.title: {A.CREATE, A.READ, A.UPDATE},
        Topic.user_id: {A.CREATE, A.READ, A.UPDATE},
        Topic.board_id: {A.QUERY, A.CREATE, A.READ},
        Topic.content: {A.CREATE, A.READ, A.UPDATE},
    }),
    Comment: TablePerm({
        Comment.related_id: {A.CREATE, A.READ},
        Comment.related_type: {A.CREATE, A.READ},
        Comment.reply_to_cmt_id: {A.CREATE, A.READ},
        Comment.state: {A.READ, A.UPDATE},
        Comment.content: {A.CREATE, A.READ},
    }),
    Upload: TablePerm({
        Upload.id: {A.QUERY, A.READ},
        Upload.state: {A.READ},
        Upload.visible: {A.READ},
        Upload.time: {A.READ},
        Upload.user_id: {A.QUERY, A.READ},
        Upload.key: {A.QUERY, A.READ},
        Upload.size: {A.READ},
        Upload.type_name: {A.QUERY, A.READ},
    }),
    Notification: TablePerm({
    },
        append_perm={A.QUERY, A.CREATE, A.READ, A.UPDATE},
        allow_delete=True
    ),
}, based_on=inactive_user)
