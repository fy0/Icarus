<template>
<div class="ic-container forum-box">
    <top-btns></top-btns>
    <loading v-if="loading"/>
    <div v-if="topics.items && topics.items.length" id="board-list">
        <div class="board-item" :key="i.id" v-for="i in topics.items">
            <div class="title" style="flex: 13 0 0%">
                <h2>
                    <router-link :to="{ name: 'forum_topic', params: {id: i.id} }">{{i.title}}</router-link>
                </h2>
                <p>
                    <router-link :to="{ name: 'account_userpage', params: {id: i.user_id.id} }">{{i.user_id.nickname}}</router-link>
                    <span> 发布于 <time timestamp="1446111343">2年前</time></span>
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
                    <p class="num">{{i.statistic.click_count}}</p>
                    <p class="txt">点击</p>
                </div>
                <div class="count">
                    <p class="num">{{i.statistic.comment_count}}</p>
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
        fetchData: async function () {
            this.loading = true
            let retList = await api.topic.list({
                order: 'sticky_weight.desc,weight.desc,time.desc',
                loadfk: {'user_id': null, 'board_id': null, 'id': {'as': 'statistic'}}
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
