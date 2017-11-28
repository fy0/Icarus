<template>
<div class="ic-container">

<mu-breadcrumb class="nav">
    <mu-breadcrumb-item href="#">
        <router-link :to="{ name: 'forum' }">社区</router-link>
    </mu-breadcrumb-item>
    <mu-breadcrumb-item href="#">
        <router-link :to="{ name: 'forum_board', params: {id: board.id} }">{{board.name}}</router-link>
    </mu-breadcrumb-item>
    <mu-breadcrumb-item>{{topic.title}}</mu-breadcrumb-item>
</mu-breadcrumb>

<div class="topic-box">
    <div class="content typo">
        <h1>{{topic.title}}</h1>
        <div v-html="marked(topic.content || '')"></div>
        <p class="ic-hr"></p>
        <comment-list></comment-list>
        <comment-post :item="topic"></comment-post>
    </div>
    <div class="info">
    </div>
</div>

</div>
</template>

<style scoped>
.topic-box {
    display: flex;
}

.topic-box > .content {
    flex: 18 0 0%;
}

.topic-box > .content > h1 {
    font-size: 28px;
    line-height: 48px;
    text-align: center;    
}

.topic-box > .info {
    flex: 6 0 0%;
}
</style>

<script>
import marked from 'marked'
import api from '@/netapi.js'
import state from '@/state.js'
import '@/assets/css/forum.css'
import CommentList from '../utils/comment-list.vue'
import CommentPost from '../utils/comment-post.vue'

let fetchData = async function (params, next, component = null) {
    let ret = await api.topic.get({id: params.id})
    if (ret.code) next('/')
    let ret2 = await api.board.get({id: ret.data.board_id})
    if (ret2.code) next('/')

    let done = (vm) => {
        vm.topic = ret.data
        vm.board = ret2.data
    }

    if (component) {
        done(component)
        next()
    } else next(done)
}

export default {
    data () {
        return {
            state,
            board: { id: 1 }, // warning fix
            topic: {}
        }
    },
    methods: {
        marked
    },
    created () {
        // fetchData(this.$route.params, this.$router.replace, this)
        // this.fetchData()
    },
    mounted: function () {
    },
    beforeRouteUpdate: async (to, from, next) => {
        this.topic = null
        fetchData(to.params, next, this)
    },
    beforeRouteEnter: async (to, from, next) => {
        fetchData(to.params, next)
    },
    components: {
        CommentList,
        CommentPost
    }
}
</script>
