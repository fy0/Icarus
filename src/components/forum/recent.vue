<template>
<div class="ic-container forum-box">
    <top-btns></top-btns>
    <loading v-if="loading"/>
    <div v-else-if="topics.items && topics.items.length" id="board-list">
        <div class="board-item" :key="i.id" v-for="i in topics.items">
            <div class="title" style="flex: 13 0 0%">
                <h2>
                    <router-link :to="{ name: 'forum_topic', params: {id: i.id} }">{{i.title}}</router-link>
                </h2>
                <p>
                    <router-link :to="{ name: 'account_userpage', params: {id: i.user_id.id} }">{{i.user_id.nickname}}</router-link>
                    <span> 发布于 <ic-time :timestamp="i.time" /></span>
                </p>
            </div>
            <div class="detail ic-xs-hidden" style="flex: 11 0 0%">
                <div class="count">
                    <p class="board">
                        <router-link :to="{ name: 'forum_board', params: {id: i.board_id.id} }">{{i.board_id.name}}</router-link>
                    </p>
                    <p class="txt">版块</p>
                </div>
                <div class="count">
                    <p class="num">{{i.s.click_count}}</p>
                    <p class="txt">点击</p>
                </div>
                <div class="count">
                    <p class="num">{{i.s.comment_count}}</p>
                    <p class="txt">回复</p>
                </div>
                <div class="recent ic-xs-hidden ic-sm-hidden">
                    <span class="line" :style="lineStyle(i.board_id)"></span>
                    <div class="post" v-if="i.s.last_comment_id">
                        <strong><user-link :user="i.s.last_comment_id.user_id" :nickname="true" /></strong>
                        <router-link tag="div" class="post-content" :to="{ name: 'forum_topic', params: {id: i.s.last_comment_id.related_id} }">{{i.s.last_comment_id.content}}</router-link>
                    </div>
                    <div class="post" v-else>○ ○ ○ ○ ○</div>
                    <ic-time v-if="i.s.last_comment_id" class="time" :timestamp="i.s.last_comment_id.time" />
                    <div v-else class="time">从未</div>
                </div>
            </div>
        </div>
    </div>
    <div v-else>尚未有人发言……</div>
</div>
</template>

<style scoped>
</style>

<script>
import api from '@/netapi.js'
// import state from '@/state.js'
import '@/assets/css/forum.css'
import TopBtns from './topbtns.vue'

export default {
    data () {
        return {
            loading: true,
            topics: []
        }
    },
    methods: {
        lineStyle: function (board) {
            return $.lineStyle(board)
        },
        fetchData: async function () {
            this.loading = true
            let retList = await api.topic.list({
                order: 'sticky_weight.desc,weight.desc,time.desc',
                loadfk: {'user_id': null, 'board_id': null, 'id': {'as': 's', loadfk: {'last_comment_id': {'loadfk': {'user_id': null}}}}}
            })
            if (retList.code === api.retcode.SUCCESS) {
                this.topics = retList.data
                this.loading = false
                return
            }

            $.message_by_code(retList.code)
            this.loading = false
        }
    },
    created () {
        this.fetchData()
    },
    components: {
        TopBtns
    }
}
</script>
