<template>
<div class="ic-container">
    <top-btns></top-btns>
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
    flex: 5 0 0%;
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
