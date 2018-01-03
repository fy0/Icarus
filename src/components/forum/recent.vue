<template>
<div class="ic-container forum-box">
    <top-btns></top-btns>
    <div id="board-list">
        <div class="board-item" :key="i.id" v-for="i in topics.items">
            <div class="title" style="flex: 13 0 0%">
                <h2>
                    <router-link :to="{ name: 'forum_topic', params: {id: i.id} }">{{i.title}}</router-link>
                </h2>
                <p><a href="/user/root">{{i.user_id.nickname}}</a> 发布于 <time timestamp="1446111343">2年前</time></p>
            </div>
            <div class="detail ic-xs-hidden" style="flex: 11 0 0%">
                <div class="count">
                    <p class="board">
                        <router-link :to="{ name: 'forum_board', params: {id: i.board_id.id} }">{{i.board_id.name}}</router-link>
                    </p>
                    <p class="txt">版块</p>
                </div>
                <div class="count">
                    <p class="num">1</p>
                    <p class="txt">点击</p>
                </div>
                <div class="count">
                    <p class="num">2</p>
                    <p class="txt">回复</p>
                </div>
                <div class="recent ic-xs-hidden ic-sm-hidden">
                    <span class="line"></span>
                    <strong><a href="#">root</a></strong>
                    <div class="post-content">前三十个文本</div>
                    <a href="#">...</a>
                </div>
            </div>
        </div>
    </div>
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
            topics: []
        }
    },
    beforeRouteEnter: async (to, from, next) => {
        let retList = await api.topic.list({
            order: 'sticky_weight.desc,weight.desc,time.desc',
            loadfk: {'user_id': null, 'board_id': null}
        })
        if (retList.code === api.retcode.SUCCESS) {
            return next(async (vm) => {
                vm.topics = retList.data
            })
        }

        $.message_by_code(retList.code)
        return next('/')
    },
    components: {
        TopBtns
    }
}
</script>
