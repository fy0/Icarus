<template>
<router-link v-if="user &&nickname" :to="{ name: 'account_userpage', params: {id: user.id} }">{{user.nickname}}</router-link>
<router-link v-else-if="user" :to="{ name: 'account_userpage', params: {id: user.id} }"><slot /></router-link>
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
