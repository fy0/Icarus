<template>
<div>
    <div ref="share" class="share-component" data-disabled="douban,tencent,linkedin,diandian,google,qq,facebook,twitter"></div>
</div>
</template>

<style lang="scss" scoped>
</style>

<script>
// social share
import 'social-share.js/dist/css/share.min.css'
// import 'social-share.js/dist/js/social-share.min.js'

export default {
  props: {
    title: {
      default: '',
      type: String
    }
  },
  created () {
    if (process.browser && window) {
      this.$nextTick(() => {
        require('social-share.js/dist/js/social-share.min.js')
        window['socialShare'](this.$refs.share, {
          title: this.title || document.title
        })
      })
    }
  },
  data () {
    return {
    }
  }
}
</script>
