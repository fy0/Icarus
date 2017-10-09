<template>
<transition-group class="tipbox" tag="div" enter-active-class="animated fadeInLeft" 
    leave-active-class="animated fadeOutLeft">
    <div class="am-alert item" :class="item.class" :key="item.id" v-for="item in state.msgs">
        <a>{{item.text}}</a><br />
    </div>
</transition-group>
</template>

<style>
.tipbox {
    position: fixed;
    left: 0;
    bottom: 5%;
    color: #056ef0;
    width: 300px;
    z-index: 100;
}

.tipbox > .item {
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
        // $.message('warning', '123');
        // $.message('success', '操作已完成');
    }
}
</script>

<style>

</style>
