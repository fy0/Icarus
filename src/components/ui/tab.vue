<template>
<div class="ic-tab" :class="[isActive ? 'active' : '']" @click="doActive">
    <span class="text">{{title}}</span>
</div>
</template>

<style lang="scss" scoped>
.ic-tab {
    user-select: none;
    outline: none;
    cursor: pointer;

    padding: 10px 30px 12px 30px;
}
</style>

<script>
export default {
  props: {
    title: {
      type: String
    },
    value: {
      type: String
    }
  },
  data () {
    return {}
  },
  computed: {
    isActive: function () {
      return this.getCurrentActive() === this.value
    }
  },
  created: function () {
    // 注：这里父组件得到的参数确实是当前组件，也就是this被传递了。
    // 但是父组件的this还是父组件
    this.addTab(this)
  },
  inject: ['setActive', 'getCurrentActive', 'addTab'],
  methods: {
    doActive: function () {
      this.setActive(this.value)
    }
  }
}
</script>
