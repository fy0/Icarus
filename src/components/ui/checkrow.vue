<template>
<div class="ic-form-row" :class="{'error': isError}">
    <slot></slot>
    <div v-if="isError">
        <ul class="multi-errors" v-if="multi">
            <li class="tip" :key="i" v-for="i in results">{{i}}</li>
        </ul>
        <span v-else class="tip" :class="{absolute, flex}" >{{errtext}}</span>
    </div>
</div>
</template>

<style scoped>
.tip {
    color: red;
    font-size: 12px;
    /* margin-top: -2px; */
}

.flex {
    margin-top: -10px;
    margin-left: 3px;
}

.absolute {
    position: absolute;
}

.multi-errors {
    margin: 0;
    padding-left: 1em
}

.error > input {
    border-color: red !important;
}
</style>

<script>
export default {
  props: {
    check: {},
    text: String,
    results: Array,

    absolute: { // 注：multi 会覆盖此属性
      type: Boolean,
      default: true
    },
    flex: { // 用于处理 absolute 状态下 + flex 居中布局的移位
      type: Boolean,
      default: false
    },
    multi: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    isError: function () {
      let resultsCheck = this.results && this.results.length
      if (this.multi) return resultsCheck
      return resultsCheck || (!this.check)
    },
    errtext: function () {
      if (this.results && this.results.length) {
        return this.results[0]
      }
      return this.text
    }
  },
  data () {
    return {
    }
  }
}
</script>
