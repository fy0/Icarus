<template>
  <redirecting v-if="regDone">
    <span>注册流程已全部完成。</span>
    <span>欢迎来到 {{$config.title}}，{{$user.data.nickname}}</span>
  </redirecting>
  <div v-else-if="available" class="ic-container box">
    <span class="captain">激活账号</span>
    <div>{{text}}</div>
  </div>
  <page-not-found v-else />
</template>

<style scoped>
.box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.captain {
  font-size: 30px;
  font-weight: bolder;
}
</style>

<script>
import { retcode } from 'slim-tools'

export default {
  data () {
    return {
      text: '正在发送请求 ...',
      regDone: false,
      available: false
    }
  },
  methods: {
    fetchData: async function () {
      let query = this.$route.query
      if (!(query.email && query.code)) return
      this.available = true

      let ret = await this.$api.user.signupConfirmByEmail(query.email, query.code)
      if (ret.code === retcode.SUCCESS) {
        this.text = '注册完成，正在进行收尾……'
        this.$api.saveAccessToken(ret.data.key)
        await this.$store.dispatch('user/apiGetUserData', ret.data.id)
        // 更新板块信息 - 注册
        await this.$store.dispatch('forum/load')
        this.regDone = true
      } else {
        if (ret.code === retcode.ALREADY_EXISTS) {
          this.$message.error('帐户已经存在')
        } else {
          this.$message.byCode(ret.code, ret.data)
        }
        this.available = false
      }
    }
  },
  created: async function () {
    await this.fetchData()
  }
}
</script>
