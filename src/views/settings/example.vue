<template>
<setting-base>
    <div v-title>用户设置 - {{state.config.title}}</div>
    <span>测试</span>
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
    methods: {
        fetchData: async function () {
            // let params = this.$route.params
            // let ret = await api.topic.get({
            //     id: params.id,
            // })
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
        SettingBase
    }
}
</script>
