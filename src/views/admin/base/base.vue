<template>
<page-not-found v-if="!isAdmin()"/>
<div class="ic-container" v-else>
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
import state from '@/state.js'

export default {
    data () {
        return {
            state
        }
    },
    methods: {
        isAdmin: $.isAdmin
    },
    components: {
        Sidebar
    }
}
</script>
