<template>
<div class="ic-container">
    <div v-if="customAbout" v-html="customAbout"></div>
    <template v-else>
        <span>旨在成为一个简洁、易用、高效的开源社区系统。</span>
        <a href="https://github.com/fy0/icarus" target="_blank">Github 链接</a>
    </template>
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
    },
    computed: {
        customAbout: function () {
            return this.state.misc && this.state.misc.BACKEND_CONFIG.ABOUT_CUSTOM_HTML
        }
    }
}
</script>
