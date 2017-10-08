<template>
<div class="ic-form-row" :class="isError ? 'error' : ''">
    <slot></slot>
    <span class="tip" v-if="isError">{{errtext}}</span>
</div>
</template>

<style scoped>
.tip {
    position: absolute;
    color: red;
    font-size: .75em;
    margin-top: 3px;
}

.error > input {
    border-color: red !important;
}
</style>

<script>
export default {
    props: {
        check: {},
        text: String,
        results: Array
    },
    computed: {
        isError: function () {
            return (this.results && this.results.length) || (!this.check)
        },
        errtext: function () {
            if (this.results && this.results.length) {
                return this.results[0]
            }
            return this.text
        }
    },
    data () {
        return {
        }
    }
}
</script>
