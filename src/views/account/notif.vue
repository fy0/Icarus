<template>
<div class="ic-container">
    <h3 class="ic-header-no-line">用户提醒</h3>
    <ic-timeline v-if="page.items">
        <ic-timeline-item v-for="i in page.items" :key="i.id">
            <span slot="time">
                <ic-time :timestamp="i.time"/>
            </span>
            <div v-if="i.type === NOTIF_TYPE.MANAGE_INFO_ABOUT_ME" class="notif-content" slot="content">
                <div style="display: flex">
                    <template>你发表的</template>
                    <template>{{typeName(i.related_type)}}</template>
                    <b class="limit m12">
                        <post-link :goto="false" :show-type="false" :type="i.related_type" :item="posts[i.related_id]"/>
                    </b>
                    <template>被</template>
                    <user-link :user="posts[i.sender_ids[0]]" />
                    <template>进行了以下操作：</template>
                </div>
                <div style="font-weight: bolder">
                    <template>{{MOPT[i.data.op]}}</template>
                    <template v-if="i.note"> - {{i.note}}</template>

                    <span style="margin-left: 0.5em;" v-if="i.data.op === MOP.TOPIC_BOARD_MOVE">
                        <template>(</template>
                        <post-link :goto="false" :type="POST_TYPES.BOARD" :item="posts[i.data.value[0]]"/>
                        <template> -> </template>
                        <post-link :goto="false" :type="POST_TYPES.BOARD" :item="posts[i.data.value[1]]"/>
                        <template>)</template>
                    </span>
                    <ManageLogItemDetail v-else :item="i.data" :simple="true" />
                </div>
            </div>
            <div v-else class="notif-content" slot="content">
                <!-- 某人，使动者 -->
                <user-link :user="posts[i.sender_ids[0]]" />
                <!-- 介词 + 定语 -->
                <template v-if="i.type === NOTIF_TYPE.BE_COMMENTED">在你发表的</template>
                <template v-else>在</template><template>{{typeName(i.loc_post_type)}}</template>
                <!-- 某地 -->
                <b class="limit m12">
                    <post-link :goto="false" :show-type="false" :type="i.loc_post_type" :item="posts[i.loc_post_id]"/>
                </b>

                <!-- 做了某事，与某某有关 -->
                <template v-if="i.type === NOTIF_TYPE.BE_COMMENTED">
                    <!-- 发表评论（结合上文，实际是对你发表） -->
                    <template>下发表了{{typeName(i.related_type)}}</template>
                </template>
                <template v-else-if="i.type === NOTIF_TYPE.BE_REPLIED">
                    <!-- 回复（目前只能回复评论） -->
                    <template>下回复了你的{{typeName(i.related_type)}}</template>
                </template>
                <template v-else-if="i.type === NOTIF_TYPE.BE_MENTIONED">
                    <!-- 在某地的XX（如评论）中提到了你 -->
                    <template v-if="i.related_type">的{{typeName(i.related_type)}}</template><template>中提到了你</template>
                </template>
                <div v-else>{{i}}</div>

                <!-- 附加内容 -->
                <div class="brief">{{atConvert(i.brief || '')}}</div>
            </div>
        </ic-timeline-item>
    </ic-timeline>
    <div v-else class="empty">尚未有任何提醒</div>
    <paginator :page-info='page' :route-name='"account_notif"' :link-method="'query'" />
</div>
</template>

<style lang="scss" scoped>
.notif-content {
    margin-top: 10px;

    .brief {
        color: lighten($gray-600, 0.4);
        margin-top: 10px;
    }
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import ManageLogItemDetail from '@/components/misc/manage-log-item-detail.vue'

export default {
    data () {
        return {
            state,
            posts: {},
            POST_TYPES: state.misc.POST_TYPES,
            NOTIF_TYPE: state.misc.NOTIF_TYPE,
            MOP: state.misc.MANAGE_OPERATION,
            MOPT: state.misc.MANAGE_OPERATION_TXT,
            page: {}
        }
    },
    created: async function () {
        await this.fetchData()
    },
    methods: {
        atConvert: $.atConvert2,
        typeName: function (type) {
            return this.state.misc.POST_TYPES_TXT[type]
        },
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
                let userIds = new Set()
                let manageInfoList = []

                for (let i of ret.data.items) {
                    for (let uid of i.sender_ids) {
                        userIds.add(uid)
                    }
                    if (i.type === state.misc.NOTIF_TYPE.MANAGE_INFO_ABOUT_ME) {
                        this.posts[i.related_id] = {
                            'id': i.related_id,
                            'post_type': i.related_type,
                            'post_title': i.data.title
                        }
                        if (i.data.op === this.MOP.TOPIC_BOARD_MOVE) {
                            this.posts[i.data.value[0]] = {
                                'id': i.data.value[0],
                                'post_type': this.POST_TYPES.BOARD,
                                'post_title': i.data.move_info[0]
                            }
                            this.posts[i.data.value[1]] = {
                                'id': i.data.value[1],
                                'post_type': this.POST_TYPES.BOARD,
                                'post_title': i.data.move_info[1]
                            }
                        }
                        continue
                    }
                    this.posts[i.loc_post_id] = {
                        'id': i.loc_post_id,
                        'post_type': i.loc_post_type,
                        'post_title': i.loc_post_title // 一个虚假的列，在post-link中高于其他声明
                    }
                }

                let posts2 = await $.getBasePostsByIDs(async (i) => {
                    return [
                        {
                            'type': i.related_type,
                            'id': i.related_id
                        }
                    ]
                }, manageInfoList)
                for (let [k, v] of Object.entries(posts2)) {
                    this.posts[k] = v
                }

                if (userIds.size > 0) {
                    let users = await api.user.list({
                        'id.in': JSON.stringify(new Array(...userIds)),
                        'select': 'id, nickname'
                    }, 1)
                    for (let t of users.data.items) {
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
    components: {
        ManageLogItemDetail
    },
    watch: {
        '$route': 'fetchData'
    }
}
</script>
