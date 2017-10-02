<template>
<div class="ic-container" v-if="board">
    <aside style="background-color: ${ board.get_color() }">
        <h3 class="name">{{ board.name }}</h3>
        <div class="brief">{{ board.brief }}</div>
    </aside>

    <div class="board-page-box">
        <div class="topic-list" v-if="topics.length">
            <div class="pure-g ic-board-item">
                <div class="pure-u-18-24 title">
                    <h2><a href="${ url_for('topic', i.id) }">${ i.title|h }</a></h2>
                    <p><a href="#">${i.user.username|h}</a> 发布于 <time timestamp="${i.time}">${i.time}</time></p>
                </div>
                <div class="pure-u-3-24 ic-text-center info ic-eng">
                    <p class="num">${i.view_count}</p>
                    <p class="txt">Click</p>
                </div>
                <div class="pure-u-3-24 ic-text-center info ic-eng">
                    <p class="num">${i.reply_count}</p>
                    <p class="txt">Replies</p>
                </div>
            </div>
        </div>
        <div class="topic-list" v-else>还未有人发言 ...</div>

        <div class="board-info">
            <a href="#" class="topic-new-btn fade-transition">
                发表主题
            </a>
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
    /* border-radius: 3px; */
    color: #fff;
}

.board-page-box {
    display: flex;
    margin-top: 10px;
    flex-direction: row;
}

.board-page-box > .topic-list {
    flex: 17 0 auto;
}

.board-page-box > .board-info {
    flex: 7 0 auto;
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

        if (ret.code === api.retcode.SUCCESS) {
            return next(vm => {
                vm.board = ret.data
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
