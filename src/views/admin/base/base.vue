<template>
  <page-not-found v-if="!$user.isSiteAdmin"/>
  <div class="ic-container" v-else>
    <div class="admin-container">
        <sidebar class="admin-sidebar"></sidebar>
        <div class="admin-main"><slot></slot></div>
    </div>
    <dialog-topic-manage />
    <dialog-user-manage />
    <dialog-comment-manage />
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
  width: 0%;
}
</style>

<script>
import Sidebar from './sidebar.vue'

export default {
  data () {
    return {}
  },
  methods: {
  },
  components: {
    Sidebar
  }
}
</script>
