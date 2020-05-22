<template>
  <div class="ic-container">
    <div v-if="customAbout" v-html="customAbout"></div>
    <template v-else>
      <span>旨在成为一个简洁、易用、高效的开源社区系统。</span>
      <a href="https://github.com/fy0/icarus" target="_blank">Github 链接</a>
    </template>
  </div>
</template>

<style scoped>
</style>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data () {
    return {}
  },
  head () {
    return {
      title: '关于',
      meta: [
        { hid: 'description', name: 'description', content: '关于页面' }
      ]
    }
  },
  computed: {
    customAbout: function (): string {
      return this.$store.getters.BACKEND_CONFIG.ABOUT_CUSTOM_HTML
    }
  },
  created () {
  }
})
</script>
