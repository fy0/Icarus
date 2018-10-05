<template>
<div v-if="available" class="ic-container box">
    <span class="captain">用户激活</span>
    <div>{{text}}</div>
</div>
<page-not-found v-else />
</template>

<style scoped>
.box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.captain {
    font-size: 30px;
    font-weight: bolder;
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'

export default {
    data () {
        return {
            state,
            text: '正在发送请求 ...',
            available: false
        }
    },
    methods: {
        fetchData: async function () {
            let query = this.$route.query
            if (!(query.uid && query.code)) return
            this.available = true

            let ret = await api.user.activation(query.uid, query.code)
            if (ret.code === api.retcode.SUCCESS) {
                this.text = '帐号激活成功！'
            } else {
                this.available = false
            }
        }
    },
    created: async function () {
        await this.fetchData()
    }
}
</script>
