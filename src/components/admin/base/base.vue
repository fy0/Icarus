<template>
<div class="ic-container">
    <div class="admin-container">
        <sidebar class="admin-sidebar"></sidebar>
        <div class="admin-main"><slot></slot></div>
    </div>
    <dialog-topic-manage />
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
    padding: 26px 0;
}
</style>

<script>
import TopBtns from './topbtns.vue'
import Sidebar from './sidebar.vue'

export default {
    data () {
        return {
        }
    },
    components: {
        TopBtns,
        Sidebar
    }
}
</script>
