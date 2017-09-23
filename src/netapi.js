
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

function buildFormData (obj) {
    let formData = new FormData()
    for (let [k, v] of Object.entries(obj)) {
        formData.append(k, v)
    }
    return formData
}

async function doFetch (url, method, params, data = null) {
    let fetchParams = {
        method: method,
        mode: 'cors',
        credentials: 'include',
        headers: {
            'Accept': 'application/json'
            // 'Content-Type': 'multipart/form-data;'
        }
    }
    if (params) url += `?${paramSerialize(params)}`
    if (method === 'POST') fetchParams.body = buildFormData(data)
    return await fetch(url, fetchParams)
}

async function nget (url, params) { return await doFetch(url, 'GET', params) }
async function npost (url, params, data) { return doFetch(url, 'POST', params, data) }

class SlimViewRequest {
    constructor (path) {
        this.path = path
        this.urlPrefix = `${remote.API_SERVER}/api/${path}`
    }

    async _wrap (promise) {
        // 为什么 method 与 function 中的 await 行为不一致？
        let ret = await promise
        return await ret.json()
    }

    async get (params) {
        return this._wrap(await nget(`${this.urlPrefix}/get`, params))
    }

    async list (params, page = 1, size = null) {
        let url = `${this.urlPrefix}/list/${page}`
        if (size) url += `/${size}`
        return this._wrap(await nget(url, params))
    }

    async set (params, data) {
        return this._wrap(await npost(`${this.urlPrefix}/set`, params, data))
    }

    async new (data) {
        return this._wrap(await npost(`${this.urlPrefix}/new`, null, data))
    }

    async delete (params) {
        return this._wrap(await npost(`${this.urlPrefix}/delete`, params))
    }
}

let retcode = {
    SUCCESS: 0
}

let retinfo = {
    [retcode.SUCCESS]: '操作已成功完成'
}

export default {
    retcode,
    retinfo,

    /** 获取综合信息 */
    misc: async function () {
        return await nget(`${remote.API_SERVER}/api/misc/info`)
    },

    user: new SlimViewRequest('user'),
    board: new SlimViewRequest('board')
}
