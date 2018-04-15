<template>
<footer class="ic-container">
    <span>Powered by <a href="https://github.com/fy0/icarus" target="_blank">Icarus</a> © 2015 - 2017</span>
    <span>当前共有 {{state.userOnline}} 人在线</span>
</footer>
</template>

<style scoped>
footer {
    width: 100%;
    margin-top: 15px;
    padding: 1pc 10px 24px;
    border-top: 1px solid #eee;
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
