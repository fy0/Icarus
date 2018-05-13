<template>
<div class="ic-container forum-box">
    <div v-title>最近话题 - {{state.config.title}}</div>
    <top-btns></top-btns>
    <loading v-if="loading"/>
    <div v-else-if="topics.items && topics.items.length" id="board-list">
        <div class="board-item-box" :key="i.id" v-for="i in topics.items"  @mouseover="itemHover(i.id)" @mouseout="itemHover(null)">
            <router-link :to="{ name: 'forum_topic', params: {id: i.id} }" class="board-item" :class="{'top-post': i.sticky_weight}">
                <div class="title" style="flex: 12 0 0%">
                    <h2>
                        <router-link :title="i.title" :to="{ name: 'forum_topic', params: {id: i.id} }">
                            <span>{{i.title}}</span>
                            <span v-if="i.state === state.misc.POST_STATE.CLOSE">[关闭]</span>
                        </router-link>
                        <span class="icons">
                            <i v-if="i.awesome == 1" class="mdi-icarus icon-diamond" title="优秀" style="color: #e57272" @click.prevent></i>
                            <i v-if="false" class="mdi-icarus icon-crown" title="精华" style="color: #e8a85d"></i>
                            <i v-if="isAdmin() && i.id === hoverId" class="mdi-icarus icon-sword-cross animated rotateIn" title="管理" style="color: #71c1ef; cursor: pointer" @click.prevent="setTopicManage(i)"></i>
                        </span>
                    </h2>
                    <p>
                        <router-link :to="{ name: 'account_userpage', params: {id: i.user_id.id} }">{{i.user_id.nickname}}</router-link>
                        <span> 发布于 <ic-time :timestamp="i.time" /></span>
                    </p>
                </div>
                <div class="detail ic-xs-hidden" style="flex: 12 0 0%">
                    <div class="count-block" style="flex: 6 0 0;">
                        <router-link tag="div" class="count" :to="{ name: 'forum_board', params: {id: i.board_id.id} }">
                            <p class="board">
                                <router-link :to="{ name: 'forum_board', params: {id: i.board_id.id} }">{{i.board_id.name}}</router-link>
                            </p>
                            <p class="txt">版块</p>
                        </router-link>
                        <div class="count">
                            <p class="num">{{i.s.click_count}}</p>
                            <p class="txt">点击</p>
                        </div>
                        <div class="count">
                            <p class="num">{{i.s.comment_count}}</p>
                            <p class="txt">回复</p>
                        </div>
                    </div>
                    <div class="recent ic-xs-hidden ic-sm-hidden">
                        <span class="line" :style="lineStyle(i.board_id)"></span>
                        <div class="post" v-if="i.s.last_comment_id">
                            <strong><user-link :user="i.s.last_comment_id.user_id" /></strong>
                            <router-link tag="div" class="post-content" :to="{ name: 'forum_topic', params: {id: i.s.last_comment_id.related_id} }">{{i.s.last_comment_id.content}}</router-link>
                        </div>
                        <div class="post" v-else>○ ○ ○ ○ ○</div>
                        <ic-time v-if="i.s.last_comment_id" class="time" :timestamp="i.s.last_comment_id.time" />
                        <div v-else class="time">从未</div>
                    </div>
                </div>
            </router-link>
        </div>
    </div>
    <div v-else>尚未有人发言……</div>
    <dialog-topic-manage />
</div>
</template>

<style scoped>
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import '@/assets/css/forum.css'
import TopBtns from './topbtns.vue'

export default {
    data () {
        return {
            state,
            hoverId: null,
            loading: true,
            topics: []
        }
    },
    methods: {
        isAdmin: function () {
            return $.isAdmin()
        },
        setTopicManage: function (topic) {
            state.dialog.topicManageData = topic
            state.dialog.topicManage = true
        },
        itemHover: function (id) {
            this.hoverId = id
        },
        lineStyle: function (board) {
            return $.lineStyle(board)
        },
        fetchData: async function () {
            this.loading = true
            let retList = await api.topic.list({
                order: 'sticky_weight.desc,weight.desc,time.desc',
                select: 'id, time, user_id, board_id, title, state, awesome',
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
