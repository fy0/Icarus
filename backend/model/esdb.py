import os
import time

import elasticsearch

import config
from model.comment_model import CommentModel
from slim.utils import to_hex

from model._post import POST_TYPES, POST_STATE, POST_VISIBLE
from model.topic_model import TopicModel
from model.user_model import UserModel
from model.wiki import WikiArticleModel

INDEX_NAME = config.ES_INDEX_NAME
if config.SEARCH_ENABLE:
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import Search, Q
    from elasticsearch_dsl.query import MultiMatch

    es = Elasticsearch(hosts=config.ES_HOSTS)


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
    main_category = None
    post_type = post.get_post_type()
    title = post.get_title()

    if post_type in {POST_TYPES.TOPIC, POST_TYPES.BOARD}:
        main_category = 'forum'
    elif post_type in {POST_TYPES.WIKI,}:
        main_category = 'wiki'

    if post_type is POST_TYPES.COMMENT:
        post: CommentModel
        if post.related_type in {POST_TYPES.TOPIC, POST_TYPES.BOARD}:
            main_category = 'forum'
        elif post_type in {POST_TYPES.WIKI, }:
            main_category = 'wiki'

    return {
        'id': to_hex(post.id),
        'state': post.state,
        'visible': post.visible,
        'time': post.time * 1000,
        'user_id': to_hex(post.user_id),

        'type': post_type,
        'title': title,

        # 扩展
        'indexed_time': int(time.time() * 1000),
        'main_category': main_category
    }


def es_update_topic(id):
    post: TopicModel = TopicModel.get_by_id(id)
    if not post: return
    u: UserModel = UserModel.get_by_id(post.user_id)
    if not u: return

    body = get_post_base_body(post)
    body.update({
        'user_nickname': u.nickname,
        'content': post.content,
        'brief': post.content[:100]
    })
    es.index(
        index=INDEX_NAME,
        doc_type="doc",
        id=to_hex(post.id),
        body=body
    )


def es_update_wiki(id):
    post: WikiArticleModel = WikiArticleModel.get_by_id(id)
    if not post: return
    if post.flag: return
    u: UserModel = UserModel.get_by_id(post.user_id)
    if not u: return

    body = get_post_base_body(post)
    body.update({
        'user_nickname': u.nickname,
        'content': post.content,
        'ref': post.ref,
        'brief': post.content[:100]
    })
    es.index(
        index=INDEX_NAME,
        doc_type="doc",
        id=to_hex(post.id),
        body=body
    )


def es_update_comment(id):
    post: CommentModel = CommentModel.get_by_id(id)
    if not post: return
    u: UserModel = UserModel.get_by_id(post.user_id)
    if not u: return

    p = POST_TYPES.get_post(post.related_type, post.related_id)

    body = get_post_base_body(post)
    body.update({
        'user_nickname': u.nickname,
        'content': post.content,
        'brief': post.content[:100],

        'related_title': p.get_title() if p else None,
        'related_type': post.related_type,
        'related_id': to_hex(post.related_id)
    })
    es.index(
        index=INDEX_NAME,
        doc_type="doc",
        id=to_hex(post.id),
        body=body
    )


def doc_search(keywords, page_size=30, offset=0, *, visible_min=POST_VISIBLE.NOT_IN_LIST, visible_max=POST_VISIBLE.NORMAL):
    q = MultiMatch(query=keywords, fields=['title', 'content'])
    q2 = Q({
        'range': {
            'state': {
                'gte': POST_STATE.CLOSE,
                'lte': POST_STATE.NORMAL
            }
        }
    }) & Q({
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
        .highlight_options(encoder='html') \
        .highlight('title', fragment_size=50) \
        .highlight('content', fragment_size=100)[offset: offset+page_size]

    return s.execute()


def update_all(reset=False):
    if reset:
        try:
            es.indices.delete(index=INDEX_NAME)
        except elasticsearch.exceptions.NotFoundError:
            pass
        create_index()

    for i in TopicModel.select(TopicModel.id):
        print('topic', to_hex(i.id))
        es_update_topic(i.id)

    for i in WikiArticleModel.select(WikiArticleModel.id):
        print('wiki', to_hex(i.id))
        es_update_wiki(i.id)

    for i in CommentModel.select(CommentModel.id):
        print('comment', to_hex(i.id))
        es_update_comment(i.id)


if __name__ == '__main__':
    # update_all(reset=True)
    val = doc_search('1111')
    # val.hits.total 个数
    # val.timed_out 是否超时
    # val.took 花费时间
    print(val)
