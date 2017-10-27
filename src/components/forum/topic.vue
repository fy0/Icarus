<template>
<div class="ic-container">

<div class="nav">
    <router-link :to="{ name: 'forum' }">社区</router-link>
    <span>»</span>
    <router-link :to="{ name: 'forum_board', params: {id: board.id} }">{{board.name}}</router-link></h2>
</div>

<div class="topic-box">
    <div class="content typo">
        <h1>{{topic.title}}</h1>
        <div v-html="marked(topic.content || '')"></div>

        <!--
        <comment></comment>
        <div class="comment-container">
            <div class="comment-info">
                <span class="comment-info-title">{{comments_length}} 条评论</span>
                <span class="comment-info-line"></span>
            </div>

            <div class="comment" v-for="(i, index) in comments" :key="index">
                <div class="ic-comment-body">
                    <div class="ic-comment-content" v-html="marked(i.content)"></div>
                    <div class="ic-comment-meta">
                        <b>{{i.user.name}}</b>
                        <time>{{time_to_text(i.time)}}</time>
                        <span> | </span>
                        <span>#{{i.id}}</span>
                    </div>
                </div>
                <div class="divider-line" v-if="index != comments.length-1"></div>
            </div>

            <div v-if="comments_page > 1">
                <span v-for="index in comments_page" :key="index">
                    <span class="comment-page-btn" v-if="$route.params.cmtpage == index">{{index}}</span>
                    <router-link class="comment-page-btn" v-else :to="{ name: 'topic', params: {id: topic.id, cmtpage: index}}" replace>{{index}}</router-link>
                </span>
            </div>

            <div v-if="state.data.user" style="margin-top: 20px">
                <form method="POST">
                    <div>
                        <textarea name="content" rows="5" placeholder="" style="width:100%;border-color:#d9d9d9" v-model="user_comment_text"></textarea>
                    </div>
                    <div>
                        <el-button @click="commentPost">发表</el-button>
                        <span style="margin-left:10px" id="reply_msg"></span>
                    </div>
                </form>
            </div>
            <div style="padding: 20px" v-else>
                需要 <router-link :to="{ path: `/signin` }">登录</router-link> 后方可回复, 如果你还没有账号你可以 <router-link :to="{ path: `/signup` }">注册</router-link> 一个帐号。
            </div> 
        </div>-->
    </div>
    <div class="info">
    </div>
</div>

<p class="ic-hr"></p>

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

export default {
    data () {
        return {
            state,
            board: {},
            topic: {}
        }
    },
    methods: {
        marked
    },
    beforeRouteEnter: async (to, from, next) => {
        let ret = await api.topic.get({id: to.params.id})
        if (ret.code) next('/')
        let ret2 = await api.board.get({id: ret.data.board_id})
        if (ret2.code) next('/')
        return next(async (vm) => {
            vm.topic = ret.data
            vm.board = ret2.data
        })
    },
    beforeRouteUpdate: async function (to, from, next) {
        return next('/')
    },
    components: {
    }
}
</script>
