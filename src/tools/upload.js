// browser only
let api = null
let store = null

import { retcode } from 'slim-tools'

if (process.browser) {
    window.onNuxtReady(({ $store }) => {
        store = $store
        api = $store.app.$api
    })
}

let uploadKeyTime = 0
let uploadToken = ''

$.staticUrl = function (key) {
    return `${store.getters.BACKEND_CONFIG.UPLOAD_STATIC_HOST}/${key}`
}

$.asyncGetUploadToken = async function (isAvatarUpload = false) {
    if (isAvatarUpload) {
        const ret = await api.upload.token('user', isAvatarUpload)
        if (ret.code === retcode.SUCCESS) {
            return ret.data
        }
        return null
    }

    const offset = store.getters.BACKEND_CONFIG.UPLOAD_QINIU_DEADLINE_OFFSET - 2 * 60
    const now = Date.parse(new Date()) / 1000
    // 若 token 的有效时间降至，那么申请一个新的（2min余量）
    if ((now - uploadKeyTime) > offset) {
        const ret = await api.upload.token('user')
        if (ret.code === retcode.SUCCESS) {
            uploadKeyTime = now
            uploadToken = ret.data
        } else {
            // 异常情况
            return null
        }
    }
    return uploadToken
}
