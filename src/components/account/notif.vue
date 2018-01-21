<template>
<div class="ic-container">
    <span>用户个人提醒：评论、回复、关注、@、收藏、赞、私信、系统通知</span>
    <div v-if="page.items">
        <ul v-for="i in page.items" :key="i.id">
            <li v-if="i.type === NOTIF_TYPE.BE_COMMENTED">
                <div>
                    <user-link :user="i.data.comment.user" />
                    <span>评论了你的</span>
                    <span>文章</span>
                    <router-link :title="i.data.post.title" :to="{ name: 'forum_topic', params: {id: i.data.post.id} }">《{{i.data.post.title}}》</router-link>
                    <ic-time :timestamp="i.time" />
                </div>
                <div>{{i.data.comment.brief}}</div>
            </li>
            <li v-else-if="i.type === NOTIF_TYPE.BE_REPLIED">
                <div>
                    <user-link :user="i.data.comment.user" />
                    <span>在文章</span>
                    <router-link :title="i.data.post.title" :to="{ name: 'forum_topic', params: {id: i.data.post.id} }">《{{i.data.post.title}}》</router-link>
                    <span>中回复了你的评论</span>
                    <ic-time :timestamp="i.time" />
                </div>
                <div>{{i.data.comment.brief}}</div>
            </li>
            <li v-else>
                {{i}}
            </li>            
        </ul>
        <paginator :page-info='page' :route-name='"account_notif"' :link-method="'query'" />
    </div>
</div>
</template>

<style scoped>

</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'

export default {
    data () {
        return {
            state,
            NOTIF_TYPE: state.misc.NOTIF_TYPE,
            page: {}
        }
    },
    created: async function () {
        await this.fetchData()
    },
    methods: {
        fetchData: async function () {
            this.state.loading++
            let params = this.$route.query
            this.page.curPage = params.page
            let ret = await api.notif.list({
                order: 'time.desc'
                // loadfk: {user_id: null, board_id: null}
            }, params.page)

            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
                // let pageNumber = this.$route.query.page
                // if (pageNumber) this.commentPage = parseInt(pageNumber)

                let ret2 = await api.notif.setRead()
                if (ret2.code === api.retcode.SUCCESS) {
                    state.unread -= ret2.data
                }
            } else {
                $.message_by_code(ret.code)
            }
            this.state.loading--
        }
    },
    watch: {
        '$route': 'fetchData'
    }
}
</script>
