<template>
<div id="app">
    <div v-title>{{state.config.title}}</div>
    <navbar class="header"></navbar>
    <loading v-if="state.loading" />
    <router-view v-show="!state.loading" class="main"></router-view>
    <my-footer class="footer"></my-footer>
    <test-panel></test-panel>
    <msg-box></msg-box>
</div>
</template>

<style scoped>
#app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}
.main {
    width: 100%;
    flex: 1;
}
</style>

<script>
import state from '@/state.js'
import Navbar from '@/components/utils/navbar.vue'
import MyFooter from '@/components/utils/footer.vue'
import MsgBox from '@/components/utils/msgbox.vue'
import TestPanel from '@/components/utils/test-panel.vue'

export default {
    name: 'app',
    data () {
        return {
            state
        }
    },
    components: {
        TestPanel,
        Navbar,
        MyFooter,
        MsgBox
    }
}
</script>
