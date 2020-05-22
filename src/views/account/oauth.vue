<template>
  <div class="ic-container">
    <span>登录中，请稍等。</span>

    <div v-title>OAuth</div>
  </div>
</template>

<style scoped>
</style>

<script>
import { retcode } from 'slim-tools'

export default {
  data () {
    return {}
  },
  beforeCreate () { // 判断是否有参数提交，如果没有就跳转到主页
    if (this.$route.query.code) { // xx?oauth=xxx
    } else {
      this.$router.replace('/')
    }
  },
  created () {
    this.check(this.$route.query.code)
  },
  methods: {
    check: async function (code) {
      // console.log('check', code)
      let ret = await this.$api.Oauth.send(code) // 拿到oauth返回的code，交给 api - get_user_data
      // 判断返回值，跳转到主页或者补全信息界面
      if (ret['code'] === retcode.SUCCESS) {
        await this.$store.dispatch('user/apiGetUserData', ret.data.id)

        if (this.goLastPage) {
          this.$message.success('登录成功，正在回到前页……')
          this.$router.go(-1)
        } else {
          this.$message.success('登录成功，正在回到主页……')
          this.$router.replace('/')
          return
        }

        this.$router.replace('/') // 没有加上用户认证，也没有判断用户是否已登陆
      } else if (ret['code'] === -1) {
        this.$router.push({
          name: 'account_oauth_check',
          params: {
            name: 'name',
            dataObj: ret
          }
        }) // 跳转到验证界面
      } else {
        // console.log('非法状态')
      }
    }
  }
}
</script>
