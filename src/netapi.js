import axios from 'axios'
import config from './config.js'

axios.defaults.retry = 2
axios.defaults.retryDelay = 300

let remote = config.remote
const backend = axios.create({
    baseURL: remote.API_SERVER,
    timeout: 5000,
    withCredentials: true,
    headers: {
        'Accept': 'application/json'
    }
})

backend.interceptors.response.use(function (response) {
    // Do something with response data
    return response.data
}, function (error) {
    // Do something with response error
    return Promise.reject(error)
})

function paramSerialize (obj) {
    let str = []
    for (let i of Object.keys(obj)) {
        str.push(encodeURIComponent(i) + '=' + encodeURIComponent(obj[i]))
    }
    return str.join('&')
}

function buildFormData (obj) {
    if (!obj) return
    let formData = new FormData()
    for (let [k, v] of Object.entries(obj)) {
        formData.append(k, v)
    }
    return formData
}

function filterValues (filter, data) {
    let keys = null
    if (_.isArray(filter)) keys = new Set(filter)
    else if (_.isSet(filter)) keys = filter
    else if (_.isFunction(filter)) return filter(data)

    let ret = {}
    for (let i of Object.keys(data)) {
        if (keys.has(i)) {
            ret[i] = data[i]
        }
    }
    return ret
}

export function createAPIRequester (ctx) {
    function getAccessToken () {
        if (process.browser) {
            return localStorage.getItem('t')
        }
    }

    function saveAccessToken (token) {
        if (process.browser) {
            localStorage.setItem('t', token)
        }
    }

    async function doRequest (url, method, params, data = null, role = null) {
        let headers = {}
        let token = getAccessToken()

        if (token) {
            // 设置 access token
            headers['AccessToken'] = token
        }

        if (role) {
            // 不然的话服务器回收到一个 'null' 的 str
            headers['Role'] = role
        }

        if (params) url += `?${paramSerialize(params)}`
        return backend.request({
            url,
            method,
            headers,
            data: buildFormData(data)
        })
        // if (method === 'POST') reqParams.body = JSON.stringify(data)
    }

    async function nget (url, params, role = null) { return doRequest(url, 'GET', params, null, role) }
    async function npost (url, params, data, role = null) { return doRequest(url, 'POST', params, data, role) }

    class SlimViewRequest {
        constructor (path) {
            this.path = path
            this.urlPrefix = `/api/${path}`
        }

        async get (params, role = null) {
            if (params && params.loadfk) {
                params.loadfk = JSON.stringify(params.loadfk)
            }
            return nget(`${this.urlPrefix}/get`, params, role)
        }

        async list (params, page = 1, size = null, role = null) {
            if (params && params.loadfk) {
                params.loadfk = JSON.stringify(params.loadfk)
            }
            let url = `${this.urlPrefix}/list/${page}`
            if (size) url += `/${size}`
            return nget(url, params, role)
        }

        async set (params, data, role = null, filter = null) {
            if (filter) data = filterValues(filter, data)
            return npost(`${this.urlPrefix}/update`, params, data, role)
        }

        async update (params, data, role = null, filter = null) {
            if (filter) data = filterValues(filter, data)
            return npost(`${this.urlPrefix}/update`, params, data, role)
        }

        async new (data, role = null, filter = null) {
            if (filter) data = filterValues(filter, data)
            return npost(`${this.urlPrefix}/new`, null, data, role)
        }

        async delete (params, role = null) {
            return npost(`${this.urlPrefix}/delete`, params, null, role)
        }
    }

    class UserViewRequest extends SlimViewRequest {
        async signin (data) {
            let ret = await npost(`${this.urlPrefix}/signin`, null, data)
            if (ret.code === retcode.SUCCESS) {
                saveAccessToken(ret.data.access_token)
            }
            return ret
        }

        // 准备进行邮件注册
        async requestSignupByEmail (data) {
            return npost(`${this.urlPrefix}/request_signup_by_email`, null, data)
        }

        // 拿到激活码，进行邮件注册
        async signupByEmail (email, code) {
            return npost(`${this.urlPrefix}/signup_by_email`, null, { email, code })
        }

        async checkIn () {
            return npost(`${this.urlPrefix}/check_in`)
        }

        /* eslint-disable camelcase */
        async changePassword ({ old_password, password }) {
            return npost(`${this.urlPrefix}/change_password`, null, { old_password, password })
        }

        // 申请重置密码
        async requestPasswordReset (nickname, email) {
            return npost(`${this.urlPrefix}/request_password_reset`, null, { nickname, email })
        }

        // 修改昵称
        async changeNickname (nickname) {
            return npost(`${this.urlPrefix}/change_nickname`, null, { nickname })
        }

        // 验证重置密码
        async validatePasswordReset (uid, code, password) {
            return npost(`${this.urlPrefix}/validate_password_reset`, null, { uid, code, password })
        }

        async signout () {
            return npost(`${this.urlPrefix}/signout`)
        }
    }

    class NotifViewRequest extends SlimViewRequest {
        async count () {
            return nget(`${this.urlPrefix}/count`, null)
        }

        async setRead () {
            return npost(`${this.urlPrefix}/set_read`, null)
        }
    }

    class UploadViewRequest extends SlimViewRequest {
        async token (role, isAvatar) {
            let params = {}
            if (isAvatar) {
                params['is_avatar'] = isAvatar
            }
            return npost(`${this.urlPrefix}/token`, params, null, role)
        }
    }

    class WikiViewRequest extends SlimViewRequest {
        async random () {
            return nget(`${this.urlPrefix}/random`, null)
        }
    }

    class SearchViewRequest extends SlimViewRequest {
        async search (keywords) {
            return npost(`${this.urlPrefix}/search`, null, { keywords })
        }
    }

    // http://localhost:9999/api/user/oauth/get_oauth_url 取url链接
    class Oauth {
        async getUrl (website) {
            if (website === 'github') {
                let info = await nget(`/api/user/oauth/get_oauth_url`)
                return info['data']['url']
            } else if (website === 'qq') {
                return nget()
            } else if (website === 'sina') {
                return nget()
            }
        }
        async oauthUpdate (userdata) {
            let ret = await npost(`/api/user/oauth/update`, null, userdata, null)
            if (ret.code === retcode.SUCCESS) {
                return retcode.SUCCESS
            }
            return retcode.FAILED
        }
        async send (code) {
            let ret = await nget(`/api/user/oauth/get_user_data`, { 'code': code })
            if (ret.code !== retcode.FAILED) {
                let oauthState = ret['data']['state']
                if (oauthState === 50) {
                    if (ret['code'] === retcode.SUCCESS) {
                        saveAccessToken(ret.data.access_token)
                        return ret
                    }
                } else {
                    return { 'code': -1, 'data': ret }
                }
            } else {
                return { 'code': retcode.FAILED, 'data': null }
            }
        }
    }

    let retcode = {
        SUCCESS: 0,
        FAILED: -255
    }

    let retinfo = {
        [retcode.SUCCESS]: '操作已成功完成'
    }

    return {
        retcode,
        retinfo,
        saveAccessToken,

        /** 获取综合信息 */
        misc: async function () {
            return nget(`/api/misc/info`)
        },

        /** 周期请求 */
        tick: async function (auid) {
            return nget(`/api/misc/tick`, { auid })
        },

        user: new UserViewRequest('user'),
        board: new SlimViewRequest('board'),
        topic: new SlimViewRequest('topic'),
        stats: new SlimViewRequest('stats'),
        comment: new SlimViewRequest('comment'),
        notif: new NotifViewRequest('notif'),
        upload: new UploadViewRequest('upload'),
        logManage: new NotifViewRequest('log/manage'),
        wiki: new WikiViewRequest('wiki'),
        search: new SearchViewRequest('search'),

        Oauth: new Oauth()
    }
}
