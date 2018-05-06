<template>
<div class="ic-container">
    <div v-if="user.nickname" v-title>{{user.nickname}} - {{state.config.title}}</div>
    <div class="userpage">
        <div class="left">
            <avatar :user="user" :size="164" class="avatar"></avatar>
            <p>{{user.nickname}}</p>
            <div>
                <div>{{state.misc.USER_GROUP_TXT[user.group]}}</div>
                <div>第 {{user.number}} 名会员</div>
                <div title="加入时间"><ic-time :ago="false" :timestamp="user.reg_time"/></div>
            </div>
        </div>
        <div class="right">
            <mu-tabs :value="activeTab" @change="handleTabChange" class="api-view-tabs">
                <mu-tab value="tabTopic" title="主题" @active="handleActive"/>
                <mu-tab value="tab2" title="评论"/>
                <mu-tab value="tab3" v-if="false" title="收藏" @active="handleActive"/>
                <mu-tab value="tab4" v-if="false" title="关注"/>
            </mu-tabs>
            <div class="tab" v-if="activeTab === 'tabTopic'">
                <div v-if="tabs.topic.topics" style="width: 100%">
                    <mu-timeline v-if="tabs.topic.topics.items && tabs.topic.topics.items.length">
                        <mu-timeline-item :key="i.id" v-for="i in tabs.topic.topics.items">
                            <span slot="time"><ic-time :timestamp="i.time"/></span>
                            <span slot="des">发表了一篇主题
                                <router-link :to="{ name: 'forum_topic', params: {id: i.id} }">《{{i.title}}》</router-link>
                            </span>
                        </mu-timeline-item>
                    </mu-timeline>
                    <div v-else>暂无数据</div>
                </div>
                <ball-beat-loader v-else style="margin-top:66px" size="90" color="#df2525"/>
            </div>
            <div class="tab" v-if="activeTab === 'tab2'">
                <div v-if="tabs.comment.data" style="width: 100%">
                    <mu-timeline v-if="tabs.comment.data.items && tabs.comment.data.items.length">
                        <mu-timeline-item :key="i.id" v-for="i in tabs.comment.data.items">
                            <span slot="time"><ic-time :timestamp="i.time"></ic-time></span>
                            <span slot="des">发表了一条评论
                                <div>
                                    <router-link :to="{ name: 'forum_topic', params: {id: i.related_id} }">{{i.content}}</router-link>
                                </div>
                            </span>
                        </mu-timeline-item>
                    </mu-timeline>
                    <div v-else>暂无数据</div>
                </div>
                <ball-beat-loader v-else style="margin-top:66px" size="90" color="#df2525"/>
            </div>
            <div class="tab" v-if="activeTab === 'tab3'" style="width: 100%">
                <h2>Tab Three</h2>
                <p>这是第三个 tab</p>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
.userpage {
    display: flex;
}

.userpage > .left {
    flex: 1 0 0%;
}

.userpage > .right {
    flex: 8 0 0;
    padding: 0 40px;
}

.api-view-tabs {
    width: 40%;
    background-color: transparent;
    color: rgba(0, 0, 0, 0.87);
}

.api-view-tabs .mu-tab-link {
    color: rgba(0, 0, 0, 0.54);
}

.api-view-tabs .mu-tab-active {
    color: #7e57c2;
}

.tab {
    padding-top: 20px;
    display: flex;
    justify-content: center;
    align-content: center;
}
</style>

<script>
import Avatar from '../utils/avatar.vue'
import state from '@/state.js'
import api from '@/netapi.js'

export default {
    data () {
        return {
            activeTab: 'tabTopic',
            user: {},
            tabs: {
                topic: {
                    topics: null
                },
                comment: {
                    data: null
                }
            },
            state
        }
    },
    mounted: async function () {
        ;
    },
    methods: {
        tabTopicLoad: async function () {
            let uid = this.user.id
            let retList = await api.topic.list({
                user_id: uid,
                order: 'time.desc',
                loadfk: {'user_id': null, 'board_id': null}
            })
            this.tabs.topic.topics = retList.data
        },
        tabCommentLoad: async function () {
            let uid = this.user.id
            let retList = await api.comment.list({
                user_id: uid,
                order: 'time.desc',
                loadfk: {}
            })
            this.tabs.comment.data = retList.data
        },
        handleTabChange (val) {
            this.activeTab = val
            if (val === 'tab2') {
                this.tabCommentLoad()
            }
        },
        handleActive () {
            // window.alert('tab active')
        },
        fetchData: async function () {
            let role = null
            let params = this.$route.params

            if (state.user && (params.id === state.user.id)) role = 'user'
            let ret = await api.user.get(params, role)

            if (ret.code === api.retcode.SUCCESS) {
                this.user = ret.data
                await this.tabTopicLoad()
            } else {
                $.message_by_code(ret.code)
            }
        }
    },
    watch: {
        // 如果路由有变化，会再次执行该方法
        '$route': 'fetchData'
    },
    created: async function () {
        let key = state.loadingGetKey(this.$route)
        this.state.loadingInc(this.$route, key)
        await this.fetchData()
        this.state.loadingDec(this.$route, key)
    },
    components: {
        Avatar
    }
}
</script>
