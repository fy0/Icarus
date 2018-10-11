<template>
<div class="ic-checkbox" :class="{'disabled': disabled}" @click="check">
    <div class="icon" :class="{'checked': value}" :style="{'width': `${size}px`, 'height': `${size}px`}">
        <svg viewBox="0 0 24 24">
            <path v-if="value" d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.11 0 2-.9 2-2V5c0-1.1-.89-2-2-2zm-9 14l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"></path>
            <path v-else d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"></path>
        </svg>
    </div>
    <div class="right">
        <slot/>
    </div>
</div>
</template>

<style lang="scss">
.ic-checkbox {
    display: inline-flex;
    align-items: center;
    cursor: pointer;
    user-select: none;

    &.disabled {
        cursor: not-allowed;
        color: $common-disabled-color;
        opacity: $common-disabled-opacity;
    }

    .icon {
        width: 24px;
        height: 24px;
        fill: currentColor;
        color: $gray-700;

        &.checked {
            color: $primary;
        }
    }

    .right {
        margin-left: 3px;
    }
}
</style>

<script>
import state from '@/state.js'

export default {
    props: {
        'value': {
            type: Boolean,
            default: false
        },
        'disabled': {
            type: Boolean,
            default: false
        },
        'size': 24
    },
    data () {
        return {
            state
        }
    },
    created: async function () {
    },
    methods: {
        check: function () {
            if (!this.disabled) {
                this.$emit('input', !this.value)
            }
        }
    }
}
</script>
