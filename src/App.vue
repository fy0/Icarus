<template>
<div id="app">
    <navbar></navbar>
    <router-view></router-view>
    <msg-box></msg-box>
</div>
</template>

<script>
import Navbar from '@/components/utils/navbar.vue'
import MsgBox from '@/components/utils/msgbox.vue'

export default {
    name: 'app',
    components: {
        Navbar,
        MsgBox
    }
}
</script>

<style>
</style>
