<template>
<div class="ic-badge-container">
  <div class="ic-badge">
      <slot />
  </div>
</div>
</template>

<style lang="scss" scoped>
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
    return {
    }
  }
}
</script>
