<template>
<div class="ic-topbtns">
    <router-link class="ic-btn keep blue" :to="{ name: 'forum_topic_new' }">发表主题</router-link>
    <router-link class="ic-btn orange" :to="{ name: 'forum' }" :class="navActiveStrict('forum')">板块列表</router-link>
    <router-link class="ic-btn orange" :to="{ name: 'forum_recent' }" :class="navActiveStrict('forum_recent')">最近话题</router-link>
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
