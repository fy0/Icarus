from crud.schemas.board import Board
from crud.roles.r30_normal_user import normal_user
from crud.schemas.topic import Topic
from crud.schemas.user import User
from crud.schemas.wiki_article import WikiArticle
from pycurd.permission import RoleDefine, TablePerm, A


super_user = RoleDefine({
    Topic: TablePerm({
        Topic.state: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Topic.visible: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Topic.time: {A.CREATE, A.READ},
        Topic.user_id: {A.QUERY, A.CREATE, A.READ},
        Topic.title: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Topic.board_id: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Topic.content: {A.CREATE, A.READ, A.UPDATE},
        Topic.awesome: {A.QUERY, A.READ, A.UPDATE},
        Topic.weight: {A.QUERY, A.READ, A.UPDATE},
        Topic.sticky_weight: {A.READ, A.UPDATE},
    }),
    WikiArticle: TablePerm({
        WikiArticle.state: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        WikiArticle.visible: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        WikiArticle.time: {A.CREATE, A.READ},
        WikiArticle.user_id: {A.QUERY, A.CREATE, A.READ},
        WikiArticle.title: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        WikiArticle.ref: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        WikiArticle.content: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
    }),
    Board: TablePerm({
        Board.state: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Board.visible: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Board.time: {A.CREATE, A.READ},
        Board.user_id: {A.QUERY, A.CREATE, A.READ},
        Board.name: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Board.brief: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Board.desc: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Board.weight: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Board.color: {A.CREATE, A.READ, A.UPDATE},
        Board.category: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Board.parent_id: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        Board.can_post_rank: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
    }),
    User: TablePerm({
        User.state: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        User.visible: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        User.time: {A.CREATE, A.READ},
        User.user_id: {A.QUERY, A.CREATE, A.READ},
        User.password: {A.UPDATE},
        User.email: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        User.nickname: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        User.credit: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        User.repute: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        User.access_time: {A.READ},
        User.last_check_in_time: {A.READ},
        User.is_wiki_editor: {A.QUERY, A.READ, A.UPDATE},
        User.is_board_moderator: {A.QUERY, A.READ, A.UPDATE},
        User.is_forum_master: {A.QUERY, A.READ, A.UPDATE},
    }),
}, based_on=normal_user)
