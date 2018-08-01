<template>
<div class="ic-container box">
    <div class="login">
        <h3 class="title">注册</h3>
        <form class="ic-form">
            <check-row :results="formErrors.email" :check="(!info.email) || checkEmail" :text="'邮箱格式不正确'">
                <label for="email">邮箱</label>
                <input type="email" name="email" id="email" v-model="info.email">
            </check-row>
            <check-row :results="formErrors.nickname" :check="(!info.nickname) || checkNickname" :text="'至少两个汉字，或以汉字/英文字符开头至少4个字符'">
                <label for="nickname">昵称</label>
                <input type="text" name="nickname" id="nickname" v-model="info.nickname">
            </check-row>
            <check-row :results="formErrors.password" :check="(!info.password) || checkPassword" :text='checkPasswordText'>
                <label for="password">密码</label>
                <input type="password" name="password" id="password" v-model="info.password">
            </check-row>
            <check-row :results="formErrors.password2" :check="(!info.password2) || checkPassword2" :text="'重复密码应与前密码一致'">
                <label for="password2">重复密码</label>
                <input type="password" name="password2" id="password2" v-model="info.password2">
            </check-row>
            <check-row :results="formErrors.verify" v-if="0">
                <label for="verify">验证码</label>
                <input type="text" name="verify" id="verify" v-model="info.verify">
            </check-row>
            <check-row style="display: flex;align-items: center;" :check="info.agreeLicense">
                <mu-checkbox v-model="info.agreeLicense"/>
                <span style="flex-shrink: 0; cursor: pointer; user-select: none;" @click="info.agreeLicense = !info.agreeLicense">同意<a href="javascript:void(0)" @click.stop="dialogLicense = true">用户许可协议</a></span>
            </check-row>
            <div class="ic-form-row">
                <input class="ic-btn success" :class="{ disabled : !info.agreeLicense }" type="submit" @click.prevent="register" value="注 册" style="width: 100%">
            </div>
        </form>
    </div>

    <mu-dialog :open="dialogLicense" title="用户许可协议">
        <div>
            <span>协议正文</span>
        </div>
        <mu-flat-button label="确定" slot="actions" primary @click="dialogLicense = false"/>
    </mu-dialog>

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

export default {
    data () {
        return {
            info: {
                email: '',
                nickname: '',
                password: '',
                password2: '',
                verify: '',
                agreeLicense: false,
                returning: true // new 之后返回记录
            },
            dialogLicense: false,
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
        checkNickname: function () {
            if ((this.info.nickname < 2) || (this.info.nickname > 32)) return false
            // 检查首字符，检查有无非法字符
            if (!/^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]+$/.test(this.info.nickname)) {
                return false
            }
            // 若长度大于4，直接许可
            if (this.info.nickname.length >= 4) {
                return true
            }
            // 长度小于4，检查其中汉字数量
            let m = this.info.nickname.match(/[\u4e00-\u9fa5]/gi)
            if (m && m.length >= 2) return true
        },
        checkEmail: function () {
            let mail = /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
            return mail.test(this.info.email)
        }
    },
    methods: {
        register: async function () {
            if (!this.info.agreeLicense) {
                return
            }
            if (this.checkPassword && this.checkPassword2 && this.checkEmail && this.checkNickname) {
                let ret = await api.user.new(this.info)
                if (ret.code !== api.retcode.SUCCESS) {
                    this.formErrors = ret.data
                    $.message_by_code(ret.code)
                } else {
                    let userinfo = ret.data
                    if (ret.code === 0) {
                        api.saveAccessToken(userinfo['access_token'])
                        ret = await api.user.get({id: ret.data.id}, 'user')
                        Vue.set(state, 'user', ret.data)
                        $.notifLoopOn()
                        $.message_by_code(ret.code)
                    } else {
                        $.message_error('注册失败！可能账号或昵称已经被注册')
                    }
                    this.$router.push({name: 'forum', params: {}})
                }
            } else {
                $.message_error('请正确填写所有项目')
            }
        }
    },
    components: {
    }
}
</script>
