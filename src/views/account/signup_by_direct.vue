<template>
  <div class="ic-container box">
    <div class="login">
      <h3 class="title">注册</h3>
      <form class="ic-form">
        <check-row :results="formErrors.email" :check="(!info.email) || checkEmailOK" :text="'邮箱格式不正确'">
          <label for="email">邮箱</label>
          <input class="ic-input" type="email" name="email" id="email" v-model="info.email">
        </check-row>
        <check-row :results="formErrors.nickname" :check="(!info.nickname) || checkNicknameOK" :text="'至少两个汉字，或以汉字/英文字符开头至少4个字符'">
          <label for="nickname">昵称</label>
          <input class="ic-input" type="text" name="nickname" id="nickname" v-model="info.nickname">
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
        <span>协议正文</span>
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

<script lang="ts">
import Vue from 'vue'
// import { mapGetters, mapState } from 'vuex'
import { Component } from 'vue-property-decorator'
import { passwordHash } from '@/utils/password'
import { checkEmail, checkNickname } from '@/utils/user'
import { retcode } from 'slim-tools'
// import { getters } from '../../store'

@Component({
  computed: {
    // ...mapState('dialogs', ['userNew']),
    // ...mapState('user', ['me'])
  }
})
export default class DialogUserNew extends Vue {
  info = {
    email: '',
    nickname: '',
    password: '',
    password2: '',
    verify: '',
    agreeLicense: false,
    returning: true // new 之后返回记录
  }

  dialogLicense = false
  formErrors = {}
  passwordMin = this.$misc.BACKEND_CONFIG.USER_PASSWORD_MIN
  passwordMax = this.$misc.BACKEND_CONFIG.USER_PASSWORD_MAX

  get checkPasswordText () {
    return `应在 ${this.passwordMin}-${this.passwordMax} 个字符之间`
  }

  get checkPassword () {
    if (this.info.password.length < this.passwordMin) return false
    if (this.info.password.length > this.passwordMax) return false
    return true
  }

  get checkPassword2 () {
    return this.info.password === this.info.password2
  }

  get checkNicknameOK () {
    return checkNickname(this.info.nickname)
  }

  get checkEmailOK () {
    return checkEmail(this.info.email)
  }

  async register () {
    if (!this.info.agreeLicense) {
      return
    }
    if (this.checkPassword && this.checkPassword2 && this.checkEmailOK && this.checkNicknameOK) {
      this.$store.commit('LOADING_INC', 1)
      let info = this.info
      let ret = await this.$api.user.signupByDirect(info.email, await passwordHash(info.password), info.nickname)

      if (ret.code !== retcode.SUCCESS) {
        this.formErrors = ret.data
        this.$message.byCode(ret.code)
      } else {
        let userinfo = ret.data
        if (ret.code === 0) {
          this.$api.saveAccessToken(userinfo['access_token'])
          await this.$store.dispatch('user/apiGetUserData', ret.data.id)

          if (ret.code === retcode.SUCCESS) {
            this.$message.success('注册成功！')
          }
        } else {
          this.$message.error('注册失败！可能账号或昵称已经被注册')
        }
        this.$router.push({ name: 'forum', params: {} })
      }

      this.$store.commit('LOADING_DEC', 1)
    } else {
      this.$message.error('请正确填写所有项目')
    }
  }
}
</script>
