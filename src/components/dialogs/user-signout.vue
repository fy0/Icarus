<template>
<ic-dialog v-model="state.dialog.userSignout" :width="'500px'" :title="`退出登录`">
    <div class="main">
        <i class="far fa-question-circle icon"></i>
        <div>你确定要退出登录吗？</div>
    </div>
    <div class="bottom">
        <span class="ic-btn primary" @click="ok">
            <template v-if="quiting">正在登出 ...</template>
            <template v-else>确定，退出登录</template>
        </span>
        <span class="ic-btn secondary" @click="close">取消，留在这里</span>
    </div>
</ic-dialog>
</template>

<style lang="scss" scoped>
.icon {
    font-size: 74px;
}

.main {
    font-size: 1.5em;
    text-align: center;
    margin-bottom: 40px;
}

.bottom {
    text-align: center;

    .ic-btn {
        padding-left: 20px;
        padding-right: 20px;
        margin-left: 10px;
    }
}
</style>

<script>
import state from '@/state.js'
import api from '@/netapi.js'
import Vue from 'vue'

export default {
    data () {
        return {
            state,
            quiting: false
        }
    },
    methods: {
        ok: async function () {
            if (this.quiting) return
            this.quiting = true
            let ret = await api.user.signout()
            if (ret.code === api.retcode.SUCCESS || ret.code === api.retcode.FAILED) {
                $.message_success('登出成功')
                Vue.delete(state, 'user')
                state.reset()
                this.$router.replace('/')
            }
            this.quiting = false
            state.dialog.userSignout = false
        },
        close: async function () {
            state.dialog.userSignout = false
        }
    }
}
</script>
