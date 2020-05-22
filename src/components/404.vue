<template>
<div class="ic-container box" style="background: none">
    <span class="not-found">404</span>
    <span>你来到了一个不存在的角落<template v-if="autoRedirectPath">，准备跳转至{{redirectTitle}}。剩余 {{second}} 秒</template></span>
    <a href="https://github.com/fy0/icarus" target="_blank">Github 链接</a>
</div>
</template>

<style scoped>
.box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    align-self: center;
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
        // 防止某些页面因为网络太慢，在还未加载出内容时被404页面倒计时跳转主页
        if (this.$store.state.loading) return
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
    countdown: function (val) {
      this.second = val
      this.fetchData()
    }
  }
}
</script>
