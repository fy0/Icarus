<template>
<div class="ic-container box">
    <div class="login">
        <h3 class="title">注册</h3>
        <form class="ic-form">
            <div class="ic-form-row">
                <label for="username">帐号</label>
                <input type="text" name="username" id="username" v-model="info.username">
            </div>
            <check-row :check="checkPassword">
                <label for="password">密码</label>
                <input type="password" name="password" id="password" v-model="info.password">
            </check-row>
            <check-row :check="checkPassword2" :text="'重复密码应与前密码一致'">
                <label for="password2">重复密码</label>
                <input type="text" name="password2" id="password2" v-model="info.password2">
            </check-row>
            <check-row :check="info.email && checkEmail" :text="''">
                <label for="email">电子邮箱</label>
                <input type="email" name="email" id="email" v-model="info.email">
            </check-row>
            <div class="ic-form-row">
                <label for="verify">验证码</label>
                <input type="text" name="verify" id="verify" v-model="info.verify">
            </div>
            <div class="ic-form-row">
                <input class="ic-btn green click" type="submit" @click="register" value="注 册" style="width: 100%">
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
    height: 80vh;
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
import CheckRow from './checkrow.vue'

export default {
    data () {
        return {
            info: {
                username: '',
                password: '',
                password2: '',
                email: '',
                verify: ''
            }
        }
    },
    computed: {
        checkEmail: function () {
            let mail = /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
            return mail.test(this.info.email)
        },
        checkPassword: function () {
            return true
        },
        checkPassword2: function () {
            return this.info.password === this.info.password2
        }
    },
    methods: {
        valid: function () {
            // border-color: #ff4949 !important;
        },
        register: async function () {
            console.log(this.info)
        }
    },
    components: {
        CheckRow
    }
}
</script>
