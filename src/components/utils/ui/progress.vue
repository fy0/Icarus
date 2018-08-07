<template>
<div class="ic-progress" @mouseover="mouseOver" @mouseout="mouseOut">
    <!-- striped animated -->
    <div class="ic-progress-bar" :class="classes" role="progressbar" :style="barStyle">
        <template>{{text}}</template>
        <template v-if="text && theShowPercent"> - </template>
        <template v-if="theShowPercent">{{percent}}%</template>
    </div>
</div>
</template>

<style lang="scss" scoped>

</style>

<script>
import state from '@/state.js'

export default {
    props: {
        text: {
            type: String,
            default: ''
        },
        value: {
            type: Number,
            default: 0
        },
        // min: {
        //     type: Number,
        //     default: 0
        // },
        max: {
            type: Number,
            default: 100
        },
        showPercent: {
            type: Boolean,
            default: false
        },
        showPercentWhenHover: {
            type: Boolean,
            default: false
        },
        classes: {
            type: String,
            default: 'primary'
        }
    },
    data () {
        return {
            state,
            percent: 0,
            hover: false
        }
    },
    computed: {
        barStyle: function () {
            let percent = this.value / this.max
            this.percent = (percent * 100).toFixed(0)
            return {
                'width': `${percent * 100}%`
            }
        },
        theShowPercent: function () {
            if (this.showPercent) return this.showPercent
            return this.showPercentWhenHover && this.hover
        }
    },
    created: function () {
    },
    methods: {
        mouseOver: function () {
            this.hover = true
        },
        mouseOut: function () {
            this.hover = false
        }
    }
}
</script>
