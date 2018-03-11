<template>
<admin-base>
    <div class="search-box" v-if="false">
        <input v-model="searchTxt" />
        <mu-raised-button @click="doSearch()" label="搜索" class="search-btn" primary/>
    </div>
    <div>
        <ul class="ic-collection">
            <li class="item ic-collection-item" v-for="i in topics.items" :key="i.id">
                <router-link tag="b" class="title" :title="i.title" :to="{ name: 'forum_topic', params: {id: i.id} }">
                    <span>{{i.title}}</span>
                    <span class="icons">
                        <i v-if="i.awesome == 1" class="mdi-icarus icon-diamond" title="优秀" style="color: #e57272"></i>
                        <i v-if="false" class="mdi-icarus icon-crown" title="精华" style="color: #e8a85d"></i>
                    </span>
                </router-link>
                <div class="info">
                    <router-link class="board" :to="{ name: 'forum_board', params: {id: i.board_id.id} }">{{i.board_id.name}}</router-link> ·
                    <user-link :user="i.user_id" /> ·
                    <ic-time :timestamp="i.time" /> ·
                    <span>{{state.misc.TOPIC_STATE_TXT[i.state]}}</span> ·
                    <i class="mdi-icarus ic-topic-manage-icon icon-sword-cross" title="管理" @click="setTopicManage(i)"></i>
                </div>
            </li>
        </ul>
    </div>
    <paginator :page-info='topics' :route-name='"admin_forum_topic"' />
</admin-base>
</template>

<style scoped>
.item > .title {
    cursor: pointer;
    margin-bottom: 15px;
    font-weight: bold;
    display: inline-block;
}

.item > .info > .board {
    background-color: #eee;
    padding: 4px;
}

.search-box {
    flex: 1;
    align-items: center;
    display: flex;
}

.search-box > input {
    width: 45%;
    height: 45px;
    padding: 10px 10px;
    margin-top: 1rem;
    margin-bottom: 1rem;
    background: #FFFFFF;
    border-radius: 2px;
    border: 1px solid #a4a4a4;
    font-size: 1.3rem;
    box-sizing: border-box;
    transition: all .2s ease;    
}

.search-box > .search-btn {
    height: 45px;
    margin-left: 10px;
}
</style>


<script>
import api from '@/netapi.js'
import state from '@/state.js'
import AdminBase from '../base/base.vue'

export default {
    data () {
        return {
            state,
            searchTxt: '',
            topics: {}
        }
    },
    methods: {
        setTopicManage: function (topic) {
            state.dialog.topicManageData = topic
            state.dialog.topicManage = true
        },
        fetchData: async function () {
            let params = this.$route.params
            let retList = await api.topic.list({
                order: 'sticky_weight.desc,weight.desc,time.desc',
                // select: 'id, time, user_id, board_id, title, state',
                loadfk: {'user_id': null, 'board_id': null, 'id': {'as': 's', loadfk: {'last_comment_id': {'loadfk': {'user_id': null}}}}}
            }, params.page)
            if (retList.code === api.retcode.SUCCESS) {
                this.topics = retList.data
            }
        }
    },
    created: async function () {
        this.state.loading++
        await this.fetchData()
        this.state.loading--
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
