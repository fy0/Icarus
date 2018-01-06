<template>
<loading v-if="loading"/>
<div v-else-if="board" class="ic-container">
    <mu-paper class="board-title" :zDepth="1" style="background-color: #777777">
        <h3 class="name">{{ board.name }}</h3>
        <div class="brief">{{ board.brief }}</div>
    </mu-paper>

    <div class="board-page-box">
        <div class="topic-list" v-if="topics.items.length">
            <div class="board-item" :key="i.id" v-for="i in topics.items">
                <div class="title">
                    <h2><router-link :to="{ name: 'forum_topic', params: {id: i.id} }">{{i.title}}</router-link></h2>
                    <p>
                        <router-link :to="{ name: 'account_userpage', params: {id: i.user_id.id} }">{{i.user_id.nickname}}</router-link>
                        <span> 发布于 <time timestamp="${i.time}">{{i.time}}</time></span>
                    </p>
                </div>
                <div class="detail ic-xs-hidden" style="flex: 5 0 0%">
                    <div class="count">
                        <p class="num">1</p>
                        <p class="txt">点击</p>
                    </div>
                    <div class="count">
                        <p class="num">2</p>
                        <p class="txt">回复</p>
                    </div>
                </div>
            </div>
            <paginator :page-info='topics' :route-name='"forum_board"'></paginator>
        </div>
        <div class="topic-list" v-else>还未有人发言 ...</div>

        <div class="board-info">
            <router-link class="topic-new-btn fade-transition" :to="{ name: 'forum_topic_new' }">发表主题</router-link>
            <div class="board-note fade-transition" style="margin-top:5px">
                <p><strong>版块公告</strong></p>
                <div>版主很懒，什么也没有写</div>
            </div>
        </div>
    </div>
</div>
<div class="ic-container" v-else>
    什么也没有
</div>
</template>

<style scoped>
.loading {
    display: flex;
    align-items: center;
    justify-content: center;
}

aside > .name {
    margin-top:0;
    font-size: 0.9em;
}

aside > .brief {
    font-size: 0.9em;
}

.board-title {
    background: #1f8dd6;
    padding: 1em 1em;
    border-radius: 3px;
    color: #fff;
}

.board-page-box {
    display: flex;
    margin-top: 10px;
    flex-direction: row;
}

.board-page-box > .topic-list {
    flex: 3 0 auto;
}

.board-page-box > .board-info {
    flex: 1 0 auto;
}

.topic-new-btn {
    border: 1px solid #eee;
    color: #000;
    padding:1em 1em;
    text-align: center;
    display: block;
}

.topic-new-btn:hover {
    border-color: #bbb;
}

.board-note {
    border: 1px solid #eee;
    padding: 1em 1em;
    font-size: 14px;
}

.board-note:hover {
    border-color: #bbb;
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import '@/assets/css/forum.css'

export default {
    data () {
        return {
            state,
            loading: true,
            board: null,
            topics: []
        }
    },
    methods: {
        test: function (id) {
            ;
        },
        fetchData: async function () {
            this.loading = true
            let params = this.$route.params
            let ret = await api.board.get({id: params.id})

            if (ret.code) {
                $.message_by_code(ret.code)
                this.loading = false
                return
            }

            let retList = await api.topic.list({board_id: params.id, loadfk: {'user_id': null}}, params.page)
            if (retList.code === api.retcode.SUCCESS) {
                this.board = ret.data
                this.topics = retList.data
            }
            this.loading = false
        }
    },
    created () {
        // 组件创建完后获取数据，
        // 此时 data 已经被 observed 了
        this.fetchData()
    },
    watch: {
        // 如果路由有变化，会再次执行该方法
        '$route': 'fetchData'
    },
    components: {
    }
}
</script>
