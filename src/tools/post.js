import api from '../netapi.js'
import state from '@/state.js'

$.makePostLinkData = function (type, item) {
    let title = item.name || item.title || item.nickname
    item['post_type'] = type
    item['post_title'] = title // 一个虚假的列，在post-link中高于其他声明
    return item
}

$.getBasePostsByIDs = async function (func, items, role = null) {
    let PT = state.misc.POST_TYPES
    let idsByType = {}

    for (let i of items) {
        let infoLst = await func(i)
        // infoLst: [{id: xxx, type: xxx}, ...]
        for (let info of infoLst) {
            if (!idsByType[info.type]) {
                idsByType[info.type] = []
            }
            idsByType[info.type].push(info.id)
        }
    }

    let posts = {}
    let doRequest = async (name, type, ex = []) => {
        let ids = idsByType[type]
        if (ids && ids.length) {
            let retPost = await api[name].list({
                'id.in': JSON.stringify(ids),
                'select': ['id', 'time', 'user_id'].concat(ex)
            }, 1, null, role)
            if (retPost.code === api.retcode.SUCCESS) {
                for (let i of retPost.data.items) {
                    posts[i.id] = $.makePostLinkData(type, i)
                }
            }
        }
    }

    await doRequest('user', PT.USER, ['nickname'])
    await doRequest('board', PT.BOARD, ['name'])
    await doRequest('topic', PT.TOPIC, ['title'])
    await doRequest('wiki', PT.WIKI, ['title', 'ref'])
    await doRequest('comment', PT.COMMENT)
    return posts
}
