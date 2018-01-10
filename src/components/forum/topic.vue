<template>
<div class="ic-container">

<mu-breadcrumb class="nav">
    <mu-breadcrumb-item href="#">
        <router-link :to="{ name: 'forum' }">社区</router-link>
    </mu-breadcrumb-item>
    <mu-breadcrumb-item href="#">
        <router-link :to="{ name: 'forum_board', params: {id: topic.board_id.id} }">{{topic.board_id.name}}</router-link>
    </mu-breadcrumb-item>
    <mu-breadcrumb-item>{{topic.title}}</mu-breadcrumb-item>
</mu-breadcrumb>

<div class="topic-box">
    <div class="article typo">
        <!--<h1>{{topic.title}}</h1>-->
        <div class="content" v-html="marked(topic.content || '')"></div>
        <p class="ic-hr"></p>
        <comment-list :item="topic" :cur-page="commentPage" />
        <comment-post :item="topic" :on-success="commentSuccess" :post-type="POST_TYPES.TOPIC"></comment-post>
    </div>
    <div class="info">
    </div>
</div>

</div>
</template>

<style>
/* scope中加不上这个 我很奇怪，这是为了让图片等不将父元素撑开 */
.topic-box > .article > .content * {
    max-width: 100%;
}
</style>

<style scoped>
.topic-box {
    display: flex;
}

.topic-box > .article {
    flex: 18 0 0%;
}

.topic-box > .article > h1 {
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

export default {
    data () {
        return {
            state,
            commentPage: 1,
            loading: true,
            POST_TYPES: state.misc.POST_TYPES,
            topic: { board_id: {id: 1} }
        }
    },
    methods: {
        marked,
        commentSuccess: function () {
            // this.$router.replace({name: 'forum_topic', params: {id: this.topic.id}})
            this.$router.go(0)
        },
        fetchData: async function () {
            let params = this.$route.params
            let ret = await api.topic.get({
                id: params.id,
                loadfk: {user_id: null, board_id: null}
            })

            if (ret.code === api.retcode.SUCCESS) {
                this.topic = ret.data
                let pageNumber = this.$route.query.page
                if (pageNumber) this.commentPage = parseInt(pageNumber)
            } else {
                $.message_by_code(ret.code)
            }
        }
    },
    watch: {
        '$route.query.page': async function (val) {
            this.commentPage = val
        }
    },
    created: async function () {
        // 注意：从这里观察出一个现象：
        // created 会比 mounted 早触发，但并不一定更早完成
        // await 占用时间的时候，挂载流程仍将继续
        this.state.loading++
        await this.fetchData()
        this.state.loading--
    },
    mounted: function () {
        ;
    },
    components: {
        CommentList,
        CommentPost
    }
}
</script>
