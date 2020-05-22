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
      hover: false
    }
  },
  computed: {
    percent: function () {
      let percent = this.value / this.max
      return (percent * 100).toFixed(0)
    },
    barStyle: function () {
      return {
        'width': `${this.percent}%`
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
