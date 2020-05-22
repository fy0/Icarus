<template>
<ic-dialog v-model="userSignout" :width="'500px'" :title="`退出登录`">
    <div class="main">
        <i class="icarus icon-question-circle icon"></i>
        <div>你确定要退出登录吗？</div>
    </div>
    <div class="bottom">
        <span class="ic-btn primary" @click="ok">
            <template v-if="quiting">正在登出 ...</template>
            <template v-else>确定，退出登录</template>
        </span>
        <span class="ic-btn secondary" @click="close">取消，留在这里</span>
    </div>
</ic-dialog>
</template>

<style lang="scss" scoped>
.icon {
    font-size: 80px;
    line-height: 90px;
}

.main {
    font-size: 1.5em;
    text-align: center;
    margin-bottom: 40px;
}

.bottom {
    text-align: center;

    .ic-btn {
        padding-left: 20px;
        padding-right: 20px;
        margin-left: 10px;
    }
}
</style>

<script>
import { mapState } from 'vuex'

export default {
  data () {
    return {
      quiting: false
    }
  },
  computed: {
    ...mapState('dialog', [
      'userSignout'
    ])
  },
  methods: {
    ok: async function () {
      if (this.quiting) return
      this.quiting = true
      await this.$store.dispatch('user/apiSignout')
      // 更新板块信息 - 退出登录
      await this.$store.dispatch('forum/load')
      // TODO: 这里先假设退出登录一定会成功吧
      this.$router.replace('/')
      this.quiting = false
      this.$dialogs.setUserSignout(false)
    },
    close: async function () {
      this.$dialogs.setUserSignout(false)
    }
  }
}
</script>
