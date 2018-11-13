<template>
<admin-base>
    <div v-title>管理日志 - 管理界面 - {{state.config.title}}</div>
    <h3 class="ic-header">管理日志</h3>

    <div v-if="page.items.length === 0" class="no-comment">目前没有日志</div>
    <div v-else class="comment-box">
        <div v-for="i in page.items" :key="i.id" :id="i.id" class="comment">
            <avatar :system="i.user_id === null" :user="i.user_id" class="avatar"></avatar>
            <div class="info">
                <div>
                    <post-link :text-limit="20" :goto="true" :show-type="true" :type-bold="true" :type="i.related_type" :item="postsOfComments[i.related_id]"/>
                    <span>被进行了以下操作：</span>
                </div>
                <div>
                    <span style="font-weight: bolder">{{MOPT[i.operation]}}</span>
                    <span v-if="i.operation === MOP.POST_STATE_CHANGE">({{i.value.map(postStateTxt).join(' -> ')}})</span>
                    <span v-if="i.operation === MOP.POST_VISIBLE_CHANGE">({{i.value.map(postVisibleTxt).join(' -> ')}})</span>
                    <span v-if="simpleChangeOP.indexOf(i.operation) != -1">({{i.value.join(' -> ')}})</span>
                </div>
                <ic-time class="time" :timestamp="i.time" />
            </div>
            <div class="manager">
                <span>操作者</span>
                <b>
                    <user-link v-if="i.user_id" :user="i.user_id" />
                    <span v-else>系统</span>
                </b>
            </div>
            <div class="role">
                <span>执行身份</span>
                <template v-if="i.role">{{i.role}}</template>
                <template v-else>系统</template>
            </div>
            <div class="time1" v-html="toMonth(i.time)"></div>
        </div>
    </div>
    <paginator :page-info='page' :route-name='"admin_common_manage_log"' />
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

.manager {
    display: flex;
    flex-direction: column;
    text-align: center;
    align-self: center;
}

.role {
    display: flex;
    flex-direction: column;
    text-align: center;
    align-self: center;
    padding: 0 20px;
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
    flex: 1 0 0;
    flex-direction: column;
    padding: 0 20px;
}
</style>

<script>
import { marked } from '@/md.js'
import api from '@/netapi.js'
import state from '@/state.js'
import AdminBase from '../base/base.vue'

export default {
    data () {
        return {
            marked,
            state,
            page: { info: {}, items: [] },
            postsOfComments: {},
            MOP: state.misc.MANAGE_OPERATION,
            MOPT: state.misc.MANAGE_OPERATION_TXT
        }
    },
    computed: {
        simpleChangeOP: function () {
            let MOP = this.MOP
            let MOPT = this.MOPT

            return [
                MOP.POST_TITLE_CHANGE,
                MOP.USER_CREDIT_CHANGE,
                MOP.USER_REPUTE_CHANGE,
                MOP.USER_EXP_CHANGE,
                MOP.USER_NICKNAME_CHANGE,
                MOP.TOPIC_BOARD_MOVE,
            ]
        }
    },
    methods: {
        postStateTxt: function (postState) {
            return state.misc.POST_STATE_TXT[postState]
        },
        postVisibleTxt: function (i) {
            return state.misc.POST_VISIBLE_TXT[i]
        },
        postGroupTxt: function (i) {
            return state.misc.USER_GROUP_TXT[i]
        },
        toMonth: function (ts) {
            let date = new Date()
            date.setTime(ts * 1000)
            return $.dateFormat(date, 'MM-dd<br>hh:mm')
        },
        fetchData: async function () {
            let key = state.loadingGetKey(this.$route)
            this.state.loadingInc(this.$route, key)
            let params = this.$route.params
            // let ret = await api.topic.get({
            //     id: params.id,
            // })
            let ret = await api.logManage.list({
                loadfk: { user_id: null },
                order: 'time.desc'
            }, params.page, null, 'admin')

            if (ret.code === api.retcode.SUCCESS) {
                let userIds = []
                let boardIds = []
                let topicIds = []
                let wikiIds = []
                let commentIds = []

                for (let i of ret.data.items) {
                    if (i.related_type === state.misc.POST_TYPES.USER) {
                        userIds.push(i.related_id)
                    } else if (i.related_type === state.misc.POST_TYPES.BOARD) {
                        boardIds.push(i.related_id)
                    } else if (i.related_type === state.misc.POST_TYPES.TOPIC) {
                        topicIds.push(i.related_id)
                    } else if (i.related_type === state.misc.POST_TYPES.WIKI) {
                        wikiIds.push(i.related_id)
                    } else if (i.related_type === state.misc.POST_TYPES.COMMENT) {
                        commentIds.push(i.related_id)
                    }
                }

                this.postsOfComments = {}

                let doRequest = async (name, ids, ex=[]) => {
                    if (ids.length) {
                        let retPost = await api[name].list({
                            'id.in': JSON.stringify(ids),
                            'select': ['id', 'time', 'user_id'].concat(ex)
                        }, 1, null, 'admin')
                        for (let i of retPost.data.items) {
                            this.postsOfComments[i.id] = i
                        }
                    }
                }

                await doRequest('user', userIds, ['nickname'])
                await doRequest('board', boardIds, ['name'])
                await doRequest('topic', topicIds, ['title'])
                await doRequest('wiki', wikiIds, ['title', 'ref'])
                await doRequest('comment', commentIds)

                this.page = ret.data // 提示：注意次序，渲染page依赖上层内容
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
