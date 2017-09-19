
import 'whatwg-fetch'
import config from './config.js'

let remote = config.remote

function paramSerialize (obj) {
    let str = []
    for (let i of Object.keys(obj)) {
        str.push(encodeURIComponent(i) + '=' + encodeURIComponent(obj[i]))
    }
    return str.join('&')
}

async function doFetch (url, method, params, data = null) {
    let fetchParams = {
        method: method,
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }
    if (params) url += `?${paramSerialize(data)}`
    if (method === 'POST') fetchParams.body = JSON.stringify(data)
    return fetch(url, fetchParams)
}

async function nget (url, params) { return doFetch(url, 'GET', params) }
async function npost (url, params, data) { return doFetch(url, 'POST', params, data) }

let retcode = {
    SUCCESS: 0
}

let retinfo = {
    [retcode.SUCCESS]: '操作已成功完成'
}

class SlimViewRequest {
    constructor (path) {
        this.path = path
        this.urlPrefix = `${remote.API_SERVER}/api/${path}`
    }

    async get (params) {
        return await nget(`${this.urlPrefix}/get`, params)
    }

    async list (params, page = 1, size = null) {
        let url = `${this.urlPrefix}/list/${page}`
        if (size) url += `/${size}`
        return await nget(url, params)
    }

    async set (params, data) {
        return await npost(`${this.urlPrefix}/set`, params, data)
    }

    async new (data) {
        return await npost(`${this.urlPrefix}/new`, null, data)
    }

    async delete (params) {
        return await npost(`${this.urlPrefix}/delete`, params)
    }
}

export default {
    retcode,
    retinfo,

    /** 获取综合信息 */
    misc: async function () {
        return await nget(`${remote.API_SERVER}/api/misc/info`)
    },

    user: new SlimViewRequest('user')
}
