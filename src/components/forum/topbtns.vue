<template>
<div class="ic-topbtns-box">
    <div class="ic-topbtns">
        <router-link class="ic-btn primary" :to="{ name: 'forum_topic_new' }">发表主题</router-link>
        <router-link class="ic-btn borderless orange" :to="{ name: 'forum' }" :class="navActiveStrict('forum')">板块列表</router-link>
        <router-link class="ic-btn borderless orange" :to="{ name: 'forum_recent' }" :class="navActiveStrict('forum_recent')">最近话题</router-link>
    </div>
    <div v-if="state.user">
        <span>声望: {{state.user.reputation}}</span>
        <span style="margin-right: 5px">积分: {{state.user.credit}}</span>
        <span class="ic-btn outline orange" @click="checkIn" v-if="!checkedIn">签到</span>
        <span class="ic-btn orange" v-else>今日已签，连续{{state.user.check_in_his}}次</span>        
    </div>
</div>
</template>

<style lang="scss" scoped>
/* 首页由于标题居中的特殊效果上下自有间隔，其他页面需要留白 15px 实现对齐 */
.ic-topbtns-box {
    display: flex;
    margin-bottom: 10px;
    padding-left: 10px;
    padding-right: 12px;
    align-items: center;
    justify-content: space-between;

    .ic-topbtns {
        display: flex;
        > a {
            display: block;
            margin-right: 6px;
        }
    }
}
</style>

<script>
import state from '@/state.js'
import api from '@/netapi.js'

export default {
    data () {
        return {
            state
        }
    },
    computed: {
        checkedIn: function () {
            return state.user && state.user['last_check_in_time'] >= state.misc.extra.midnight_time
        }
    },
    methods: {
        checkIn: async function () {
            let ret = await api.user.checkIn()
            console.log(111, ret)
        },
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
