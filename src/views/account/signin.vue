<template>
  <div class="ic-container box">
    <div class="login">
        <h3 class="title">登录</h3>
        <form class="ic-form">
            <check-row :results="formErrors.email" :check="(!info.email) || checkEmail" :text="'邮箱格式不正确'">
                <label for="email">邮箱/昵称</label>
                <input class="ic-input" type="email" name="email" id="email" v-model="info.email">
            </check-row>
            <check-row :results="formErrors.password" :check="(!info.password) || checkPassword" :text='checkPasswordText'>
                <label for="password">密码</label>
                <input class="ic-input" type="password" name="password" id="password" v-model="info.password">
            </check-row>
            <div class="ic-form-row">
                <div class="ic-btn success" @click.prevent="login">登 录</div>
            </div>
            <div class="ic-form-row">
                <nuxt-link class="lost-poasswrod" :to="{name: 'account_password_reset_request'}">忘记密码？</nuxt-link>
            </div>
            <div v-if="false" class="ic-form-row three-auth">
                <span class="title"> 第三方登录 </span>
                <div class="icons">
                    <!-- <span class="icon">QQ</span>
                    <span class="icon">微博</span>
                    <span class="icon">Github</span> -->
                    <input class="icon" type="submit" name="" value="QQ">
                    <input class="icon" type="submit" name="" value="微博">
                    <input class="icon" type="submit" name="" value="github" @click.prevent="github_url">
                </div>
            </div>
        </form>
    </div>
  </div>
</template>

<style scoped>
.title {
  color: #444;
  margin-bottom: 20px;
}

.three-auth {
  display: flex;
  flex-direction: column;
}

.three-auth > .title {
  text-align: center;
}

.three-auth > .title:before, .three-auth > .title:after {
  display: inline-block;
  width: 50px;
  content: " ";
  border-top: 1px solid #ccc;
  vertical-align: middle;
}

.three-auth > .icons {
  display: flex;
  justify-content: center;
}

.three-auth > .icons > .icon {
  border: 1px solid #ccc;
  border-radius: 4px;
  border-style: groove;
}

.three-auth > .icons > .icon:not(:first-child) {
  margin-left: 20px;
}

.lost-poasswrod {
  color: #aaa;
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

export default {
  data () {
    return {
      info: {
        email: '',
        password: ''
      },
      goLastPage: false,
      formErrors: {},
      passwordMin: this.$misc.BACKEND_CONFIG.USER_PASSWORD_MIN,
      passwordMax: this.$misc.BACKEND_CONFIG.USER_PASSWORD_MAX
    }
  },
  head () {
    return {
      title: '用户登录',
      meta: [
        { hid: 'description', name: 'description', content: '用户登录' }
      ]
    }
  },
  computed: {
    checkEmail: function () {
      // let mail = /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
      // return mail.test(this.info.email)
      return true
    },
    checkPasswordText: function () {
      return `应在 ${this.passwordMin}-${this.passwordMax} 个字符之间`
    },
    checkPassword: function () {
      if (this.info.password.length < this.passwordMin) return false
      if (this.info.password.length > this.passwordMax) return false
      return true
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.goLastPage = from.fullPath !== '/'
    })
  },
  methods: {
    login: async function () {
      if (this.checkEmail && this.checkPassword) {
        this.$store.commit('LOADING_INC', 1)
        // 登录请求
        let ret = await this.$api.user.signin({
          email: this.info.email,
          password: await $.passwordHash(this.info.password)
        })
        if (ret.code === retcode.SUCCESS) {
          // 刷新用户信息
          await this.$store.dispatch('user/apiGetUserData', ret.data.id)
          // 更新板块信息 - 登录
          await this.$store.dispatch('forum/load')

          if (this.goLastPage) {
            this.$store.commit('LOADING_DEC', 1)
            this.$message.success('登录成功，正在回到前页……')
            this.$router.go(-1)
            return
          } else {
            this.$store.commit('LOADING_DEC', 1)
            this.$message.success('登录成功，正在回到主页……')
            this.$router.replace('/')
            return
          }
        } else {
          this.formErrors = ret.data
          this.$message.byCode(ret.code)
        }
        // ret = await this.$api.user.get({username: this.info.username}, 'test')
        // console.log(ret)
        this.$store.commit('LOADING_DEC', 1)
      } else {
        this.$message.error('请正确填写所有项目')
      }
    },
    github_url: async function () {
      // 获取url，然后跳转
      let ghUrl = await this.$api.Oauth.getUrl('github')
      window.open(ghUrl, '_blank')
      // console.log(ghUrl)
    }
  },
  components: {
  }
}
</script>
