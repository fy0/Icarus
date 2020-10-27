from crud.roles.r30_normal_user import normal_user
from crud.schemas.wiki_article import WikiArticle
from pycurd.permission import RoleDefine, TablePerm, A


wiki_editor = RoleDefine({
    WikiArticle: TablePerm({
        WikiArticle.state: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        WikiArticle.visible: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        WikiArticle.time: {A.CREATE, A.READ},
        WikiArticle.user_id: {A.QUERY, A.CREATE, A.READ},
        WikiArticle.title: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        WikiArticle.ref: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
        WikiArticle.content: {A.QUERY, A.CREATE, A.READ, A.UPDATE},
    }),
}, based_on=normal_user)
