<template>
<span class="detail" style="margin-left: .5em" v-if="item.value">
    <!-- 加这个 v-if 是遇到了一种源数据残缺的奇怪情况，可能是旧数据库在几次表结构与逻辑修改中累积的问题 -->
    <template v-if="getOP(item) === MOP.POST_STATE_CHANGE">
        <span v-if="simple">-> {{postStateTxt(item.value.change[1])}}</span>
        <span v-else>({{item.value.change.map(postStateTxt).join(' -> ')}})</span>
    </template>
    <template v-else-if="getOP(item) === MOP.TOPIC_AWESOME_CHANGE">
        <span v-if="item.value.change[1] === 0">-> 撤销</span>
        <span v-else></span>
    </template>
    <span v-else-if="getOP(item) === MOP.POST_VISIBLE_CHANGE">({{item.value.change.map(postVisibleTxt).join(' -> ')}})</span>
    <span v-else-if="getOP(item) === MOP.USER_GROUP_CHANGE">({{item.value.change.map(postGroupTxt).join(' -> ')}})</span>
    <span v-else-if="simpleChangeOP.indexOf(getOP(item)) != -1">({{item.value.change.join(' -> ')}})</span>
</span>
</template>

<style scoped>
</style>

<script>
export default {
  props: {
    item: {},
    simple: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      MOP: this.$misc.MANAGE_OPERATION,
      MOPT: this.$misc.MANAGE_OPERATION_TXT
    }
  },
  computed: {
    simpleChangeOP: function () {
      let MOP = this.MOP
      return [
        MOP.POST_TITLE_CHANGE,
        MOP.USER_CREDIT_CHANGE,
        MOP.USER_REPUTE_CHANGE,
        MOP.USER_EXP_CHANGE,
        MOP.USER_NICKNAME_CHANGE,
        MOP.TOPIC_BOARD_MOVE,
        MOP.TOPIC_AWESOME_CHANGE,
        MOP.TOPIC_STICKY_WEIGHT_CHANGE
      ]
    }
  },
  methods: {
    postStateTxt: function (postState) {
      return this.$misc.POST_STATE_TXT[postState]
    },
    postVisibleTxt: function (i) {
      return this.$misc.POST_VISIBLE_TXT[i]
    },
    postGroupTxt: function (i) {
      return this.$misc.USER_GROUP_TXT[i]
    },
    getOP: function (item) {
      return item.operation || item.op
    }
  }
}
</script>
