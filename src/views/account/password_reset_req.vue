<template>
  <div v-if="!done" class="ic-container box">
    <div class="login">
        <h3 class="title">忘记密码</h3>
        <form class="ic-form">
            <check-row :results="formErrors.email" :check="(!info.email) || checkEmail" :text="'邮箱格式不正确'">
                <label for="email">注册邮箱</label>
                <input class="ic-input" type="email" name="email" id="email" v-model="info.email">
            </check-row>

            <check-row :results="formErrors.nickname" :check="(!info.nickname) || checkNickname" :text="'至少两个汉字，或以汉字/英文字符开头至少4个字符'">
                <label for="nickname">用户昵称</label>
                <input class="ic-input" type="text" name="nickname" id="nickname" v-model="info.nickname">
            </check-row>

            <div class="ic-form-row">
                <span></span>
                <input class="ic-btn success" type="submit" @click.prevent="resetPassword" value="申请重置密码">
            </div>

            <div class="ic-form-row">
                <nuxt-link class="lost-poasswrod" :to="{name: 'account_signin'}">返回登录</nuxt-link>
            </div>
        </form>
    </div>
  </div>
  <redirecting class="ic-container box" v-else>
      <span>操作已成功完成，请检查邮箱。</span>
      <span>若一段时间后未收到密码重置邮件，请重新进行此操作。</span>
      <span>若问题还未解决，请联系站点管理员。</span>
  </redirecting>
</template>

<style scoped>
.title {
  color: #444;
  margin-bottom: 20px;
}

.lost-poasswrod {
  color: #aaa;
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
  padding-top: 14px;
  padding-bottom: 14px;
}
</style>

<script>
import { retcode } from 'slim-tools'

export default {
  data () {
    return {
      info: {
        email: '',
        nickname: ''
      },
      formErrors: {},
      requesting: false,
      done: false
    }
  },
  computed: {
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
    resetPassword: async function () {
      if (this.requesting) return
      this.requesting = true
      if (this.checkNickname && this.checkEmail) {
        let ret = await this.$api.user.requestPasswordReset(this.info.nickname, this.info.email)
        if (ret.code !== retcode.SUCCESS) {
          this.formErrors = ret.data
          this.$message.error('重置密码失败，请确认邮箱和昵称组合正确')
        } else {
          this.done = true
        }
      } else {
        this.$message.error('请正确填写所有项目')
      }
      this.requesting = false
    },
    fetchData: async function () {
    }
  },
  created: async function () {
    await this.fetchData()
  },
  components: {
  }
}
</script>
