<template>
<div class="ic-container forum-box">
    <div v-title>{{state.config.title}}</div>
    <top-btns></top-btns>
    <div id="board-list" v-if="boardInfo.items && boardInfo.items.length">
        <div class="board-item-box" v-if="!i.parent_id" :key= "i.id" v-for="i in boardInfo.items">
            <router-link :to="{ name: 'forum_board', params: {id: i.id} }" class="board-item">
                <div class="title">
                    <h2><router-link :to="{ name: 'forum_board', params: {id: i.id} }">{{i.name}}</router-link></h2>
                    <div class="sub-boards" v-if="subBoards[i.id]" style="padding-top: 3px">
                        <span>-</span>
                        <template v-for="j in subBoards[i.id]">
                            <router-link :key="j.id" :to="{ name: 'forum_board', params: {id: j.id} }" class="item" style="margin-right: 10px">{{j.name}}</router-link>
                        </template>
                    </div>
                    <p>{{i.brief}}</p>
                </div>
                <div class="detail ic-xs-hidden">
                    <div class="count-block">
                        <div class="count">
                            <span v-if="false" class="tip">24h</span>
                            <p class="num">{{i.s.topic_count}}</p>
                            <p class="txt">主题</p>
                        </div>
                        <div class="count">
                            <span v-if="false" class="tip">24h</span>
                            <p class="num">{{i.s.comment_count}}</p>
                            <p class="txt">回复</p>
                        </div>
                    </div>
                    <div class="recent ic-xs-hidden ic-sm-hidden">
                        <span class="line" :style="lineStyle(i)"></span>
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
    </div>
    <div v-else>
        <p>欢迎来到这里，站点已成功建立。</p>
        <p>下面，前往 <router-link :to="{ name: 'admin_forum_board' }"><a>管理界面</a></router-link> 添加板块。</p>
    </div>
</div>
</template>

<style scoped>
.board-list {
    justify-content: flex-start;
}

.board-list .board-item2 {
    margin: 5px;
}

.sub-boards > .item:not(:last-child)::after {
    content: ',';
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import TopBtns from './topbtns.vue'
import '@/assets/css/forum.css'

export default {
    data () {
        return {
            state,
            subBoards: {},
            boardInfo: {}
        }
    },
    components: {
        TopBtns
    },
    methods: {
        atConvert: $.atConvert2,
        lineStyle: function (board) {
            return $.lineStyle(board)
        },
        fetchData: async function () {
            let ret = await api.board.list({
                order: 'weight.desc,time.asc', // 权重从高到低，时间从先到后
                loadfk: {'id': [
                    {
                        'as': 's',
                        'loadfk': {
                            'last_comment_id': {
                                'loadfk': {'user_id': null}
                            }
                        }
                    },
                    {'as': 's24h', 'table': 's24'}
                ]}
            })

            if (ret.code === api.retcode.SUCCESS) {
                this.boardInfo = ret.data
                for (let i of ret.data.items) {
                    if (i.parent_id) {
                        if (!this.subBoards[i.parent_id]) this.subBoards[i.parent_id] = [i]
                        else this.subBoards[i.parent_id].push(i)
                    }
                }
            } else {
                $.message_by_code(ret.code)
            }
        }
    },
    created: async function () {
        let key = state.loadingGetKey(this.$route)
        this.state.loadingInc(this.$route, key)
        await this.fetchData()
        this.state.loadingDec(this.$route, key)
    }
}
</script>
