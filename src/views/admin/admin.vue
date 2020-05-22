<template>
  <admin-base>欢迎来到管理界面</admin-base>
</template>

<style scoped>
</style>

<script>
import AdminBase from './base/base.vue'

export default {
  data () {
    return {}
  },
  head () {
    return {
      title: '管理界面',
      meta: [
        { hid: 'description', name: 'description', content: '管理页面' }
      ]
    }
  },
  components: {
    AdminBase
  }
}
</script>
