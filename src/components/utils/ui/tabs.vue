<template>
<div class="ic-tabs">
    <slot />
</div>
</template>

<style>
.ic-tabs {
    display: flex;
}
</style>

<script>
import state from '@/state.js'

export default {
    props: {
        value: {
            type: String
        }
    },
    data () {
        return {
            state
        }
    },
    provide () {
        return {
            'setActive': this.setActive,
            'getCurrentActive': this.getCurrentActive
        }
    },
    mounted: async function () {
    },
    methods: {
        setActive: function (name) {
            this.$emit('input', name)
        },
        getCurrentActive: function () {
            return this.value
        }
    }
}
</script>
