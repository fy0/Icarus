<template>
<div class="ic-container box">
    <slot />
    <span><template v-if="autoRedirectPath">准备跳转至{{redirectTitle}}，剩余 {{second}} 秒</template></span>
</div>
</template>

<style scoped>
.box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.not-found {
    font-size: 100px;
}
</style>

<script>
export default {
  props: {
    countdown: {
      type: Number,
      default: 7
    },
    redirectTitle: {
      type: String,
      default: '首页'
    },
    autoRedirectPath: {
      type: String,
      default: '/'
    }
  },
  data () {
    return {
      second: 7,
      timer: null
    }
  },
  methods: {
    fetchData: function () {
      this.timer = setInterval(() => {
        this.second--
        if (!this.second) {
          clearInterval(this.timer)
          this.$router.push(this.autoRedirectPath)
        }
      }, 1000)
    }
  },
  created () {
    this.second = this.countdown
    this.fetchData()
  },
  beforeDestroy () {
    if (this.timer) {
      clearInterval(this.timer)
    }
  },
  watch: {
    'countdown': function (val) {
      this.second = val
      this.fetchData()
    }
  }
}
</script>
