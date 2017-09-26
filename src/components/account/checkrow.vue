<template>
<div class="ic-form-row" :class="isError ? 'error' : ''">
    <slot></slot>
    <span class="tip" v-if="isError">{{text}}</span>
</div>
</template>

<style scoped>
.tip {
    position: absolute;
    color: red;
    font-size: .75em;
}

.error > input {
    border-color: red !important;
}
</style>

<script>
export default {
    props: {
        check: {},
        text: String
    },
    computed: {
        isError: function () {
            return (!this.check)
        }
    },
    data () {
        return {
        }
    }
}
</script>
