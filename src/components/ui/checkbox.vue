<template>
<div class="ic-checkbox" :class="{'disabled': disabled}" @click="check">
    <svg viewBox="0 0 24 24" class="icon" :class="{'checked': value}" :style="iconStyle">
        <path v-if="value" d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.11 0 2-.9 2-2V5c0-1.1-.89-2-2-2zm-9 14l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"></path>
        <path v-else d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"></path>
    </svg>
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
        width: 21.33px; // 实际上是16px，内部是外部的3/4
        height: 21.33px;
        fill: currentColor;
        color: $gray-700;

        &.checked {
            color: $primary;
        }
    }

    .right {
        margin-left: 5px;
    }
}
</style>

<script>
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
    'size': {
      type: Number,
      default: 16
    }
  },
  data () {
    return {}
  },
  computed: {
    iconStyle: function () {
      let blockSize = `${this.size / 0.75}px`
      let marginOffset = `-${this.size * 0.125}px`
      return {
        'width': blockSize,
        'height': blockSize,
        'margin-left': marginOffset,
        'margin-right': marginOffset
      }
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
