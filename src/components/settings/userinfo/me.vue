<template>
<setting-base>
    <div v-title>个人信息 - 用户设置 - {{state.config.title}}</div>

    <div class="topic-manage-item">
        <span class="label">Email</span>
        <div class="right">
            <div>{{user.email}}</div>
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">昵称</span>
        <div class="right">
            <div>{{user.nickname}}</div>
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">注册时间</span>
        <div class="right">
            <ic-time :ago="false" :timestamp="user.time" />
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">最后登录时间</span>
        <div class="right">
            <ic-time :ago="false" :timestamp="user.key_time" />
        </div>
    </div>
    <div class="topic-manage-item">
        <span class="label">简介</span>
        <div class="right">
            <mu-text-field v-model="user.biology" :maxLength="255"/>
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">状态</span>
        <div class="right" style="display: flex">
            {{state.misc.POST_STATE_TXT[user.state]}}
        </div>
    </div>
    <div class="topic-manage-item" style="align-items: center">
        <span class="label">用户组</span>
        <div class="right" style="display: flex">
            {{state.misc.USER_GROUP_TXT[user.group]}}
        </div>
    </div>
</setting-base>
</template>

<style scoped>
</style>

<script>
// import api from '@/netapi.js'
import state from '@/state.js'
import SettingBase from '../base/base.vue'

export default {
    data () {
        return {
            state
        }
    },
    computed: {
        'user': function () {
            return state.user
        }
    },
    methods: {
        fetchData: async function () {
            // let params = this.$route.params
            // let ret = await api.topic.get({
            //     id: params.id,
            // })
        }
    },
    created: async function () {
        console.log(state.user)
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
        SettingBase
    }
}
</script>
