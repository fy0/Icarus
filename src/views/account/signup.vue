<template>
  <account-signup-direct v-if="useLegacy" />
  <redirecting v-else-if="regDone" :countdown="30">
    <h2>注册成功！</h2>
    <div style="align-items: none">
        <div>我们已经向你的邮箱发送了一封邮件，请点击其中的激活链接完成注册。</div>
        <div>激活之后，你的账号将自动登录。</div>
        <div>如果没有正确收到激活邮件，请检查垃圾邮件箱。</div>
        <div>如果还是没有发现邮件，请尝试重新注册，或联系站点管理员：</div>
        <div><a :href="`mailto:${$misc.BACKEND_CONFIG.SITE_CONTACT_EMAIL}?subject=无法收到激活邮件，注册邮箱：${info.email}`">{{$misc.BACKEND_CONFIG.SITE_CONTACT_EMAIL}}</a></div>
    </div>
  </redirecting>
  <div v-else class="ic-container box">
    <div class="login">
        <h3 class="title">注册</h3>
        <form class="ic-form">
            <check-row :results="formErrors.email" :check="(!info.email) || checkEmail" :text="'邮箱格式不正确'">
                <label for="email">邮箱</label>
                <input class="ic-input" type="email" name="email" id="email" v-model="info.email">
            </check-row>
            <check-row :results="formErrors.password" :check="(!info.password) || checkPassword" :text='checkPasswordText'>
                <label for="password">密码</label>
                <input class="ic-input" type="password" name="password" id="password" v-model="info.password">
            </check-row>
            <check-row :results="formErrors.password2" :check="(!info.password2) || checkPassword2" :text="'重复密码应与前密码一致'">
                <label for="password2">重复密码</label>
                <input class="ic-input" type="password" name="password2" id="password2" v-model="info.password2">
            </check-row>
            <check-row :results="formErrors.verify" v-if="0">
                <label for="verify">验证码</label>
                <input class="ic-input" type="text" name="verify" id="verify" v-model="info.verify">
            </check-row>
            <check-row :check="info.agreeLicense">
                <ic-checkbox v-model="info.agreeLicense">
                    <template>同意<a href="javascript:void(0)" @click.stop="dialogLicense = true">用户许可协议</a></template>
                </ic-checkbox>
            </check-row>
            <div class="ic-form-row">
                <input class="ic-btn success" :class="{ disabled : !info.agreeLicense }" type="submit" @click.prevent="register" value="注 册" style="width: 100%">
            </div>
        </form>
    </div>

    <ic-dialog v-model="dialogLicense" title="用户许可协议">
        <div>
            <div v-html="signupLicense"></div>
        </div>
        <div class="bottom">
            <span class="ic-btn primary" @click="dialogLicense = false">确定</span>
        </div>
    </ic-dialog>

  </div>
</template>

<style lang="scss" scoped>
.bottom {
  text-align: right;

  .ic-btn {
    padding-left: 30px;
    padding-right: 30px;
    margin-left: 10px;
  }
}

.title {
  color: #444;
  margin-bottom: 20px;
}

.box {
  display: flex;
  align-items: center;
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

<script>
import { retcode } from 'slim-tools'
import AccountSignupDirect from '@/views/account/signup_by_direct.vue'

export default {
  data () {
    return {
      info: {
        email: '',
        password: '',
        password2: '',
        verify: '',
        agreeLicense: false,
        returning: true // new 之后返回记录
      },
      regDone: false,
      dialogLicense: false,
      formErrors: {},
      passwordMin: this.$misc.BACKEND_CONFIG.USER_PASSWORD_MIN,
      passwordMax: this.$misc.BACKEND_CONFIG.USER_PASSWORD_MAX,
      signupLicense: this.$misc.BACKEND_CONFIG.SIGNUP_LICENSE_HTML
    }
  },
  head () {
    return {
      title: '用户注册',
      meta: [
        { hid: 'description', name: 'description', content: '用户注册' }
      ]
    }
  },
  computed: {
    useLegacy: function () {
      return (!(this.$misc.BACKEND_CONFIG.EMAIL_ACTIVATION_ENABLE))
    },
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
    checkEmail: function () {
      let mail = /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
      return mail.test(this.info.email)
    }
  },
  watch: {
    'info.email': function () {
      this.formErrors.email = undefined
    }
  },
  methods: {
    register: async function () {
      if (!this.info.agreeLicense) {
        return
      }
      if (this.checkPassword && this.checkPassword2 && this.checkEmail) {
        this.$store.commit('LOADING_INC', 1)
        let info = _.clone(this.info)
        info.password = await $.passwordHash(info.password)
        let ret = await this.$api.user.signupRequestByEmail(info)

        if (ret.code === retcode.SUCCESS) {
          this.regDone = true
        } else if (ret.code === retcode.INVALID_POSTDATA) {
          this.formErrors = ret.data
        } else {
          this.$message.byCode(ret.code, ret.data)
        }

        this.$store.commit('LOADING_DEC', 1)
      } else {
        this.$message.error('请正确填写所有项目')
      }
    }
  },
  components: {
    AccountSignupDirect
  }
}
</script>
