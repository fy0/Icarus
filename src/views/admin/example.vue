<template>
  <admin-base>
    <span>测试</span>
  </admin-base>
</template>

<style scoped>
</style>

<script>
import AdminBase from '../base/base.vue'

export default {
  data () {
    return {}
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
    AdminBase
  }
}
</script>
