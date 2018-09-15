import api from '../netapi.js'
import state from '@/state.js'

let uploadKeyTime = 0
let uploadToken = ''

$.staticUrl = function (key) {
    return `${state.misc.BACKEND_CONFIG.UPLOAD_STATIC_HOST}/${key}`
}

$.asyncGetUploadToken = async function (isAvatarUpload = false) {
    if (isAvatarUpload) {
        let ret = await api.upload.token('user', isAvatarUpload)
        if (ret.code === api.retcode.SUCCESS) {
            return ret.data
        }
        return null
    }

    let offset = state.misc.BACKEND_CONFIG.UPLOAD_QINIU_DEADLINE_OFFSET - 2 * 60
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
