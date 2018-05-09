<template>
<admin-base>
    <div v-if="page.items.length === 0" class="no-comment">目前尚未有评论</div>
    <div v-else class="comment-box">
        <div v-for="(i, _) in page.items" :key="i.id" :id="i.id" class="comment">
            <div class="content" v-html="marked(i.content || '')"></div>
            <div class="info">
                <avatar :user="i.user_id" class="avatar"></avatar>
                <b><user-link :user="i.user_id" /></b>
                <span v-if="i.reply_to_cmt_id">
                    <span>回复</span>
                    <b><a :href="'#' + i.reply_to_cmt_id.id">{{i.reply_to_cmt_id.user_id.nickname}}</a></b>
                </span>
                <span><ic-time :timestamp="i.time" /></span>
            </div>
        </div>
    </div>
</admin-base>
</template>

<style scoped>
.comment-box {
    border: 1px solid #e0e0e0;    
}

.comment {
    display: flex;
    flex-direction: column;
    border-bottom: 1px solid #e0e0e0;
    padding: 20px;
}

.comment > .info {
    display: flex;
    justify-content: flex-end;
}
</style>

<script>
import marked from 'marked'
import api from '@/netapi.js'
import state from '@/state.js'
import AdminBase from '../base/base.vue'

export default {
    data () {
        return {
            marked,
            state,
            page: { info: {}, items: [] }
        }
    },
    methods: {
        fetchData: async function () {
            // let params = this.$route.params
            // let ret = await api.topic.get({
            //     id: params.id,
            // })
            let ret = await api.comment.list({
                loadfk: {user_id: null, reply_to_cmt_id: {loadfk: {'user_id': null}}}
            }, 1)
            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
                console.log(111, this.page)
            }
        }
    },
    created: async function () {
        let key = state.loadingGetKey(this.$route)
        this.state.loadingInc(this.$route, key)
        await this.fetchData()
        this.state.loadingDec(this.$route, key)
    },
    watch: {
        // 如果路由有变化，会再次执行该方法
        '$route': 'fetchData'
    },
    components: {
        AdminBase
    }
}
</script>
