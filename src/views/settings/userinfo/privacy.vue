<template>
  <setting-base>
    <div v-title>隐私设置 - 用户设置 - {{$config.title}}</div>
    <span>公开邮箱 公开动态 </span>
  </setting-base>
</template>

<style scoped>
</style>

<script>
import SettingBase from '../base/base.vue'

export default {
  data () {
    return {}
  },
  head () {
    return {
      title: '隐私设置 - 用户设置',
      meta: [
        { hid: 'description', name: 'description', content: '用户设置页面' }
      ]
    }
  },
  methods: {
    fetchData: async function () {
      // let params = this.$route.params
      // let ret = await this.$api.topic.get({
      //     id: params.id,
      // })
    }
  },
  created: async function () {
    this.$store.commit('LOADING_INC', 1)
    await this.fetchData()
    this.$store.commit('LOADING_DEC', 1)
  },
  watch: {
    // 如果路由有变化，会再次执行该方法
    '$route': 'fetchData'
  },
  components: {
    SettingBase
  }
}
</script>
