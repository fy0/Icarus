<template>
<div class="test-panel">
    <button class="ic-btn click" @click="hello">测试面板</button>
    <button :key="i" v-for="i in state.test.items" @click="i[1]">{{i[0]}}</button>
</div>
</template>

<style>
.test-panel {
    position: fixed;
    top: 80px;
    right: 30px;
    opacity: 0.7;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 3px;
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
    mounted: async function () {
        ;
    },
    methods: {
        hello: function () {
            alert('hello!')
        }
    }
}
</script>

<style>
</style>
