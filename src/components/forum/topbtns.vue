<template>
<div class="ic-topbtns-box">
    <div class="ic-topbtns">
        <router-link class="ic-btn primary" :to="{ name: 'forum_topic_new' }">发表主题</router-link>
        <router-link class="ic-btn borderless orange" :to="{ name: 'forum_main', params: {page: 1} }" :class="navActiveStrict('forum_main')">最近话题</router-link>
        <router-link class="ic-btn borderless orange" :to="{ name: 'forum_boards' }" :class="navActiveStrict('forum_boards')">板块列表</router-link>
    </div>
    <div v-if="state.user" style="display: flex; align-items: center;">
        <!-- <span>声望: {{state.user.reputation}}</span> -->
        <div class="char-info">
            <div class="bar-area">
                <span class="level">lv. {{levelInfo.level}}</span>
                <ic-progress :show-percent-when-hover="true" class="expbar" v-model="levelInfo.cur" :title="`${levelInfo.cur}/${levelInfo.exp.level}`" :max="levelInfo.exp.level"/>
            </div>
            <div class="other">
                <span style="margin-right: 5px">⭐ {{state.user.exp}}</span>
                <span style="margin-right: 5px">💰 {{state.user.credit}}</span>
            </div>
        </div>
        <span class="ic-btn outline orange" @click="checkIn" v-if="!checkedIn">签到</span>
        <span class="ic-btn orange" v-else>今日已签 x{{state.user.check_in_his}}</span>        
    </div>
</div>
</template>

<style lang="scss" scoped>
.char-info {
    display: inline-flex;
    flex-direction: column;
    margin-right: 5px;
    min-width: 120px;
    font-size: 12px;
    line-height: 16px;

    .bar-area {
        flex: 1;
        height: 16px;
        display: flex;
        align-items: center;

        .level {
            margin-right: 3px;
        }

        .expbar {
            flex: 1;
            max-height: 10px;
            padding: 1px;
            border: 1px solid $primary;
            border-radius: 3px;
            font-size: 5px !important;

            .ic-progress-bar {
                padding: 1px;
                border-radius: 2px;
            }
        }
    }

    .other {
        flex: 1;
        margin-left: 24px;
    }
}

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
        levelInfo: function () {
            return $.getLevelByExp(this.state.user.exp)
        },
        checkedIn: function () {
            return state.user && state.user['last_check_in_time'] >= state.misc.extra.midnight_time
        }
    },
    methods: {
        checkIn: async function () {
            let ret = await api.user.checkIn()
            state.user['last_check_in_time'] = ret.data.time
            state.user['check_in_his'] = ret.data.check_in_his
            state.user.exp += ret.data.exp
            state.user.credit += ret.data.credit
            $.message_success(`签到成功！获得经验 ${ret.data.exp} 点，积分 ${ret.data.credit} 点，已连续签到 ${ret.data.check_in_his} 次！`, 5000)
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
