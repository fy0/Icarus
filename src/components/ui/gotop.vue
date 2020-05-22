<template>
<transition v-on:enter="enter">
    <div title="回到顶部" class="gotop" @click="gotop" v-show="showGoTop">
        <i class="icarus icon-arrow-up"></i>
    </div>
</transition>
</template>

<style>
.gotop {
    z-index: 9999;
    position: fixed;
    right: calc(8%);
    bottom: 6%;
    height: 40px;
    width: 40px;
    color: #056ef0;
    text-align: center;
    line-height: 40px;
    cursor: pointer;
}
</style>

<script>
import anime from 'animejs'

export default {
  data () {
    return {
      showGoTop: false
    }
  },
  created: async function () {
    setInterval(() => {
      let el = document.documentElement
      this.showGoTop = el.scrollTop > 0
    }, 100)
  },
  methods: {
    enter: function (el, done) {
      anime({
        targets: el,
        duration: 700,
        scale: [0, 1],
        complete: () => {
          done()
        }
      })
    },
    gotop: function () {
      anime({
        targets: this.$el,
        duration: 500,
        easing: 'easeOutExpo',
        scale: [1, 1.5, 1]
      })
      // 延迟200使得动画运动到接近最高点时再向上，不会给人迟滞感
      setTimeout(() => {
        let el = document.documentElement
        let top = el.scrollTop
        let timer = setInterval(() => {
          top -= Math.abs(top * 0.1)
          if (top <= 1) {
            top = 0
            clearInterval(timer)
          }
          el.scrollTop = top
        }, 20)
      }, 200)
    }
  }
}
</script>

<style>
</style>
