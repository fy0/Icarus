<template>
<router-link v-if="nickname" :to="{ name: 'account_userpage', params: {id: user.id} }">{{user.nickname}}</router-link>
<router-link v-else :to="{ name: 'account_userpage', params: {id: user.id} }"><slot /></router-link>
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
