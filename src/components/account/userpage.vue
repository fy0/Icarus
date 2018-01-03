<template>
<div class="ic-container">
    <div class="userpage">
        <div class="left">
            <avatar :user="user" :size="164" class="avatar"></avatar>            
            <p>{{user.nickname}}</p>
            <p>{{state.misc.USER_GROUP_TXT[user.group]}}</p>
        </div>
        <div class="right">
            <mu-tabs :value="activeTab" @change="handleTabChange" class="api-view-tabs">
                <mu-tab value="tabTopic" title="主题" @active="handleActive"/>
                <mu-tab value="tab2" title="评论"/>
                <mu-tab value="tab3" title="收藏" @active="handleActive"/>
                <mu-tab value="tab4" title="关注"/>
            </mu-tabs>
            <div class="tab" v-if="activeTab === 'tabTopic'">
                <div v-if="tabs.topic.topics">
                    <mu-timeline>
                        <mu-timeline-item :key="i.id" v-for="i in tabs.topic.topics.items">
                            <span slot="time">{{i.time}}</span>
                            <span slot="des">{{i.title}}</span>
                        </mu-timeline-item>
                    </mu-timeline>
                </div>
                <mu-circular-progress v-else :strokeWidth="5" :size="90" color="red"/>
            </div>
            <div class="tab" v-if="activeTab === 'tab2'">
                <h2>Tab Two</h2>
                <p>
                    这是第二个 tab
                </p>
            </div>
            <div class="tab" v-if="activeTab === 'tab3'">
                <h2>Tab Three</h2>
                <p>
                这是第三个 tab
                </p>
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
    flex: 1 0 auto;
}

.userpage > .right {
    flex: 8 0 auto;
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
        handleTabChange (val) {
            this.activeTab = val
        },
        handleActive () {
            console.log(111)
            // window.alert('tab active')
        }
    },
    beforeRouteEnter: async (to, from, next) => {
        let ret = await api.user.get(to.params)

        if (ret.code === api.retcode.SUCCESS) {
            return next(async vm => {
                vm.user = ret.data
                await vm.tabTopicLoad()
            })
        }

        $.message_by_code(ret.code)
        return next('/')
    },
    components: {
        Avatar
    }
}
</script>
