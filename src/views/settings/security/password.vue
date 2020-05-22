<template>
  <setting-base>
    <h3 class="ic-header">修改密码</h3>
    <form class="ic-form">
        <check-row :flex="true" :results="formErrors.old_password" :check="true" :text='checkPasswordText'>
            <label for="old_password">旧密码</label>
            <input class="ic-input" autocomplete="old-password" type="password" name="old_password" id="old_password" v-model="info.old_password">
        </check-row>

        <check-row :flex="true" :results="formErrors.password" :check="(!info.password) || checkPassword" :text='checkPasswordText'>
            <label for="password">新密码</label>
            <input class="ic-input" autocomplete="password" type="password" name="password" id="password" v-model="info.password">
        </check-row>

        <check-row :flex="true" :results="formErrors.password2" :check="(!info.password2) || checkPassword2" :text="'重复密码应与前密码一致'">
            <label for="password2">重复密码</label>
            <input class="ic-input" autocomplete="password" type="password" name="password2" id="password2" v-model="info.password2">
        </check-row>

        <div class="ic-form-row">
            <span></span>
            <input class="ic-btn success" type="submit" @click.prevent="changePassword" value="确 认">
        </div>
    </form>
  </setting-base>
</template>

<style scoped>
.ic-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 420px;

  padding: 10px 30px 10px 0px;
}

.ic-form-row {
  display: flex;
  align-items: center;
  padding-top: 10px;
  padding-bottom: 10px;
  width: 100%;
}

.ic-form-row > :nth-child(1) {
  padding-right: 10px;
  flex: 3 0 0;
}

.ic-form-row > label {
  text-align: right;
}

.ic-form-row > :nth-child(2) {
  flex: 7 0 0;
}
</style>

<script>
import SettingBase from '../base/base.vue'
import { retcode } from 'slim-tools'

export default {
  data () {
    return {
      info: {
        old_password: '',
        password: '',
        password2: '',
        verify: ''
      },
      dialogLicense: false,
      formErrors: {},
      passwordMin: this.$misc.BACKEND_CONFIG.USER_PASSWORD_MIN,
      passwordMax: this.$misc.BACKEND_CONFIG.USER_PASSWORD_MAX
    }
  },
  head () {
    return {
      title: '修改密码 - 用户设置',
      meta: [
        { hid: 'description', name: 'description', content: '用户设置页面' }
      ]
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
    }
  },
  methods: {
    changePassword: async function () {
      if (this.checkPassword && this.checkPassword2) {
        // 提交修改请求
        let info = _.clone(this.info)
        info.password = await $.passwordHash(info.password)
        info.password2 = await $.passwordHash(info.password2)
        info.old_password = await $.passwordHash(info.old_password)
        let ret = await this.$api.user.changePassword(info)

        if (ret.code !== retcode.SUCCESS) {
          this.formErrors = ret.data
          this.$message.error('修改密码失败')
        } else {
          this.$api.saveAccessToken(ret.data)
          this.$message.byCode(ret.code)
          this.info.old_password = ''
          this.info.password = ''
          this.info.password2 = ''
          this.info.verify = ''
        }
      } else {
        this.$message.error('请正确填写所有项目')
      }
    }
  },
  components: {
    SettingBase
  }
}
</script>
