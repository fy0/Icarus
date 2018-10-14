<template>
<ic-dialog v-if="state.user" :width="'360px'" v-model="state.dialog.userSetNickname" :title="`修改用户昵称`" scrollable>
    <div>
        <form class="ic-form">
            <check-row>
                <label for="nickname">当前昵称</label>
                <div>{{state.user.nickname}}</div>
            </check-row>
            <check-row :results="formErrors.nickname" :check="(!info.nickname) || checkNickname" :text="'至少两个汉字，或以汉字/英文字符开头至少4个字符'">
                <label for="nickname">新昵称</label>
                <input class="ic-input" type="text" name="nickname" id="nickname" v-model="info.nickname">
            </check-row>
        </form>
    </div>
    <div class="bottom">
        <span class="ic-btn primary" @click="ok">确定</span>
        <span class="ic-btn secondary" @click="cancel">取消</span>
    </div>
</ic-dialog>
</template>

<style lang="scss" scoped>
.ic-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-bottom: 20px;
    margin-top: -20px;
}

.ic-form-row > * {
    width: 100%;
}

.ic-form-row {
    width: 100%;
    padding-top: 10px;
    padding-bottom: 10px;
}

.bottom {
    text-align: center;

    .ic-btn {
        padding-left: 30px;
        padding-right: 30px;
        margin-left: 10px;
    }
}
</style>

<script>
import state from '@/state.js'
import api from '@/netapi.js'

export default {
    data () {
        return {
            state,
            formErrors: {
                nickname: []
            },
            info: {
                nickname: ''
            },
            sending: false
        }
    },
    methods: {
        ok: async function () {
            if (await this.changeNickname()) {
                state.dialog.userSetNickname = null
            }
        },
        cancel: async function () {
            state.dialog.userSetNickname = null
        },
        checkNickname: function () {
            return $.checkNickname(this.info.nickname)
        },
        changeNickname: async function () {
            if (this.sending) return
            this.sending = true

            let ret = await api.user.changeNickname(this.info.nickname)
            if (ret.code === api.retcode.SUCCESS) {
                $.message_success('修改成功！')
                state.user.nickname = ret.data.nickname
                state.user.change_nickname_chance = ret.data.change_nickname_chance
                this.sending = false
                return true
            } else if (ret.code === api.retcode.INVALID_POSTDATA) {
                this.formErrors = ret.data
            }
            this.sending = false
        }
    }
}
</script>
