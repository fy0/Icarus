<template>
<footer class="ic-container">
    <div v-html="extraHtml" v-if="extraHtml"></div>
    <span>Powered by <a href="https://github.com/fy0/icarus" target="_blank">Icarus</a>1.4.0 WIP © 2018</span>
    <span>当前共有 {{state.userOnline}} 人在线</span>
</footer>
</template>

<style scoped>
footer {
    width: 100%;
    padding-top: 16px;
    padding-bottom: 24px;
    border-top: 1px solid #ddd;
    color: #999;
}
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
        extraHtml: function () {
            if ((!this.state.misc) || (!this.state.misc.BACKEND_CONFIG)) return
            return this.state.misc.BACKEND_CONFIG.FOOTER_EXTRA_HTML
        }
    }
}
</script>
