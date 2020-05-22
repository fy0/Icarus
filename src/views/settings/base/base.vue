<template>
<div class="ic-container">
    <div class="admin-container">
        <sidebar class="admin-sidebar"></sidebar>
        <div class="admin-main"><slot></slot></div>
    </div>
    <dialog-user-set-avatar />
</div>
</template>

<style lang="scss" scoped>
.admin-container {
    display: flex;
}

.admin-sidebar {
    flex: 1 0 0%;
    max-width: $page-left-max-width;
}

.admin-main {
    flex: 4 0 0%;
    padding: 0 0;
}
</style>

<script>
import Sidebar from './sidebar.vue'

export default {
  data () {
    return {}
  },
  head () {
    return {
      title: '用户设置',
      meta: [
        { hid: 'description', name: 'description', content: '用户设置页面' }
      ]
    }
  },
  components: {
    Sidebar
  }
}
</script>
