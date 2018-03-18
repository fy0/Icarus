<template>
<div class="ic-container">
    <span>一个简洁、易用、高效的社区系统。</span>
    <a href="https://github.com/fy0/icarus" target="_blank">Github 链接</a>
    <div v-title>关于 - {{state.config.title}}</div>
</div>
</template>

<style scoped>

</style>

<script>
import state from '@/state.js'

export default {
    data () {
        return {
            state
        }
    }
}
</script>
