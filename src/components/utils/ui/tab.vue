<template>
<div class="ic-tab" :class="[isActive ? 'active' : '']" @click="doActive">
    <span class="text">{{title}}</span>
</div>
</template>

<style lang="scss" scoped>
.ic-tab {
    user-select: none;
    outline: none;
    cursor: pointer;

    .text {
        padding: 10px 20px;
    }
}
</style>

<script>
import state from '@/state.js'

export default {
    props: {
        title: {
            type: String
        },
        value: {
            type: String
        }
    },
    data () {
        return {
            state
        }
    },
    computed: {
        isActive: function () {
            return this.getCurrentActive() === this.value
        }
    },
    inject: ['setActive', 'getCurrentActive'],
    methods: {
        doActive: function () {
            this.setActive(this.value)
        }
    }
}
</script>
