<template>
<div v-if="available" class="ic-container box">
    <form class="ic-form">
        <div class="ic-form-row">
            <span></span>
            <h4 style="margin: 0">密码重置</h4>
        </div>

        <check-row :flex="true" :results="formErrors.password" :check="(!info.password) || checkPassword" :text='checkPasswordText'>
            <label for="password">新密码</label>
            <input type="password" name="password" id="password" v-model="info.password">
        </check-row>

        <check-row :flex="true" :results="formErrors.password2" :check="(!info.password2) || checkPassword2" :text="'重复密码应与前密码一致'">
            <label for="password2">重复密码</label>
            <input type="password" name="password2" id="password2" v-model="info.password2">
        </check-row>

        <div class="ic-form-row">
            <span></span>
            <input class="ic-btn green click" type="submit" @click.prevent="resetPassword" value="确 认">
        </div>
    </form>
</div>
<page-not-found v-else />
</template>

<style scoped>
.ic-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 420px;

    padding: 10px 30px;
}

.ic-form-row {
    display: flex;
    align-items: center;
    padding-top: 10px;
    padding-bottom: 10px;
    width: 100%;
}

.ic-form-row > :nth-child(1) {
    padding-right: 10px;
    flex: 3 0 0;
}

.ic-form-row > label {
    text-align: right;
}

.ic-form-row > :nth-child(2) {
    flex: 7 0 0;
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import CheckRow from '../utils/checkrow.vue'

export default {
    data () {
        return {
            info: {
                old_password: '',
                password: '',
                password2: '',
                verify: ''
            },
            formErrors: {},
            available: false
        }
    },
    computed: {
        checkPasswordText: function () {
            return `应在 ${state.misc.PASSWORD_MIN}-${state.misc.PASSWORD_MAX} 个字符之间`
        },
        checkPassword: function () {
            if (this.info.password.length < state.misc.PASSWORD_MIN) return false
            if (this.info.password.length > state.misc.PASSWORD_MAX) return false
            return true
        },
        checkPassword2: function () {
            return this.info.password === this.info.password2
        }
    },
    methods: {
        resetPassword: async function () {
            if (this.checkPassword && this.checkPassword2) {
                let ret = await api.user.changePassword(this.info)
                if (ret.code !== api.retcode.SUCCESS) {
                    this.formErrors = ret.data
                    $.message_error('修改密码失败')
                } else {
                    api.saveAccessToken(ret.data)
                    $.message_by_code(ret.code)
                    this.info.old_password = ''
                    this.info.password = ''
                    this.info.password2 = ''
                    this.info.verify = ''
                }
            } else {
                $.message_error('请正确填写所有项目')
            }
        },
        fetchData: async function () {
            this.available = true
            /*
            let query = this.$route.query
            if (!(query.uid && query.code)) return
            this.available = true

            let ret = await api.user.activation(query.uid, query.code)
            if (ret.code === api.retcode.SUCCESS) {
                this.text = '帐号激活成功！'
            } else {
                this.available = false
            }
            */
        }
    },
    created: async function () {
        await this.fetchData()
    },
    components: {
        CheckRow
    }
}
</script>
