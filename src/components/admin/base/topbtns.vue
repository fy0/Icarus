<template>
<div class="ic-topbtns" style="margin-bottom: 15px">
    <router-link class="ic-btn keep blue" :to="{ name: 'admin' }">管理界面</router-link>
    <router-link class="ic-btn keep orange" :to="{ name: 'forum_recent' }">概览</router-link>
</div>
</template>

<style scoped>

</style>

<script>
export default {
    data () {
        return {
        }
    },
    methods: {
        navActiveStrict: function (...names) {
            for (let name of names) {
                if (name === this.$route.name) {
                    return 'keep'
                }
            }
            return 'flag'
        }
    }
}
</script>
