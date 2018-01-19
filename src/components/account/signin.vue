<template>
<div class="ic-container box">
    <div class="login">
        <h3 class="title">登录</h3>
        <form class="ic-form">
            <check-row :results="formErrors.email" :check="(!info.email) || checkEmail" :text="'邮箱格式不正确'">
                <label for="email">邮箱</label>
                <input type="email" name="email" id="email" v-model="info.email">
            </check-row>
            <check-row :results="formErrors.password" :check="(!info.password) || checkPassword" :text='checkPasswordText'>
                <label for="password">密码</label>
                <input type="password" name="password" id="password" v-model="info.password">
            </check-row>
            <div class="ic-form-row">
                <input class="ic-btn green click" type="submit" @click.prevent="login" name="" value="登 录">
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
import Vue from 'vue'
import api from '@/netapi.js'
import state from '@/state.js'
import CheckRow from '../utils/checkrow.vue'

export default {
    data () {
        return {
            info: {
                email: '',
                password: ''
            },
            goLastPage: false,
            formErrors: {}
        }
    },
    computed: {
        checkEmail: function () {
            let mail = /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
            return mail.test(this.info.email)
        },
        checkPasswordText: function () {
            return `应在 ${state.misc.PASSWORD_MIN}-${state.misc.PASSWORD_MAX} 个字符之间`
        },
        checkPassword: function () {
            if (this.info.password.length < state.misc.PASSWORD_MIN) return false
            if (this.info.password.length > state.misc.PASSWORD_MAX) return false
            return true
        }
    },
    beforeRouteEnter (to, from, next) {
        next(vm => {
            vm.goLastPage = from.fullPath !== '/'
        })
    },
    methods: {
        login: async function () {
            if (this.checkEmail && this.checkPassword) {
                state.loading++
                let ret = await api.user.signin(this.info)
                if (ret.code === api.retcode.SUCCESS) {
                    ret = await api.user.get({id: ret.data.id}, 'user')
                    if (ret.code !== api.retcode.SUCCESS) return
                    Vue.set(state, 'user', ret.data) // 这样顶栏可以接到事件

                    if (this.goLastPage) {
                        state.loading--
                        $.message_success('登录成功，正在回到前页……')
                        this.$router.go(-1)
                    } else {
                        state.loading--
                        $.message_success('登录成功，正在回到主页……')
                        this.$router.replace('/')
                        return
                    }
                } else {
                    this.formErrors = ret.data
                    $.message_by_code(ret.code)
                }
                // ret = await api.user.get({username: this.info.username}, 'test')
                // console.log(ret)
                state.loading--
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
