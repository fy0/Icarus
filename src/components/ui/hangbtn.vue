<template>
<transition v-on:enter="enter">
    <div class="hang-btn" @click="click" v-show="showBtn" ref="btn">
        <slot />
    </div>
</transition>
</template>

<style>
.hang-btn {
    z-index: 9999;
    position: fixed;
    right: 8%;
    bottom: 6%;
    height: 40px;
    width: 40px;
    color: #056ef0;
    text-align: center;
    line-height: 40px;
    cursor: pointer;
}

.hang-btn > i {
    font-size: 28px;
}

.gotop > i {
    font-size: 28px;
}
</style>

<script>
import anime from 'animejs'

export default {
  props: {
    checkDisplay: {
      type: Function
    },
    onclick: {
      type: Function
    }
  },
  data () {
    return {
      showBtn: false
    }
  },
  created: async function () {
    let int = setInterval(() => {
      // 经试验，this.$el, this.$parent.$el在切换页面后都依旧存在，只有ref是比较稳妥的做法
      if (!this.$refs.btn) return clearInterval(int)
      this.showBtn = this.checkDisplay(this.$el)
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
    click: function () {
      anime({
        targets: this.$el,
        duration: 500,
        easing: 'easeOutExpo',
        scale: [1, 1.5, 1]
      })
      // 延迟200使得动画运动到接近最高点时再向上，不会给人迟滞感
      setTimeout(() => {
        this.onclick(this.$el)
      }, 200)
    }
  }
}
</script>

<style>
</style>
