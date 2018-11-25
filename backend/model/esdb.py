import os
import time

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import MultiMatch
from slim.utils import to_hex

from model._post import POST_TYPES, POST_STATE, POST_VISIBLE
from model.topic import Topic
from model.user import User
from model.wiki import WikiArticle

es = Elasticsearch(hosts=[{
    "host": "localhost",
    "port": 9200
}])

INDEX_NAME = "icarus-index"


def create_index():
    es.indices.create(index=INDEX_NAME, ignore=400)
    es.indices.put_mapping(index=INDEX_NAME, body={
        "properties": {
            # type, user_id
            "state": {
                "type": "integer",
            },
            "visible": {
                "type": "integer",
            },
            "time": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            },
            # 加入索引的时间
            "indexed_time": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            },

            "title": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word"
            },
            "user_nickname": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word"
            },
            "content": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word"
            }
        }
    }, doc_type='doc')


def get_post_base_body(post):
    return {
        'state': post.state,
        'visible': post.visible,
        'time': post.time * 1000,
        'user_id': to_hex(post.user_id),
        'indexed_time': int(time.time() * 1000),

        'type': post.get_post_type(),
        'title': post.get_title()
    }


def es_update_topic(id):
    post: Topic = Topic.get_by_id(id)
    if not post: return
    u: User = User.get_by_id(post.user_id)
    if not u: return

    body = get_post_base_body(post)
    body.update({
        'user_nickname': u.nickname,
        'content': post.content,
    })
    es.index(
        index=INDEX_NAME,
        doc_type="doc",
        id=to_hex(post.id),
        body=body
    )


def es_update_wiki(id):
    post: WikiArticle = WikiArticle.get_by_id(id)
    if not post: return
    if post.flag: return
    u: User = User.get_by_id(post.user_id)
    if not u: return

    body = get_post_base_body(post)
    body.update({
        'user_nickname': u.nickname,
        'content': post.content,
    })
    es.index(
        index=INDEX_NAME,
        doc_type="doc",
        id=to_hex(post.id),
        body=body
    )


def doc_search(text, page_size=30, offset=0, *, visible_min=POST_VISIBLE.NOT_IN_LIST, visible_max=POST_VISIBLE.NORMAL):
    q = MultiMatch(query=text, fields=['title', 'content'])
    q2 = Q({
        'range': {
            'state': {
                'gte': POST_STATE.CLOSE,
                'lte': POST_STATE.NORMAL
            }
        }
    }) | Q({
        'range': {
            'visible': {
                'gte': visible_min,
                'lte': visible_max
            }
        }
    })

    s = Search(using=es, index=INDEX_NAME) \
        .query(q & q2) \
        .source(exclude=["content"]) \
        .highlight('content', fragment_size=50)[offset : offset+page_size]

    return s.execute()


def update_all(reset=False):
    if reset:
        es.indices.delete(index=INDEX_NAME)
        create_index()

    for i in Topic.select(Topic.id):
        print('topic', i.id.tobytes())
        es_update_topic(i.id)

    for i in WikiArticle.select(WikiArticle.id):
        print('wiki', i.id.tobytes())
        es_update_wiki(i.id)


if __name__ == '__main__':
    # update_all(reset=True)
    val = doc_search('1111')
    # val.hits.total 个数
    # val.timed_out 是否超时
    # val.took 花费时间
    print(val)
