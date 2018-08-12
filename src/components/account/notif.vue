<template>
<div class="ic-container">
    <h3 class="ic-header-no-line">用户提醒</h3>    
    <ic-timeline v-if="page.items">
        <ic-timeline-item v-for="i in page.items" :key="i.id">
            <span slot="time">
                <ic-time :timestamp="i.time"/>
            </span>
            <div class="notif-content" slot="content" v-if="i.type === NOTIF_TYPE.BE_COMMENTED">
                <user-link :user="i.data.comment.user" />
                <span>评论了你的</span>
                <span>文章</span>
                <router-link :title="i.data.post.title" :to="{ name: 'forum_topic', params: {id: i.data.post.id} }">{{i.data.post.title}}</router-link>
                <div>{{atConvert(i.data.comment.brief)}}</div>
            </div>
            <div class="notif-content" slot="content" v-else-if="i.type === NOTIF_TYPE.BE_REPLIED">
                <user-link :user="i.data.comment.user" />
                <span>在文章</span>
                <router-link :title="i.data.post.title" :to="{ name: 'forum_topic', params: {id: i.data.post.id} }">{{i.data.post.title}}</router-link>
                <span>中回复了你的评论</span>
                <ic-time :timestamp="i.time" />
                <div>{{atConvert(i.data.comment.brief)}}</div>
            </div>
            <div class="notif-content" slot="content" v-else-if="i.type === NOTIF_TYPE.BE_MENTIONED">
                <template v-if="i.data.mention.related_type === POST_TYPES.COMMENT">
                    <user-link :user="i.data.mention.user" /> 在
                    <post-link :goto="false" :show-type="true" :type="POST_TYPES.TOPIC" :item="posts[i.data.mention.data.comment_info.related_id]"/>
                    <span>的评论中提到了你</span>
                </template>
                <template v-if="i.data.mention.related_type === POST_TYPES.TOPIC">
                    <user-link :user="i.data.mention.user" />
                    <span>在文章</span>
                    <router-link :title="i.data.mention.data.title" :to="{ name: 'forum_topic', params: {id: i.data.mention.related_id} }">{{i.data.mention.data.title}}</router-link>
                    <span>中提到了你</span>
                </template>
            </div>
            <div class="notif-content" slot="content" v-else>
                {{i}}
            </div>
        </ic-timeline-item>
    </ic-timeline>
    <div v-else class="empty">尚未有任何提醒</div>
    <paginator :page-info='page' :route-name='"account_notif"' :link-method="'query'" />
</div>
</template>

<style scoped>
.notif-content {
    margin-top: 10px;
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'

export default {
    data () {
        return {
            state,
            posts: {},
            POST_TYPES: state.misc.POST_TYPES,
            NOTIF_TYPE: state.misc.NOTIF_TYPE,
            page: {}
        }
    },
    created: async function () {
        await this.fetchData()
    },
    methods: {
        atConvert: $.atConvert2,
        fetchData: async function () {
            let key = state.loadingGetKey(this.$route)
            this.state.loadingInc(this.$route, key)
            let params = this.$route.query
            this.page.curPage = params.page
            let ret = await api.notif.list({
                receiver_id: state.user.id,
                order: 'time.desc'
                // loadfk: {user_id: null, board_id: null}
            }, params.page)

            if (ret.code === api.retcode.SUCCESS) {
                let topicIdSet = new Set()
                for (let i of ret.data.items) {
                    if (i.type === this.NOTIF_TYPE.BE_MENTIONED &&
                        i.data.mention.related_type === this.POST_TYPES.COMMENT) {
                        topicIdSet.add(i.data.mention.data.comment_info.related_id)
                    }
                }

                if (topicIdSet.size > 0) {
                    let topics = await api.topic.list({'id.in': JSON.stringify(new Array(...new Set(topicIdSet)))}, 1)
                    for (let t of topics.data.items) {
                        this.posts[t.id] = t
                    }
                }

                this.page = ret.data
                // let pageNumber = this.$route.query.page
                // if (pageNumber) this.commentPage = parseInt(pageNumber)

                let ret2 = await api.notif.setRead()
                if (ret2.code === api.retcode.SUCCESS) {
                    // 会出现负数问题
                    // state.unread -= ret2.data
                    state.unread = 0
                }
            } else {
                if (ret.code === api.retcode.NOT_FOUND) {
                } else {
                    $.message_by_code(ret.code)
                }
            }
            this.state.loadingDec(this.$route, key)
        }
    },
    watch: {
        '$route': 'fetchData'
    }
}
</script>
