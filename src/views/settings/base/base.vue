<template>
<div class="ic-container">
    <div v-title>用户设置 - {{$config.title}}</div>
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
    components: {
        Sidebar
    }
}
</script>
