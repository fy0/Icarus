<template>
<div class="ic-tabs">
    <slot />
    <div :style="lineStyle" class="ic-tab-highlight-line"></div>
</div>
</template>

<style lang="scss" scoped>
.ic-tabs {
    display: inline-flex;
    position: relative;

    .ic-tab-highlight-line {
        position: absolute;
        left: 0;
        bottom: 0;
        height: 2px;
        background-color: $primary;
        transition: transform .3s;
    }
}
</style>

<script>
export default {
  props: {
    value: {
      type: String
    }
  },
  data () {
    return {
      tabs: []
    }
  },
  computed: {
    lineStyle: function () {
      let width = 0
      let translate = 0
      if (this.tabs.length) {
        width = 1 / this.tabs.length
        translate = this.tabs.indexOf(this.value) / (this.tabs.length - 1)
      }
      return {
        'width': `${width * 100}%`,
        'transform': `translateX(${translate * 100}%)`
      }
    }
  },
  provide () {
    return {
      'addTab': this.addTab,
      'setActive': this.setActive,
      'getCurrentActive': this.getCurrentActive
    }
  },
  mounted: async function () {
  },
  methods: {
    addTab: function (tab) {
      this.tabs.push(tab.value)
    },
    setActive: function (name) {
      this.$emit('input', name)
    },
    getCurrentActive: function () {
      return this.value
    }
  }
}
</script>
