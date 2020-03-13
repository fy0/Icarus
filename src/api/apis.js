import { SlimSQLAPI } from 'slim-tools/build/main'
import { retcode } from './misc'

export class UserAPI extends SlimSQLAPI {
    signin ({ email, password }) {
        let ret = this.request('/signin', 'POST', { data: { email, password } })
        if (ret.code === retcode.SUCCESS) {
            this.saveAccessToken(ret.data.access_token)
        }
        return ret
    }

    // 准备进行邮件注册
    async requestSignupByEmail (data) {
        return this.request('/request_signup_by_email', 'POST', { data })
    }

    // 拿到激活码，进行邮件注册
    async signupByEmail (email, code) {
        return this.request('/signup_by_email', 'POST', { data: { email, code } })
    }

    async checkIn () {
        return this.request('/check_in', 'POST')
    }

    /* eslint-disable camelcase */
    async changePassword ({ old_password, password }) {
        return this.request('/change_password', 'POST', { data: { old_password, password } })
    }

    // 申请重置密码
    async requestPasswordReset (nickname, email) {
        return this.request('/request_password_reset', 'POST', { data: { nickname, email } })
    }

    // 修改昵称
    async changeNickname (nickname) {
        return this.request('/change_nickname', 'POST', { data: { nickname } })
    }

    // 验证重置密码
    async validatePasswordReset (uid, code, password) {
        return this.request('/validate_password_reset', 'POST', { data: { uid, code, password } })
    }

    async signout () {
        return this.request('/signout', 'POST')
    }
}

export class NotifAPI extends SlimSQLAPI {
    async count () {
        return this.request('/count', 'GET')
    }

    async setRead () {
        return this.request('/set_read', 'POST')
    }
}

export class UploadAPI extends SlimSQLAPI {
    async token (role, isAvatar) {
        const params = {}
        if (isAvatar) {
            params.is_avatar = isAvatar
        }
        return this.request('/token', 'POST', { params, role })
    }
}

export class WikiAPI extends SlimSQLAPI {
    async random () {
        return this.request('/random', 'GET')
    }
}

export class SearchAPI extends SlimSQLAPI {
    async random (keywords) {
        return this.request('/search', 'GET', { params: { keywords } })
    }
}

export class OAuthAPI extends SlimSQLAPI {
    async getUrl (website) {
        return this.request('/get_oauth_url', 'GET', { params: { website } })
    }

    async getUserData (code) {
        let ret = this.request('/get_user_data', 'GET', { params: { code } })
        if (ret.code !== retcode.FAILED) {
            const oauthState = ret.data.state
            if (oauthState === 50) {
                if (ret.code === retcode.SUCCESS) {
                    this.saveAccessToken(ret.data['access_token'])
                    return ret
                }
            } else {
                return { code: -1, data: ret }
            }
        } else {
            return { code: retcode.FAILED, data: null }
        }
    }
}
