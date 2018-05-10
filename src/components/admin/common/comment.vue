<template>
<admin-base>
    <paginator :page-info='page' :route-name='"admin_common_comment"' />
    <div v-if="page.items.length === 0" class="no-comment">目前尚未有评论</div>
    <div v-else class="comment-box">
        <div v-for="(i, _) in page.items" :key="i.id" :id="i.id" class="comment">
            <avatar :user="i.user_id" class="avatar"></avatar>
            <div class="info">
                <div>
                    <b><user-link :user="i.user_id" /></b>
                    <span v-if="i.reply_to_cmt_id">
                        <span>回复</span>
                        <b><a>{{i.reply_to_cmt_id.user_id.nickname}}</a></b>
                    </span>
                    <ic-time class="time" :timestamp="i.time" />
                    <span>于</span>
                    <post-link :goto="true" :show-type="true" :type="i.related_type" :item="postsOfComments[i.related_id]"/>
                </div>
                <div class="content" v-html="marked(i.content || '')"></div>
                <div>
                    <i class="mdi-icarus ic-topic-manage-icon icon-sword-cross" title="管理" @click="setCommentManage(i)"></i>
                    <template v-for="(v, k) in state.misc.POST_STATE_TXT">
                        <a v-if="i.state != k" class="state" :key="k" href="javascript:void(0)">{{v}}</a>
                        <b v-else :key="k" class="state">{{v}}</b>
                    </template>
                </div>
            </div>
            <div class="time1" v-html="toMonth(i.time)"></div>
        </div>
    </div>
    <paginator :page-info='page' :route-name='"admin_common_comment"' />
</admin-base>
</template>

<style scoped>
.state {
    margin-left: 10px;
}

.time1 {
    text-align: center;
    align-self: center;
    padding-right: 20px;
}

.time {
    font-weight: bold;
}

.comment-box {
    border: 1px solid #e0e0e0;
}

.comment {
    display: flex;
    flex-direction: row;
    border-bottom: 1px solid #e0e0e0; 
    padding: 20px;
    justify-content: space-between;
}

.comment > .info {
    display: flex;
    flex: 1 0 auto;
    flex-direction: column;
    padding: 0 20px;
}
</style>

<script>
import Vue from 'vue'
import marked from 'marked'
import api from '@/netapi.js'
import state from '@/state.js'
import AdminBase from '../base/base.vue'

export default {
    data () {
        return {
            marked,
            state,
            page: { info: {}, items: [] },
            postsOfComments: {}
        }
    },
    methods: {
        DateFormat: function (d, format) {
            var date, k
            date = {
                'M+': d.getMonth() + 1,
                'd+': d.getDate(),
                'h+': d.getHours(),
                'm+': d.getMinutes(),
                's+': d.getSeconds(),
                'q+': Math.floor((d.getMonth() + 3) / 3),
                'S+': d.getMilliseconds()
            }
            if (/(y+)/i.test(format)) {
                format = format.replace(RegExp.$1, (d.getFullYear() + '').substr(4 - RegExp.$1.length))
            }
            for (k in date) {
                if (new RegExp('(' + k + ')').test(format)) {
                    format = format.replace(RegExp.$1, RegExp.$1.length === 1 ? date[k] : ('00' + date[k]).substr(('' + date[k]).length))
                }
            }
            return format
        },
        toMonth: function (ts) {
            let date = new Date()
            date.setTime(ts * 1000)
            return this.DateFormat(date, 'MM-dd<br>hh:mm')
        },
        fetchData: async function () {
            let key = state.loadingGetKey(this.$route)
            this.state.loadingInc(this.$route, key)
            let params = this.$route.params
            // let ret = await api.topic.get({
            //     id: params.id,
            // })
            let ret = await api.comment.list({
                loadfk: {user_id: null, reply_to_cmt_id: {loadfk: {'user_id': null}}}
            }, params.page, null, 'admin')

            if (ret.code === api.retcode.SUCCESS) {
                this.page = ret.data
                let topicIds = []

                for (let i of this.page.items) {
                    if (i.related_type === state.misc.POST_TYPES.TOPIC) {
                        topicIds.push(i.related_id)
                    }
                }

                let postsOfComments = {}
                let retTopic = await api.topic.list({'id.in': JSON.stringify(topicIds)}, 1)
                for (let i of retTopic.data.items) {
                    postsOfComments[i.id] = i
                }

                // 不知道为何直接 = 赋值就是取不到值，原因不详
                Vue.set(this, 'postsOfComments', postsOfComments)
            }
            this.state.loadingDec(this.$route, key)
        }
    },
    created: async function () {
        await this.fetchData()
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
