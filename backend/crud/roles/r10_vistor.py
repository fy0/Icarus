from crud.schemas.board import Board
from crud.schemas.comment import Comment
from crud.schemas.manage_log import ManageLog
from crud.schemas.post_stats import PostStats
from crud.schemas.topic import Topic
from crud.schemas.wiki_article import WikiArticle
from crud.schemas.user import User

from pycurd.permission import RoleDefine, TablePerm, A


visitor = RoleDefine({
    User: TablePerm({
        User.id: {A.QUERY, A.READ},
        User.state: {A.READ},
        User.visible: {A.READ},
        User.time: {A.READ},
        User.user_id: {A.QUERY, A.READ},

        User.email: {A.CREATE},
        User.phone: {A.CREATE},
        User.nickname: {A.READ, A.CREATE},

        User.biology: {A.READ},
        User.avatar: {A.READ},
        User.type: {A.READ},
        User.url: {A.READ},
        User.location: {A.READ},
        User.group: {A.READ},

        User.is_wiki_editor: {A.READ},
        User.is_board_moderator: {A.READ},
        User.is_forum_master: {A.READ},

        User.access_time: {A.READ},
        User.number: {A.READ},
        User.exp: {A.READ},
        User.credit: {A.READ},
        User.repute: {A.READ},
    }),
    Topic: TablePerm({
        Topic.id: {A.QUERY, A.READ},
        Topic.state: {A.READ},
        Topic.visible: {A.READ},
        Topic.time: {A.READ},
        Topic.user_id: {A.QUERY, A.READ},

        Topic.title: {A.READ},
        Topic.board_id: {A.QUERY, A.READ},
        Topic.edit_count: {A.READ},
        Topic.edit_time: {A.READ},
        Topic.last_edit_user_id: {A.READ},
        Topic.content: {A.READ},
        Topic.awesome: {A.READ},
        Topic.sticky_weight: {A.QUERY, A.READ},
        Topic.weight: {A.READ},
        Topic.update_time: {A.READ},
    }),
    WikiArticle: TablePerm({
        WikiArticle.id: {A.QUERY, A.READ},
        WikiArticle.state: {A.READ},
        WikiArticle.visible: {A.READ},
        WikiArticle.time: {A.READ},
        WikiArticle.user_id: {A.QUERY, A.READ},

        WikiArticle.title: {A.READ},
        WikiArticle.ref: {A.QUERY, A.READ},
        WikiArticle.content: {A.READ},
        WikiArticle.flag: {A.QUERY, A.READ},
    }),
    Board: TablePerm({
        Board.id: {A.QUERY, A.READ},
        Board.state: {A.READ},
        Board.visible: {A.READ},
        Board.time: {A.READ},
        Board.user_id: {A.QUERY, A.READ},

        Board.name: {A.READ},
        Board.brief: {A.READ},
        Board.desc: {A.READ},
        Board.weight: {A.QUERY, A.READ},
        Board.color: {A.READ},
        Board.category: {A.READ},
        Board.parent_id: {A.QUERY, A.READ},
        Board.can_post_rank: {A.QUERY, A.READ},
    }),
    Comment: TablePerm({
        Comment.id: {A.QUERY, A.READ},
        Comment.state: {A.READ},
        Comment.visible: {A.READ},
        Comment.time: {A.READ},
        Comment.user_id: {A.QUERY, A.READ},

        Comment.related_id: {A.QUERY, A.READ},
        Comment.related_type: {A.QUERY, A.READ},
        Comment.reply_to_cmt_id: {A.QUERY, A.READ},
        Comment.content: {A.READ},
        Comment.post_number: {A.READ},
    }),
    PostStats: TablePerm({
        PostStats.id: {A.QUERY, A.READ},
    },
        default_perm={A.READ},
        append_perm={A.UPDATE},
        allow_delete=True
    ),
    ManageLog: TablePerm({
        ManageLog.related_type: {A.QUERY, A.READ},
        ManageLog.related_id: {A.QUERY, A.READ},
    },
        default_perm={A.READ}
    ),
})
