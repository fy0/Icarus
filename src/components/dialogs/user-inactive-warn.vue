<template>
  <ic-dialog v-if="$user.data" v-model="userInactive" :title="`还未准备好……`" scrollable>
    <div>
        <div>你的账号需要<b>激活</b>后才能发言，请在邮箱中查收激活邮件。</div>
        <div>
            <template>如果没有正确收到激活邮件，请检查垃圾邮件箱，或点击这里</template>
            <a v-if="sending">正在发送中 ...</a>
            <a v-else href="javascript:void(0)" @click="resendActivationMail">重发激活邮件</a>
            <template>。</template>
        </div>
        <div>如果还是没有收到邮件，请联系站点管理员：</div>
        <div><a :href="`mailto:${state.misc.BACKEND_CONFIG.SITE_CONTACT_EMAIL}?subject=无法收到激活邮件，用户名：${state.user.nickname}`">{{state.misc.BACKEND_CONFIG.SITE_CONTACT_EMAIL}}</a></div>
    </div>
    <div class="bottom">
        <span class="ic-btn primary" @click="ok">确定</span>
    </div>
  </ic-dialog>
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
</style>

<script>
import { mapState } from 'vuex'
import { retcode } from 'slim-tools'
import { timeout } from '@/utils/misc'

export default {
  data () {
    return {
      sending: false
    }
  },
  computed: {
    ...mapState('dialog', [
      'userInactive'
    ])
  },
  methods: {
    ok: async function () {
      this.$dialogs.setUserInactive(false)
    },
    resendActivationMail: async function () {
      this.sending = true
      await timeout(1000) // 先留着吧，我觉得一点即出结果体验也不好
      let ret = await this.$api.user.resendActivationMail()
      if (ret.code === retcode.SUCCESS) {
        this.$message.success('激活邮件发送成功！请检查邮箱。')
      } else {
        this.$message.error('发送失败，每30分钟只能发送一次。')
      }
      this.sending = false
    }
  }
}
</script>
