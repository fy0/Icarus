<template>
<div class="ic-container forum-box">
    <div v-title>最近话题 - {{state.config.title}}</div>
    <div class="wrapper">
        <div class="left-nav">
            <div class="left-nav-box">
                <!-- <span class="post-new-topic">板块列表</span> -->
                <router-link class="ic-btn primary post-new-topic" :style="postNewTopicStyle" :to="{ name: 'forum_topic_new' }">发表主题</router-link>
                <div class="ul-subboards">
                    <router-link :to="{ name: 'index'}" class="item" style="margin: 10px 0 10px 0">
                        <div class="sign"></div>
                        <span class="sub-board-item">全部主题</span>
                    </router-link>
                    <router-link v-for="j in boardList" :key="j.id" class="item" :to="{ name: 'forum_board', params: {id: j.id} }">
                        <div class="sign" :style="lineStyleBG(j)"></div>
                        <span class="sub-board-item">{{j.name}}</span>
                    </router-link>
                </div>
            </div>
        </div>
        <div class="right" id="board-list">
            <top-btns></top-btns>
            <loading v-if="loading"/>
            <div style="flex: 1 0 0%" v-else-if="topics && topics.items.length">
                <div class="board-item-box" :key="i.id" v-for="i in topics.items"  @mouseover="itemHover(i.id)" @mouseout="itemHover(null)">
                    <router-link :to="{ name: 'forum_topic', params: {id: i.id} }" class="board-item" :class="{'top-post': i.sticky_weight}">
                        <div class="title-recent" style="flex: 10 0 0%">
                            <avatar style="margin-right: 10px;" :user="i.user_id" :size="32" class="avatar"></avatar>
                            <div class="right">
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
                                    <router-link class="board-badge" :style="lineStyleBG(i.board_id)" :to="{ name: 'forum_board', params: {id: i.board_id.id} }">{{i.board_id.name}}</router-link>
                                    <user-link :user="i.user_id" />
                                    <span> 发布于 <ic-time :timestamp="i.time" /></span>
                                </p>
                            </div>
                        </div>
                        <div class="detail ic-xs-hidden" style="flex: 9 0 0%">
                            <div class="count-block" style="flex: 4 0 0;">
                                <div class="count">
                                    <p class="num">{{i.s.click_count}}</p>
                                    <p class="txt">点击</p>
                                </div>
                                <div class="count">
                                    <p class="num">{{i.s.comment_count}}</p>
                                    <p class="txt">回复</p>
                                </div>
                            </div>
                            <div class="recent ic-xs-hidden ic-sm-hidden" style="flex: 5 0 0;">
                                <span class="line" :style="lineStyle(i.board_id)"></span>
                                <div class="post" v-if="i.s.last_comment_id && i.s.last_comment_id.id">
                                    <strong><user-link :user="i.s.last_comment_id.user_id" /></strong>
                                    <router-link tag="div" class="post-content" :to="{ name: 'forum_topic', params: {id: i.s.last_comment_id.related_id} }">{{atConvert(i.s.last_comment_id.content)}}</router-link>
                                </div>
                                <div class="post" v-else>○ ○ ○ ○ ○</div>
                                <ic-time v-if="i.s.last_comment_id" class="time" :timestamp="i.s.last_comment_id.time" />
                                <div v-else class="time">从未</div>
                            </div>
                        </div>
                    </router-link>
                </div>
                <paginator v-if="isBoard" :page-info='topics' :route-name='"forum_board"' />
                <paginator v-else :page-info='topics' :route-name='"forum_main"' />
            </div>
            <div style="flex: 1 0 0%" v-else>
                <div style="margin-left: 10px;">尚未有人发言……</div>
            </div>
        </div>
    </div>
    <dialog-topic-manage />
</div>
</template>

<style scoped lang="scss">
.wrapper {
    display: flex;

    .left-nav {
        flex: 5 0 0%;
    }

    .right {
        flex: 19 0 0%;
    }
}

.ul-subboards > .item {
    display: flex;
    align-items: center;
    padding: 7px 0;
    font-size: 14px;
    font-weight: bolder;
    color: $gray-600;
}

.board-badge {
    padding: 8px;
    color: $light;
    opacity: 0.6;
    // background-color: $gray-400;

    &:hover {
        color: $light;
    }
}

.ul-subboards > .item > .sign {
    width: 1em;
    height: 1em;
    background-color: #000;
    border-radius: 3px;
    flex-shrink: 0;
}

$left-nav-padding-right: 30px;

.ul-subboards {
    margin: 0;
    list-style: none;

    .sub-board-item {
        margin-left: 3px;
    }
}

.left-nav-box {
    padding: 0 $left-nav-padding-right 0 0;
}

.post-new-topic {
    width: 100%;
    display: block;
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import '@/assets/css/_forum.scss'
import TopBtns from './topbtns2.vue'
import nprogress from 'nprogress/nprogress.js'

let pageOneHack = function (to, from, next) {
    // 这一hack的目标是抹除 /r/1 的存在，使其与 / 看起来完全一致
    // 但似乎由于 nprogress 的存在，显得有点僵硬
    if (to.name === 'forum_main' && (to.params.page === '1' || to.params.page === 1)) {
        if (from.name === 'index') {
            state.loading = 0
            nprogress.done()
            return next(false)
        }
        return next({name: 'index'})
    }
    next()
}

export default {
    data () {
        return {
            state,
            hoverId: null,
            loading: true,
            boardList: [],
            topics: null
        }
    },
    computed: {
        postNewTopicStyle: function () {
            ;
        },
        isBoard: function () {
            return this.$route.name === 'forum_board'
        }
    },
    methods: {
        atConvert: $.atConvert2,
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
        lineStyleBG: function (board) {
            return $.lineStyle(board, 'background-color')
        },
        fetchData: async function () {
            this.loading = true
            let baseQuery = {}
            let params = this.$route.params
            let page = 1

            // 具体板块
            if (this.$route.name === 'forum_board') {
                baseQuery['board_id'] = params.id
                page = params.page
            } else if (this.$route.name === 'forum_main') {
                page = params.page
            }

            let boards = await api.board.list({
                order: 'parent_id.asc,weight.desc,time.asc' // 权重从高到低，时间从先到后
            })
            if (boards.code === api.retcode.SUCCESS) {
                let lst = []
                for (let i of boards.data.items) {
                    lst.push(i)
                }
                this.boardList = lst
            }

            let query = this.$route.query
            let order = 'weight.desc, update_time.desc' // 权重降序（希望以后能做到无视置顶权重<5的置顶）

            if (query.type === '2') {
                order = 'update_time.desc, time.desc' // 更新时间降序
            }

            if (query.type === '3') {
                order = 'time.desc' // 发布时间降序
            }

            let retList = await api.topic.list(Object.assign(baseQuery, {
                order: order,
                select: 'id, time, user_id, board_id, title, state, awesome, weight, update_time',
                loadfk: {'user_id': null, 'board_id': null, 'id': {'as': 's', loadfk: {'last_comment_id': {'loadfk': {'user_id': null}}}}}
            }), page)
            if (retList.code === api.retcode.SUCCESS) {
                this.topics = retList.data
                this.loading = false
                return
            } else {
                this.topics = null
            }

            // $.message_by_code(retList.code)
            this.loading = false
        }
    },
    beforeRouteEnter (to, from, next) {
        return pageOneHack(to, from, next)
    },
    beforeRouteUpdate (to, from, next) {
        return pageOneHack(to, from, next)
    },
    created () {
        this.fetchData()
    },
    watch: {
        // 如果路由有变化，会再次执行该方法
        '$route': 'fetchData'
    },
    components: {
        TopBtns
    }
}
</script>
