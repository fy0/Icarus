<template>
<setting-base>
    <div v-title>用户设置 - {{$config.title}}</div>
    <span>测试。以后来个仪表盘什么的</span>
</setting-base>
</template>

<style scoped>
</style>

<script>
// import api from '@/netapi.js'
import SettingBase from './base/base.vue'

export default {
    data () {
        return {}
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
        this.$store.commit('LOADING_INC', 1)
        await this.fetchData()
        this.$store.commit('LOADING_DEC', 1)
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
