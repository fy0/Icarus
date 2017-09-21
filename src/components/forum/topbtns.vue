<template>
<div class="forum-topbtns">
    <a class="ic-btn keep blue" href="#">发表主题</a>
    <router-link class="ic-btn orange" :to="{ name: 'forum' }" :class="navActive('forum')">板块列表</router-link>
    <router-link class="ic-btn orange" :to="{ name: 'recent' }" :class="navActive('recent')">最近话题</router-link>
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
        navActive: function (...names) {
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
