<template>
<div class="ic-container">
    <div v-title>用户设置 - {{state.config.title}}</div>
    <div class="admin-container">
        <sidebar class="admin-sidebar"></sidebar>
        <div class="admin-main"><slot></slot></div>
    </div>
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
    components: {
        Sidebar
    }
}
</script>
