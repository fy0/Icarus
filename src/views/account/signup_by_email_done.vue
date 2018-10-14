<template>
<redirecting v-if="regDone">
    <span>注册流程已全部完成。</span>
    <span>欢迎来到 {{state.config.title}}，{{state.user.nickname}}</span>
</redirecting>
<div v-else-if="available" class="ic-container box">
    <span class="captain">激活账号</span>
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
import Vue from 'vue'

export default {
    data () {
        return {
            state,
            text: '正在发送请求 ...',
            regDone: false,
            available: false
        }
    },
    methods: {
        fetchData: async function () {
            let query = this.$route.query
            if (!(query.email && query.code)) return
            this.available = true

            let ret = await api.user.signupByEmail(query.email, query.code)
            if (ret.code === api.retcode.SUCCESS) {
                this.text = '注册完成，正在进行收尾……'
                api.saveAccessToken(ret.data.key)
                ret = await api.user.get({ id: ret.data.id }, 'inactive_user')
                Vue.set(state, 'user', ret.data)
                this.regDone = true
            } else {
                if (ret.code === api.retcode.ALREADY_EXISTS) {
                    $.message_error('帐户已经存在')
                } else {
                    $.message_by_code(ret.code, ret.data)
                }
                this.available = false
            }
        }
    },
    created: async function () {
        await this.fetchData()
    }
}
</script>
