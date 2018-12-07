<template>
<footer class="ic-container">
    <span>Powered by <a href="https://github.com/fy0/icarus" target="_blank">Icarus</a>1.3.3 © 2018</span>
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
    }
}
</script>
