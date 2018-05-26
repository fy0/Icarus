<template>
<div class="ic-container">
    <div v-title>管理界面 - {{state.config.title}}</div>
    <div class="admin-container">
        <sidebar class="admin-sidebar"></sidebar>
        <div class="admin-main"><slot></slot></div>
    </div>
    <dialog-topic-manage />
    <dialog-user-manage />
    <dialog-comment-manage />
</div>
</template>

<style scoped>
.admin-container {
    display: flex;
}

.admin-sidebar {
    flex: 1 0 0%;
}

.admin-main {
    flex: 5 0 0%;
    padding: 0 0;
}
</style>

<script>
import TopBtns from './topbtns.vue'
import Sidebar from './sidebar.vue'
import state from '@/state.js'

export default {
    data () {
        return {
            state
        }
    },
    components: {
        TopBtns,
        Sidebar
    }
}
</script>
