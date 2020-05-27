import { SlimSQLAPI, retcode } from 'slim-tools'

export class UserAPI extends SlimSQLAPI {
  async signin ({ email, password }: any) {
    let ret = await this.request('/signin', 'POST', { data: { email, password } })
    if (ret.code === retcode.SUCCESS) {
      this.saveAccessToken(ret.data.access_token)
    }
    return ret
  }

  /** 注册（直接形式，不开启邮件注册） */
  async signupByDirect (email: string, password: string, nickname: string) {
    return this.request('/signup_by_direct', 'POST', { data: { email, password, nickname } })
  }

  // 准备进行邮件注册
  async signupRequestByEmail (data: any) {
    return this.request('/signup_request_by_email', 'POST', { data })
  }

  // 拿到激活码，进行邮件注册
  async signupConfirmByEmail (email: string, code: string) {
    return this.request('/signup_confirm_by_email', 'POST', { data: { email, code } })
  }

  async checkIn () {
    return this.request('/check_in', 'POST')
  }

  /* eslint-disable camelcase */
  async changePassword ({ old_password, password }: any) {
    return this.request('/change_password', 'POST', { data: { old_password, password } })
  }

  // 申请重置密码
  async requestPasswordReset (nickname: string, email: string) {
    return this.request('/request_password_reset', 'POST', { data: { nickname, email } })
  }

  // 修改昵称
  async changeNickname (nickname: string) {
    return this.request('/change_nickname', 'POST', { data: { nickname } })
  }

  // 验证重置密码
  async validatePasswordReset (uid: string, code: string, password: string) {
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
  async qn_token (role: string, isAvatar: boolean) {
    const params: any = {}
    if (isAvatar) {
      params.is_avatar = isAvatar
    }
    return this.request('/qn_token', 'POST', { params, role })
  }

  async upload (file: File, role: string) {
    let data = {
      'file': file
    }
    return this.request('/upload', 'post', { data, role })
  }
}

export class WikiAPI extends SlimSQLAPI {
  async random () {
    return this.request('/random', 'GET')
  }
}

export class SearchAPI extends SlimSQLAPI {
  async random (keywords: Array<string>) {
    return this.request('/search', 'GET', { params: { keywords } })
  }
}

export class MiscAPI extends SlimSQLAPI {
  async info () {
    return this.request('/info', 'GET')
  }
}

export class OAuthAPI extends SlimSQLAPI {
  async getUrl (website: string) {
    return this.request('/get_oauth_url', 'GET', { params: { website } })
  }

  async getUserData (code: any) {
    let ret = await this.request('/get_user_data', 'GET', { params: { code } })
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
