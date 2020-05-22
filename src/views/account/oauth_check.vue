<template>
  <div class="ic-container">
    <div class="login">
        <h3 class="title">第三方注册用户信息确认</h3>
        <form class="ic-form">
            <check-row :results="formErrors.email" :check="(!info.email) || checkEmail" :text="'邮箱格式不正确'">
                <label for="email">邮箱</label>
                <input type="email" name="email" id="email" v-model="info.email">
            </check-row>
            <check-row :results="formErrors.nickname" :check="(!info.nickname) || checkNickname" :text="'至少两个汉字，或以汉字/英文字符开头至少4个字符'">
                <label for="nickname">昵称</label>
                <input type="text" name="nickname" id="nickname" v-model="info.nickname">
            </check-row>
            <check-row :results="formErrors.password" :check="(!info.password) || checkPassword" :text='checkPasswordText'>
                <label for="password">密码</label>
                <input type="password" name="password" id="password" v-model="info.password">
            </check-row>
            <check-row :results="formErrors.password2" :check="(!info.password2) || checkPassword2" :text="'重复密码应与前密码一致'">
                <label for="password2">重复密码</label>
                <input type="password" name="password2" id="password2" v-model="info.password2">
            </check-row>
            <check-row :results="formErrors.verify" v-if="0">
                <label for="verify">验证码</label>
                <input type="text" name="verify" id="verify" v-model="info.verify">
            </check-row>
            <check-row style="display: flex;align-items: center;" :check="info.agreeLicense">
                <ic-checkbox v-model="info.agreeLicense">
                    <template>同意<a href="javascript:void(0)" @click.stop="dialogLicense = true">用户许可协议</a></template>
                </ic-checkbox>
            </check-row>
            <div class="ic-form-row">
                <input class="ic-btn green click" :class="{ disabled : !info.agreeLicense }" type="submit" @click.prevent="confirm" value="注 册" style="width: 100%">
            </div>
        </form>

        <div v-title>OAuth</div>
    </div>
  </div>
</template>

<script>
import { retcode } from 'slim-tools'

export default {
  data () {
    return {
      info: {
        nickname: '',
        email: '',
        // other: '',
        password: '',
        password2: '',
        verify: '',
        agreeLicense: false,
        returning: true, // new 之后返回记录
        state: 0,
        platform: 'github',
        id: '', // 用户id
        oauthId: '', // oauth表ID
        loginId: ''
      },
      dialogLicense: false,
      formErrors: {},
      passwordMin: this.$misc.BACKEND_CONFIG.USER_PASSWORD_MIN,
      passwordMax: this.$misc.BACKEND_CONFIG.USER_PASSWORD_MAX
    }
  },
  mounted () {
    let routerParams = this.$route.params.dataObj
    if (routerParams !== undefined) {
      if (routerParams['code'] === -1) {
        this.info.state = routerParams['data']['data']['state']
        this.info.oauthId = routerParams['data']['data']['oauth_id']
        this.info.loginId = routerParams['data']['data']['login_id']
      } else {
        // console.log('OAUTH CHECK: code is error!')
      }
    }
  },
  computed: {
    checkPasswordText: function () {
      return `应在 ${this.passwordMin}-${this.passwordMax} 个字符之间`
    },
    checkPassword: function () {
      if (this.info.password.length < this.passwordMin) return false
      if (this.info.password.length > this.passwordMax) return false
      return true
    },
    checkPassword2: function () {
      return this.info.password === this.info.password2
    },
    checkNickname: function () {
      if ((this.info.nickname < 2) || (this.info.nickname > 32)) return false
      // 检查首字符，检查有无非法字符
      if (!/^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]+$/.test(this.info.nickname)) {
        return false
      }
      // 若长度大于4，直接许可
      if (this.info.nickname.length >= 4) {
        return true
      }
      // 长度小于4，检查其中汉字数量
      let m = this.info.nickname.match(/[\u4e00-\u9fa5]/gi)
      if (m && m.length >= 2) return true
      return false
    },
    checkEmail: function () {
      let mail = /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
      return mail.test(this.info.email)
    }
  },
  methods: {
    confirm: async function () {
      if (!this.info.agreeLicense) {
        return
      }
      if (this.checkPassword && this.checkPassword2 && this.checkEmail && this.checkNickname) {
        let ret = await this.$api.user.new(this.info)
        if (ret.code !== retcode.SUCCESS) {
          this.formErrors = ret.data
          this.$message.byCode(ret.code)
        } else {
          let userinfo = ret.data
          if (ret.code === 0) {
            this.$api.saveAccessToken(userinfo['access_token'])
            await this.$store.dispatch('user/apiGetUserData', ret.data.id)

            this.$message.byCode(ret.code)
            // 用户注册完之后顺便把对应内容发给 oauthUpdate 更新
            this.info.id = userinfo.id
            let retUpdate = await this.$api.Oauth.oauthUpdate(this.info)
            if (retUpdate === retcode.SUCCESS) {
              alert('信息录入成功')
              this.$router.go('/')
            } else {
              alert('信息录入失败')
              return
            }
          } else {
            this.$message.error('注册失败！可能账号或昵称已经被注册')
          }
          this.$router.push({ name: 'forum', params: {} })
        }
      } else {
        this.$message.error('请正确填写所有项目')
      }
    },
    cancel: async function () {
    }
  },
  components: {
  }
}
</script>

<style scoped>
.title {
  color: #444;
}

.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: auto;
  margin-right: auto;
}

.ic-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 320px;

  padding: 10px 30px;
  border: 1px solid #ddd;
}

.ic-form-row > * {
  width: 100%;
}

.ic-form-row {
  width: 100%;
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>
