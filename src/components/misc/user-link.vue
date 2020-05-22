<!-- 仅需id和nickname -->
<template>
<nuxt-link v-if="user && nickname" :to="{ name: 'account_userpage', params: {id: user.id} }">{{user.nickname}}</nuxt-link>
<nuxt-link v-else-if="user" :to="{ name: 'account_userpage', params: {id: user.id} }"><slot /></nuxt-link>
</template>

<style scoped>
</style>

<script>
export default {
  props: {
    user: {},
    nickname: {
      default: true
    }
  },
  methods: {
  }
}
</script>
