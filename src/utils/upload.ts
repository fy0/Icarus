// browser only
import { retcode } from 'slim-tools'

let api: any = null
let store: any = null

if (process.browser) {
  (window as any).onNuxtReady(({ $store }: any) => {
    store = $store
    api = $store.app.$api
  })
}

let uploadKeyTime = 0
let uploadToken = ''

export function staticUrl (key: string) {
  return `${store.getters.BACKEND_CONFIG.UPLOAD_STATIC_HOST}/${key}`
}

export async function asyncGetUploadToken (isAvatarUpload = false) {
  if (isAvatarUpload) {
    const ret = await api.upload.qn_token('user', isAvatarUpload)
    if (ret.code === retcode.SUCCESS) {
      return ret.data
    }
    return null
  }

  const offset = store.getters.BACKEND_CONFIG.UPLOAD_QINIU_DEADLINE_OFFSET - 2 * 60
  const now = Date.parse((new Date()).toISOString()) / 1000
  // 若 token 的有效时间降至，那么申请一个新的（2min余量）
  if ((now - uploadKeyTime) > offset) {
    const ret = await api.upload.qn_token('user')
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
