<template>
<ic-dialog v-model="siteNew" :title="`新建站点指引`" scrollable :allow-outside-close="false">
    <div>
        <div>你好，你的站点已经初步搭建完成了。</div>
        <div>之所以会看到这张页面，是因为当前还没有任何<b>板块</b>被建立。</div>
        <div>首先，建议进行<nuxt-link :to="{ name: 'account_signup' }">帐户注册</nuxt-link>。</div>
        <div><b>首个完成注册的帐户</b>将自动获得<b>管理员</b>权限。</div>
        <div>随后，前往 <nuxt-link :to="{ name: 'admin_forum_board' }"><a>管理界面</a></nuxt-link> 添加板块。</div>
        <div>在未添加板块的情况下，每次来到这个页面，当前指引都会重新出现一次，</div>
        <div>以帮助你顺利完成整个流程。不过这可能有点烦人。</div>
        <div>最后，请支持<a href="https://github.com/fy0/icarus" target="_blank">开源社区程序 Icarus</a></div>
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

export default {
  data () {
    return {}
  },
  computed: {
    ...mapState('dialog', [
      'siteNew'
    ])
  },
  methods: {
    ok: async function () {
      this.$store.commit('dialog/SET_SITE_NEW', { val: false })
    }
  }
}
</script>
