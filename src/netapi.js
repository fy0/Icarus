
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

async function doFetch (url, method, params, data = null, role = null) {
    let fetchParams = {
        method: method,
        mode: 'cors',
        credentials: 'include',
        headers: {
            'Role': role,
            'Accept': 'application/json'
            // 'Content-Type': 'application/json;'
        }
    }
    if (params) url += `?${paramSerialize(params)}`
    // if (method === 'POST') fetchParams.body = JSON.stringify(data)
    if (method === 'POST') fetchParams.body = buildFormData(data)
    return fetch(url, fetchParams)
}

async function nget (url, params, role = null) { return (await doFetch(url, 'GET', params, null, role)).json() }
async function npost (url, params, data, role = null) { return (await doFetch(url, 'POST', params, data, role)).json() }

class SlimViewRequest {
    constructor (path) {
        this.path = path
        this.urlPrefix = `${remote.API_SERVER}/api/${path}`
    }

    async get (params, role = null) {
        return await nget(`${this.urlPrefix}/get`, params, role)
    }

    async list (params, page = 1, size = null, role = null) {
        let url = `${this.urlPrefix}/list/${page}`
        if (size) url += `/${size}`
        return await nget(url, params, role)
    }

    async set (params, data, role = null) {
        return await npost(`${this.urlPrefix}/set`, params, data, role)
    }

    async new (data, role = null) {
        return await npost(`${this.urlPrefix}/new`, null, data, role)
    }

    async delete (params, role = null) {
        return await npost(`${this.urlPrefix}/delete`, params, null, role)
    }
}

class UserViewRequest extends SlimViewRequest {
    async signin (data) {
        return await npost(`${this.urlPrefix}/signin`, null, data)
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

    user: new UserViewRequest('user'),
    board: new SlimViewRequest('board')
}
