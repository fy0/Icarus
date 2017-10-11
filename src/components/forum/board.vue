<template>
<div class="ic-container" v-if="board">
    <aside style="background-color: #777777">
        <h3 class="name">{{ board.name }}</h3>
        <div class="brief">{{ board.brief }}</div>
    </aside>

    <div class="board-page-box">
        <div class="topic-list" v-if="topics.items.length">
            <div class="board-item" v-for="i in topics.items">
                <div class="title">
                    <h2><a href="#">{{ i.title }}</a></h2>
                    <p><a href="#">{{i.user_id}}</a> 发布于 <time timestamp="${i.time}">{{i.time}}</time></p>
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
aside > .name {
    margin-top:0;
    font-size: 0.9em;
}

aside > .brief {
    font-size: 0.9em;
}

aside {
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
            board: null,
            topics: []
        }
    },
    beforeRouteEnter: async (to, from, next) => {
        let ret = await api.board.get({id: to.params.id})
        if (ret.code) next('/')

        let retList = await api.topic.list({board_id: to.params.id})
        if (retList.code === api.retcode.SUCCESS) {
            return next(vm => {
                console.log(retList.data)
                vm.board = ret.data
                vm.topics = retList.data
            })
        }

        $.message_by_code(ret.code)
        return next('/')
    },
    beforeRouteUpdate: async function (to, from, next) {
        let ret = await api.board.get({id: to.params.id})

        if (ret.code === api.retcode.SUCCESS) {
            this.board = ret.data
            return next()
        }

        $.message_by_code(ret.code)
        return next('/')
    }
}
</script>
