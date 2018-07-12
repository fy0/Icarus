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
            <div class="ic-form-row">
                <router-link class="lost-poasswrod" :to="{name: 'account_password_reset_request'}">忘记密码？</router-link>
            </div>
            <div class="ic-form-row three-auth">
                <span class="title"> 第三方登录 </span>
                <div class="icons">
                    <span class="icon">QQ</span>
                    <span class="icon">微博</span>
                    <span class="icon">Github</span>
                    <input type="submit" name="" value="github" @click.prevent="github_url">
                </div>
            </div>
        </form>
    </div>
</div>
</template>

<style scoped>
.three-auth {
    display: flex;
    flex-direction: column;
}

.three-auth > .title {
    text-align: center;
}

.three-auth > .title:before, .three-auth > .title:after {
    display: inline-block;
    width: 50px;
    content: " ";
    border-top: 1px solid #ccc;
    vertical-align: middle;
}

.three-auth > .icons {
    display: flex;
    justify-content: center;
}

.three-auth > .icons > .icon {
    border: 1px solid #ccc;
    border-radius: 4px;
}

.three-auth > .icons > .icon:not(:first-child) {
    margin-left: 20px;
}

.lost-poasswrod {
    color: #aaa;
}

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
            state,
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
            let key = state.loadingGetKey(this.$route)
            if (this.checkEmail && this.checkPassword) {
                this.state.loadingInc(this.$route, key)
                let ret = await api.user.signin(this.info)
                if (ret.code === api.retcode.SUCCESS) {
                    ret = await api.user.get({id: ret.data.id}, 'inactive_user')
                    if (ret.code !== api.retcode.SUCCESS) return
                    Vue.set(state, 'user', ret.data) // 这样顶栏可以接到事件
                    $.notifLoopOn()

                    if (this.goLastPage) {
                        this.state.loadingDec(this.$route, key)
                        $.message_success('登录成功，正在回到前页……')
                        this.$router.go(-1)
                    } else {
                        this.state.loadingDec(this.$route, key)
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
                this.state.loadingDec(this.$route, key)
            } else {
                $.message_error('请正确填写所有项目')
            }
        },
        github_url: async function () {
            // 获取url，然后跳转
            let ghUrl = await api.Oauth.getUrl('github')
            window.open(ghUrl, '_blank')
            console.log(ghUrl)
            return
        }
    },
    components: {
        CheckRow
    }
}
</script>
