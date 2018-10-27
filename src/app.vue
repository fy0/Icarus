<template>
<div id="app">
    <div v-title>{{state.config.title}}</div>
    <navbar class="header"></navbar>
    <loading v-if="state.loading" />
    <router-view v-show="!state.loading" class="main"></router-view>
    <my-footer class="footer"></my-footer>
    <ic-gotop />
    <msg-box />
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
    padding-top: 25px;
    padding-bottom: 15px;
}
</style>

<script>
import state from '@/state.js'
import Navbar from '@/components/misc/header.vue'
import MyFooter from '@/components/misc/footer.vue'
import MsgBox from '@/components/misc/msgbox.vue'

export default {
    name: 'app',
    data () {
        return {
            state
        }
    },
    components: {
        Navbar,
        MyFooter,
        MsgBox
    }
}
</script>
