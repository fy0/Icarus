<template>
<div class="test-panel">
    <mu-raised-button @click="hello" label="测试面板" primary/>
    <mu-raised-button :key="i[0]" v-for="i in state.test.items" @click="i[1]" :label="i[0]" primary/>
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
