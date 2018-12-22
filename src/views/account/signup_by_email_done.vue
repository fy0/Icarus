<template>
<redirecting v-if="regDone">
    <span>注册流程已全部完成。</span>
    <span>欢迎来到 {{$config.title}}，{{$user.data.nickname}}</span>
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

export default {
    data () {
        return {
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
                await this.$store.dispatch('user/apiGetUserData', ret.data.id)
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
