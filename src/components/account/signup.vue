<template>
<div class="ic-container box">
    <div class="login">
        <h3 class="title">注册</h3>
        <form class="ic-form">
            <check-row :results="formErrors.email" :check="(!info.email) || checkEmail" :text="'邮箱格式不正确'">
                <label for="email">邮箱</label>
                <input type="email" name="email" id="email" v-model="info.email">
            </check-row>
            <check-row :results="formErrors.password" :check="(!info.password) || checkPassword" :text='checkPasswordText'>
                <label for="password">密码</label>
                <input type="password" name="password" id="password" v-model="info.password">
            </check-row>
            <check-row :results="formErrors.password2" :check="(!info.password2) || checkPassword2" :text="'重复密码应与前密码一致'">
                <label for="password2">重复密码</label>
                <input type="password" name="password2" id="password2" v-model="info.password2">
            </check-row>
            <check-row :results="formErrors.verify">
                <label for="verify">验证码</label>
                <input type="text" name="verify" id="verify" v-model="info.verify">
            </check-row>
            <div class="ic-form-row">
                <input class="ic-btn green click" type="submit" @click.prevent="register" value="注 册" style="width: 100%">
            </div>
        </form>
    </div>
</div>
</template>

<style scoped>
.title {
    color: #444;
}

.box {
    display: flex;
    align-items: center;
}

.login {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-left: auto;
    margin-right: auto;
}

.ic-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 320px;

    padding: 10px 30px;
    border: 1px solid #ddd;
}

.ic-form-row > * {
    width: 100%;
}

.ic-form-row {
    width: 100%;
    padding-top: 10px;
    padding-bottom: 10px;
}
</style>

<script>
import api from '@/netapi.js'
import state from '@/state.js'
import CheckRow from './checkrow.vue'

export default {
    data () {
        return {
            info: {
                email: '',
                password: '',
                password2: '',
                verify: ''
            },
            formErrors: {}
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
        },
        checkEmail: function () {
            let mail = /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
            return mail.test(this.info.email)
        }
    },
    methods: {
        register: async function () {
            if (this.checkPassword && this.checkPassword2 && this.checkEmail) {
                let ret = await api.user.new(this.info)
                if (ret.code !== api.retcode.SUCCESS) {
                    this.formErrors = ret.data
                    $.message_by_code(ret.code)
                } else {
                    let userinfo = ret.data
                    console.log(userinfo)
                    $.message_by_code(ret.code)
                }
            } else {
                $.message_error('请正确填写所有项目')
            }
        }
    },
    components: {
        CheckRow
    }
}
</script>
