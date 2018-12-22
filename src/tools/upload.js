import api from '../netapi.js'
import store from '@/store/index'

let uploadKeyTime = 0
let uploadToken = ''

$.staticUrl = function (key) {
    return `${store.state.BACKEND_CONFIG.UPLOAD_STATIC_HOST}/${key}`
}

$.asyncGetUploadToken = async function (isAvatarUpload = false) {
    if (isAvatarUpload) {
        let ret = await api.upload.token('user', isAvatarUpload)
        if (ret.code === api.retcode.SUCCESS) {
            return ret.data
        }
        return null
    }

    let offset = store.state.BACKEND_CONFIG.UPLOAD_QINIU_DEADLINE_OFFSET - 2 * 60
    let now = Date.parse(new Date()) / 1000
    // 若 token 的有效时间降至，那么申请一个新的（2min余量）
    if ((now - uploadKeyTime) > offset) {
        let ret = await api.upload.token('user')
        if (ret.code === api.retcode.SUCCESS) {
            uploadKeyTime = now
            uploadToken = ret.data
        } else {
            // 异常情况
            return null
        }
    }
    return uploadToken
}
