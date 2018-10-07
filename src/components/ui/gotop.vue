<template>
<div class="gotop" @click="gotop" v-show="showGoTop">
    <i class="fa fa-arrow-up" aria-hidden="true"></i>
</div>
</template>

<style>
.gotop {
    z-index: 9999;
    position: fixed;
    right: 8%;
    bottom: 6%;
    height: 40px;
    width: 40px;
    color: #056ef0;
    text-align: center;
    line-height: 40px;
    cursor: pointer;
}

.tipbox > .item {
}
</style>

<script>
import state from '@/state.js'

export default {
    data () {
        return {
            state,
            showGoTop: false
        }
    },
    created: async function () {
        setInterval(() => {
            let el = document.documentElement
            this.showGoTop = el.scrollTop > 0
        }, 100)
    },
    methods: {
        gotop: function () {
            let el = document.documentElement
            let top = el.scrollTop
            let timer = setInterval(() => {
                top -= Math.abs(top * 0.1)
                if (top <= 1) {
                    top = 0
                    clearInterval(timer)
                }
                el.scrollTop = top
            }, 20)
        }
    }
}
</script>

<style>
</style>
