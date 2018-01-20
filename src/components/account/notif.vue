<template>
<div class="ic-container">
    用户个人提醒：评论、回复、关注、@、收藏、赞、私信、系统通知
    <div v-if="page.items">
        <ul v-for="i in page.items" :key="i.id">
            <li v-if="i.type === NOTIF_TYPE.BE_COMMENTED">
                <div>
                    <span>某某</span>
                    <span>评论了你的</span>
                    <span>文章</span>
                    <router-link :title="i.data[6]" :to="{ name: 'forum_topic', params: {id: i.data[3]} }">《{{i.data[6]}}》</router-link>
                    <ic-time :timestamp="i.time" />
                </div>
                <div>{{i.data[7]}}</div>
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
        isType: function () {
            console.log(state.misc.NOTIF_TYPE)
        },
        fetchData: async function () {
            this.state.loading++
            let params = this.$route.query
            this.page.curPage = params.page
            let ret = await api.notif.list({
                order: 'id.desc'
                // loadfk: {user_id: null, board_id: null}
            }, params.page)

            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
                // let pageNumber = this.$route.query.page
                // if (pageNumber) this.commentPage = parseInt(pageNumber)
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
